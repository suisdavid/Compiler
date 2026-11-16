from __future__ import annotations
from dataclasses import dataclass,field
from codegen.model import *
from utils.util import util

#next update: free variables when they're no longer used
class Generator:
    class Allocator: #for register allocating
        def __init__(self,phiMap:dict[str,str]):
            self.in_use=[0]*32
            self.stk_offset=0
            self.rbp_offset=8#for rbp_addr and ret_addr
            self.varpos={}#varName to position(Position)
            self.phiMap=phiMap

        def addUnit(self,varName:str):
            self.varpos[varName]=Position(reg=False,id=0,const=True)

        def find_usable_reg(self)->int:
            for name in util.useregs:
                idx=util.regMap[name]
                if self.in_use[idx]==0:
                    return idx
            return -1 
        
        def allocate(self,varName:str,varSize:int=4,is_param:bool=False)->Position:
            if not varName.startswith("%"): #instant number
                if varName=='true':
                    return Position(reg=False,id=True,const=True)
                elif varName=='false':
                    return Position(reg=False,id=False,const=True)
                else:
                    return Position(reg=False,id=int(varName),const=True)
            if self.phiMap.get(varName):
                varName=self.phiMap[varName]

            pos=self.varpos.get(varName)
            if pos:
                return pos
            else:
                if is_param==True:
                    if varSize<=4 and 0 in self.in_use[util.paramStart:util.paramStart+util.paramNum]:
                        idx=self.in_use[util.paramStart:].index(0)+util.paramStart
                        self.in_use[idx]=1
                        self.varpos[varName]=Position(reg=True,id=idx)
                    else:
                        self.rbp_offset+=varSize
                        self.varpos[varName]=Position(reg=False,id=-(self.rbp_offset-varSize))#<0 indicates rbp offset
                else:
                    idx=self.find_usable_reg()
                    if varSize<=4 and idx!=-1:
                        self.in_use[idx]=1
                        self.varpos[varName]=Position(reg=True,id=idx)
                    else:
                        self.stk_offset+=varSize
                        self.varpos[varName]=Position(reg=False,id=self.stk_offset-varSize)#>=0 indicates rsp offset
                return self.varpos[varName]
            
        def free(self,varName:str):
            pos=self.varpos.get(varName)
            if pos and pos.reg:
                self.in_use[pos.id]=0

        def check_free(self):#check whether some registers can be freed
            pass

    def __init__(self,functions:list[FunctionDescriptions],output_path:str):
        self.functions=functions
        self.reservedFunctionName=["main","print_i32","println_i32","get_i32","__rx_alloc"]
        self.functions.append(FunctionDescriptions(identifier="print_i32",param_types=["i32"],param_num=1,ret_size=0,block=[]))
        self.functions.append(FunctionDescriptions(identifier="println_i32",param_types=["i32"],param_num=1,ret_size=0,block=[]))
        self.functions.append(FunctionDescriptions(identifier="get_i32",param_types=[],param_num=0,ret_size=4,block=[]))
        self.functions.append(FunctionDescriptions(identifier="__rx_alloc",param_types=["i32","i32"],param_num=2,ret_size=4,block=[]))
        self.output=output_path
        self.varSize={}#varname to Size
        self.varType={}#varname to Type(IR-based)
        self.functionAllocators={}#function name to allocator
        self.callOffset={}#offset needed for passing parameters
        self.gen=[]

        self.arithmeticOps=['add','sub','mul','and','or','xor','shl','lshr','ashr','sdiv','udiv','srem','urem']
    def Emit(self,opcode:int,rd:int,r1:int,r2:int=0,label:str=None):
        self.ops.append(Op(opcode=opcode,rd=rd,r1=r1,r2=r2,label=label))

    def GetStackOffset(self,offset:int,sp:bool=True)->tuple[int,int]:#non-negative offset to rsp/rbp, returns (rs1,imm)
        r0=util.regMap['sp'] if sp else util.regMap['gp']
        if offset<2048:
            return r0,offset
        r1=util.regMap[util.tempregs[3]] 
        if offset%4096>=2048:
            self.Emit(Opcode.LUI,r1,(offset>>12)+1)
            offset=offset%4096-4096
        else:
            self.Emit(Opcode.LUI,r1,offset>>12)
            offset%=4096
        self.Emit(Opcode.ADD,r1,r1,r0)
        return r1,offset


    def LoadConst(self,offset:int,available:int=0)->int:#load offset into the available temp register
        rd=util.regMap[util.tempregs[3]] 
        if offset>=0:
            if offset%4096>=2048:
                self.Emit(Opcode.LUI,rd,(offset>>12)+1)
                offset=offset%4096-4096
            else:
                self.Emit(Opcode.LUI,rd,offset>>12)
                offset%=4096
        else:
            offset=-offset
            if offset%4096>2048:
                self.Emit(Opcode.LUI,rd,-((offset>>12)+1))
                offset=4096-offset%4096
            else:
                self.Emit(Opcode.LUI,rd,-(offset>>12))
                offset=-(offset%4096)
        res=util.regMap[util.tempregs[available]]
        self.Emit(Opcode.ADDI,res,rd,offset)
        return res


    def Load(self,pos:Position,r1:int):#Load four bytes from r1(addr) into po
        if pos.reg:
            self.Emit(Opcode.LW,pos.id,r1,0)
        else:
            tp=util.regMap[util.tempregs[2]] 
            self.Emit(Opcode.LW,tp,r1,0)
            r2,imm=self.GetStackOffset(pos.id,True) if pos.id>=0 else self.GetStackOffset(-pos.id,False)
            self.Emit(Opcode.SW,tp,r2,imm)
    
    def Store(self,pos:Position,r1:int):#Load four bytes from pos into r1(addr)
        if pos.const:
            self.Emit(Opcode.SW,self.LoadConst(pos.id),r1,0)
        elif pos.reg:
            self.Emit(Opcode.SW,pos.id,r1,0)
        else:
            r2,imm=self.GetStackOffset(pos.id,True) if pos.id>=0 else self.GetStackOffset(-pos.id,False)
            tp=util.regMap[util.tempregs[2]] 
            self.Emit(Opcode.LW,tp,r2,imm)
            self.Emit(Opcode.SW,tp,r1,0)


    def LoadStackOffset(self,offset:int,available:int=0,sp:bool=True):#load sp/gp+offset into the available temp register
        rd=util.regMap[util.tempregs[available]] 
        r0=util.regMap['sp'] if sp else util.regMap['gp']
        if offset<2048 and offset>=-2048:
            self.Emit(Opcode.ADDI,rd,r0,offset)
        else:
            self.LoadConst(offset,available)
            self.Emit(Opcode.ADD,rd,r0,rd)
        
        
    def Add(self,rd:int,offset:int=0):#rd+=offset
        if offset==0:
            return
        if offset>=-2048 and offset<2048:
            self.Emit(Opcode.ADDI,rd,rd,offset)
        else:
            self.Emit(Opcode.ADD,rd,rd,self.LoadConst(offset))

    def PutInReg(self,pos:Position,available:int=0)->int:#return temp register id,available is provided temp register id
        if pos.const:#const but not in size limit
            self.LoadConst(pos.id,available)
            return util.regMap[util.tempregs[available]]
        if pos.reg:
            return pos.id
        r1,imm=self.GetStackOffset(pos.id) if pos.id>=0 else self.GetStackOffset(-pos.id,False)
        rd=util.regMap[util.tempregs[available]]
        self.Emit(Opcode.LW,rd,r1,imm)#load i32
        return rd

           
    def ArithmeticEmit(self,opcode:int,rd:Position,r1:int,r2:int=0):#automatic writes to the store position of rd
        if rd.reg:
            self.Emit(opcode,rd.id,r1,r2)
        else:
            r0=util.regMap[util.tempregs[0]]
            self.Emit(opcode,r0,r1,r2)
            r1,imm=self.GetStackOffset(rd.id,True) if rd.id>=0 else self.GetStackOffset(-rd.id,False)
            self.Emit(Opcode.SW,r0,r1,imm)#store i32

    def Mov(self,new_pos:Position,prev_pos:Position):#Mov four bytes from prev_pos to new_pos
        self.ArithmeticEmit(Opcode.ADDI,new_pos,self.PutInReg(prev_pos),0)

    def Call(self,caller:FunctionDescriptions,callee:str,paramList:list[tuple[int,str]],retval:str=None,retsize:int=0):
        #step 1: calculate the conflicting local and param registers
        conflict=[]
        caller_allocator=self.functionAllocators[caller.identifier]
        callee_allocator=self.functionAllocators[callee]
        sp=util.regMap['sp']
        gp=util.regMap['gp']
        ra=util.regMap['ra']
        a0=util.regMap['a0']
        for i in range(32):
            if caller_allocator.in_use[i]:
                conflict.append(i)
                self.Emit(Opcode.SW,i,sp,len(conflict)*(-4))
        offset=len(conflict)*4+self.callOffset[callee]
        self.Add(sp,-offset)
        self.Emit(Opcode.SW,gp,sp,-8)#store previous rbp

        #step 2: put params into param registers or stack
        for i in range(len(paramList)):
            size,name=paramList[i]
            prev_pos=caller_allocator.allocate(name)
            new_pos=callee_allocator.varpos.get(f"%param{i+1}")
            if new_pos.reg==False:#updated rsp effect
                new_pos=Position(reg=False,id=-new_pos.id)
            if prev_pos.reg==False and prev_pos.const==False and prev_pos.id>=0:#updated rsp effect
                prev_pos=Position(reg=False,id=prev_pos.id+offset)

            if size==0:
                continue
            elif size==4:
                self.Mov(new_pos,prev_pos)
            else:
                self.LoadStackOffset(prev_pos.id,0,True) if prev_pos.id>=0 else self.LoadStackOffset(-prev_pos.id,0,False)
                self.LoadStackOffset(new_pos.id,1)
                self.LoadConst(size,2)
                self.Emit(Opcode.JAL,util.regMap['t6'],0,0,"internal.memcpy")

        #step 3: update rbp and call(ra is pushed into stack at the beginning of the callee function so that pc is not needed)
        self.Emit(Opcode.ADDI,gp,sp,-8)#update rbp
        self.Emit(Opcode.JAL,ra,0,0,f'{callee}.real_entry')

        #rsp -= 8+final_stk_offset at the beginning of the callee function, and returned to the -offset at the end of the callee function
        #step 4: return to original status(rbp is recovered at the end of the callee function)
        self.Add(sp,offset)
        for i in range(len(conflict)):
            self.Emit(Opcode.LW,conflict[i],sp,(i+1)*(-4))

        #step 5: pass retval
        if retval:
            if retsize==0:
                caller_allocator.addUnit(retval)
                return
            pos=caller_allocator.allocate(retval)
            if retsize==4:#passed with a0
                self.Mov(pos,Position(reg=True,id=a0))
            else: #passed with stack
                self.LoadStackOffset(pos.id,1,True)#must be allocated on stack
                self.LoadStackOffset(-offset,0,True)
                self.LoadConst(retsize,2)
                self.Emit(Opcode.JAL,util.regMap['t6'],0,0,"internal.memcpy")

            
            




    
    #function calling paradigm: ra store pc next,push stack addr into stack register, rsp-=offset; store used registers and params in reserved registers/ stack; jmp; retrieve stack addr
    def Register(self,function:FunctionDescriptions):
        #allocate params
        allocator=self.Allocator(function.phiMap)
        if function.ret_size>4:
            allocator.allocate(f"%param0",function.ret_size,True)#retval
        for i in range(function.param_num):
            allocator.allocate(f"%param{i+1}",util.GetIRAllocSize(function.param_types[i]),True)
        self.functionAllocators[function.identifier]=allocator
        self.callOffset[function.identifier]=allocator.rbp_offset

    #add,sub,mul,sdiv(udiv),srem(urem),and,or,xor,shl,lshr,ashr,icmp,alloca,load,store,getelementptr,extractvalue,zext,br,call,ret,unreachable,freeze,phi
    def Parse(self,function:FunctionDescriptions):
        identifier=function.identifier
        allocator=self.functionAllocators[identifier]
        for op in function.block:
            op=list(filter(lambda x: x!='', op.replace(',',' ').replace(" x ","x").split(' ')))#replace(" x ","x") is for handling array types
            if len(op)==0:
                continue
            allocator.check_free()
            if op[0].startswith("%"):
                opcode=op[2]
                rd=op[0]
                if opcode in self.arithmeticOps:
                    size=op[3]
                    r1=allocator.allocate(op[4])
                    r2=allocator.allocate(op[5])
                
                    if r1.const and r2.const:#constant folding
                        if opcode=='add':
                            allocator.varpos[rd]=Position(reg=False,id=util.s32(r1.id+r2.id),const=True)
                        elif opcode=='and':
                            allocator.varpos[rd]=Position(reg=False,id=util.s32(util.u32(r1.id)&util.u32(r2.id)),const=True)
                        elif opcode=='or':
                            allocator.varpos[rd]=Position(reg=False,id=util.s32(util.u32(r1.id)|util.u32(r2.id)),const=True)
                        elif opcode=='xor':
                            allocator.varpos[rd]=Position(reg=False,id=util.s32(util.u32(r1.id)^util.u32(r2.id)),const=True)
                        elif opcode=='sub':
                            allocator.varpos[rd]=Position(reg=False,id=util.s32(r1.id-r2.id),const=True)
                        elif opcode=='shl':
                            allocator.varpos[rd]=Position(reg=False,id=util.s32(util.u32(r1.id)<<(r2.id%32)),const=True)
                        elif opcode=='lshr':
                            allocator.varpos[rd]=Position(reg=False,id=util.s32((util.u32(r1.id)>>(r2.id%32))),const=True)
                        elif opcode=='ashr':
                            allocator.varpos[rd]=Position(reg=False,id=util.s32(r1.id>>(r2.id%32))) if r1.id>=0 else util.s32((util.u32(r1.id)>>(r2.id%32))-(1<<(32-r2.id%32)),const=True)
                        elif opcode=='mul':
                            allocator.varpos[rd]=Position(reg=False,id=util.s32(r1.id*r2.id),const=True)
                        elif opcode=='sdiv':
                            allocator.varpos[rd]=Position(reg=False,id=util.div(r1.id,r2.id)[0],const=True)
                        elif opcode=='udiv':
                            allocator.varpos[rd]=Position(reg=False,id=util.s32(util.u32(r1.id)//util.u32(r2.id)),const=True)
                        elif opcode=='srem':
                            allocator.varpos[rd]=Position(reg=False,id=util.div(r1.id,r2.id)[1],const=True)
                        elif opcode=='urem':
                            allocator.varpos[rd]=Position(reg=False,id=util.s32(util.u32(r1.id)%util.u32(r2.id)),const=True)

                    else:
                        pos=allocator.allocate(rd)
                        if r1.const and r1.id<2048 and r1.id>=-2048 and opcode in ['add','and','or','xor']:#no immediates for shifts!
                            opcodeI=[Opcode.ADDI,Opcode.ANDI,Opcode.ORI,Opcode.XORI][['add','and','or','xor'].index(opcode)]
                            r2=self.PutInReg(r2,0)
                            self.ArithmeticEmit(opcodeI,pos,r2,r1.id)
                        elif r2.const and r2.id<2048 and r2.id>-2048 and opcode in ['add','and','or','xor','sub']:
                            opcodeI=Opcode.ADDI
                            if opcode=='sub':
                                r2.id=-r2.id
                            else:
                                opcodeI=[Opcode.ADDI,Opcode.ANDI,Opcode.ORI,Opcode.XORI][['add','and','or','xor'].index(opcode)]
                            r1=self.PutInReg(r1,0)
                            self.ArithmeticEmit(opcodeI,pos,r1,r2.id)
                        else:
                            opcodeN=[Opcode.ADD,Opcode.SUB,Opcode.MUL,Opcode.AND,Opcode.OR,Opcode.XOR,Opcode.SLL,Opcode.SRL,Opcode.SRA,Opcode.DIV,Opcode.DIVU,Opcode.REM,Opcode.REMU][self.arithemticOps.index(opcode)]
                            r1=self.PutInReg(r1,0)
                            r2=self.PutInReg(r2,1)
                            self.ArithmeticEmit(opcodeN,pos,r1,r2)

                elif opcode =='icmp':#cmps
                    cmp=op[3]
                    size=op[4]
                    r1=allocator.allocate(op[5])
                    r2=allocator.allocate(op[6])

                    if r1.const and r2.const:#constant folding
                        if cmp=='sgt':
                            allocator.varpos[rd]=Position(reg=False,id=(r1.id>r2.id),const=True)
                        elif cmp=='slt':
                            allocator.varpos[rd]=Position(reg=False,id=(r1.id<r2.id),const=True)
                        elif cmp=='sge':
                            allocator.varpos[rd]=Position(reg=False,id=(r1.id>=r2.id),const=True)
                        elif cmp=='sle':
                            allocator.varpos[rd]=Position(reg=False,id=(r1.id<=r2.id),const=True)
                        elif cmp=='ugt':
                            allocator.varpos[rd]=Position(reg=False,id=(util.u32(r1.id)>util.u32(r2.id)),const=True) 
                        elif cmp=='ult':
                            allocator.varpos[rd]=Position(reg=False,id=(util.u32(r1.id)>util.u32(r2.id)),const=True)  
                        elif cmp=='uge':
                            allocator.varpos[rd]=Position(reg=False,id=(util.u32(r1.id)>util.u32(r2.id)),const=True)
                        elif cmp=='ule':
                            allocator.varpos[rd]=Position(reg=False,id=(util.u32(r1.id)>util.u32(r2.id)),const=True)
                    else:
                        pos=allocator.allocate(rd)
                        if r2.const and r2.id<2048 and r2.id>=-2048 and cmp in ['slt','ult']:
                            opcodeI=Opcode.SLTI if cmp=='slt' else Opcode.SLTIU
                            r1=self.PutInReg(r2,0)
                            self.ArithmeticEmit(opcodeI,pos,r1,r2.id)
                        else:
                            r1=self.PutInReg(r1,0)
                            r2=self.PutInReg(r2,1)
                            r3=util.regMap[util.tempregs[2]]
                            if cmp=='slt':
                                self.ArithmeticEmit(Opcode.SLT,pos,r1,r2)
                            elif cmp=='sgt':
                                self.ArithmeticEmit(Opcode.SLT,pos,r2,r1)
                            elif cmp=='sge':
                                self.Emit(Opcode.SLT,r3,r1,r2)
                                self.ArithmeticEmit(Opcode.XORI,pos,r3,1)
                            elif cmp=='sle':
                                self.Emit(Opcode.SLT,r3,r2,r1)
                                self.ArithmeticEmit(Opcode.XORI,pos,r3,1)
                            elif cmp=='ult':
                                self.ArithmeticEmit(Opcode.SLTU,pos,r1,r2)
                            elif cmp=='ugt':
                                self.ArithmeticEmit(Opcode.SLTU,pos,r2,r1)
                            elif cmp=='uge':
                                self.Emit(Opcode.SLTU,r3,r1,r2)
                                self.ArithmeticEmit(Opcode.XORI,pos,r3,1)
                            elif cmp=='ule':
                                self.Emit(Opcode.SLTU,r3,r2,r1)
                                self.ArithmeticEmit(Opcode.XORI,pos,r3,1)

                elif opcode=='zext':#extend i1 to i32, nothing change
                    allocator.varpos[rd]=allocator.allocate(op[4])

                elif opcode=='freeze': #create a (), make it 0
                    allocator.addUnit(rd)

                elif opcode=='phi':#use phiMap
                    pass

                elif opcode=='getelementptr':
                    type=op[3]
                    base=allocator.allocate(op[5])
                    r0=self.PutInReg(base)
                    pos=allocator.allocate(op[0])
                    idx=allocator.allocate(op[-1])
                    if len(op)>8:#the first idx must be zero
                        if type.startswith("["):#array
                            innerSize=util.GetIRAllocSize(util.GetArrayInfo(type)[0])
                            r1=self.PutInReg(idx,1)
                            r2=self.LoadConst(innerSize,2)
                            r3=util.regMap[util.tempregs[3]]
                            self.Emit(Opcode.MUL,r3,r1,r2)
                            self.ArithmeticEmit(Opcode.ADD,pos,r0,r3)
                        else:#struct, idx must be const
                            r1=self.LoadConst(util.GetFieldOffset(type,idx.id))
                            self.ArithmeticEmit(Opcode.ADD,pos,r0,r1)
                    else:
                        size=util.GetIRAllocSize(type)
                        r1=self.PutInReg(idx,1)
                        r2=self.LoadConst(size,2)
                        r3=util.regMap[util.tempregs[3]]
                        self.Emit(Opcode.MUL,r3,r1,r2)
                        self.ArithmeticEmit(Opcode.ADD,pos,r0,r3)

                elif opcode=='extractvalue':#Vec, const 
                    pos=allocator.allocate(op[0])
                    base=allocator.allocate(op[4])
                    r0=self.PutInReg(base)
                    idx=int(op[-1])
                    if idx!=0:
                        r1=util.regMap[util.tempregs[1]]
                        self.Emit(Opcode.ADDI,r1,r0,idx*4)
                        self.Load(pos,r1)
                    else:
                        self.Load(pos,r0)

                elif opcode=='alloca':
                    size=util.GetIRAllocSize(op[3])
                    allocator.stk_offset+=size
                    offset=allocator.stk_offset
                    pos=allocator.allocate(op[0])
                    sp=util.regMap['sp']

                    if offset<2048:
                        self.ArithmeticEmit(Opcode.ADDI,pos,sp,offset)
                    else:
                        self.ArithmeticEmit(Opcode.ADD,pos,sp,self.LoadConst(offset,0))

                elif opcode=='load':
                    size=util.GetIRAllocSize(op[3])
                    if size==0:
                        allocator.addUnit(op[0])
                        continue
                    pos=allocator.allocate(op[0],size)
                    base=allocator.allocate(op[5])
                    r1=self.PutInReg(base,0)
                    if size==4:#no need to call the internal.memcpy function when load size<=4
                        self.Load(pos,r1)
                    else:
                        self.LoadStackOffset(pos.id,1)#op[0] must be allocated on stack
                        self.LoadConst(size,2)
                        self.Emit(Opcode.JAL,util.regMap['t6'],0,0,"internal.memcpy")

                elif opcode=='call': #nonvoid call
                    retval=op[0]
                    retsize=util.GetIRAllocSize(op[3])
                    funcName=op[4][1:-1]
                    paramList=[]
                    for i in range(5,len(op)-1,2):
                        size=util.GetIRAllocSize(op[i])
                        name=op[i+1]
                        paramList.append((size,name))
                    self.Call(function,funcName,paramList,retval,retsize)#Call Function

                
            elif op[0]=='br':#jmp
                if op[1]=='i1':#conditional jump
                    cond,block1,block2=op[2], identifier+'.'+op[4][1:], identifier+'.'+op[6][1:]
                    r1=self.PutInReg(allocator.allocate(cond))
                    x0=util.regMap['zero']#zero
                    self.Emit(Opcode.BNE,0,r1,x0,block1)
                    self.Emit(Opcode.JAL,x0,0,0,block2)
                else:
                    block=identifier+'.'+op[2][1:]
                    self.Emit(Opcode.JAL,0,0,0,block)

            elif op[0]=='store':
                size=util.GetIRAllocSize(op[1])
                if size==0:
                    allocator.addUnit(op[4])
                    continue
                pos=allocator.allocate(op[2])
                dest=allocator.allocate(op[4])
                r1=self.PutInReg(dest,1)
                if size<=4:#no need to call the internal.memcpy function when load size<=4
                    self.Store(pos,r1)
                else:
                    self.LoadStackOffset(pos.id,0,True) if pos.id>=0 else self.LoadStackOffset(-pos.id,0,False)#must be on stack
                    self.LoadConst(size,2)
                    self.Emit(Opcode.JAL,util.regMap['t6'],0,0,"internal.memcpy")


            elif op[0]=='unreachable':#nothing happens
                pass

            elif op[0]=='call':#void call
                funcName=op[2][1:-1]
                paramList=[]
                for i in range(3,len(op)-1,2):
                    size=util.GetIRAllocSize(op[i])
                    name=op[i+1]
                    paramList.append((size,name))
                self.Call(function,funcName,paramList)

            elif op[0]=='ret':
                retsize=util.GetIRAllocSize(op[1])
                retval=allocator.allocate(op[2])
                if retsize==4:#pass with a0
                    self.Mov(Position(reg=True,id=util.regMap['a0']),retval)
                elif retsize>4:
                    self.LoadStackOffset(retval.id,0,True) if retval.id>=0 else self.LoadStackOffset(-retval.id,0,False)#must be allocated on stack
                    self.LoadStackOffset(8,1,False)
                    self.LoadConst(retsize,2)
                    self.Emit(Opcode.JAL,util.regMap['t6'],0,0,"internal.memcpy")
                self.Emit(Opcode.JAL,0,0,0,f"{identifier}.return")#return block
                    

            elif op[0].endswith(":"):#block start
                block=identifier+'.'+op[0][:-1]
                self.Emit(Opcode.BLOCK,0,0,0,block)

        ra=util.regMap['ra']
        sp=util.regMap['sp']
        gp=util.regMap['gp']
        prev_ops=[Op(Opcode.BLOCK,0,0,0,f"{identifier}.real_entry"),Op(Opcode.SW,ra,sp,-4)]
        offset=8+allocator.stk_offset# sp -= 8+final_stk_offset
        framesize=offset
        if offset<=2048:
            prev_ops.append(Op(Opcode.ADDI,sp,sp,-offset))
        else:
            rd=util.regMap['t3']
            if offset%4096>2048:
                prev_ops.append(Op(Opcode.LUI,rd,-((offset>>12)+1)))
                offset=4096-offset%4096
            else:
                prev_ops.append(Op(Opcode.LUI,rd,-(offset>>12)))
                offset=-(offset%4096)
            prev_ops.append(Op(Opcode.ADDI,rd,rd,offset))
            prev_ops.append(Op(Opcode.ADD,sp,sp,rd))
        self.ops=prev_ops+self.ops

        #return
        self.Emit(Opcode.BLOCK,0,0,0,f"{identifier}.return")
        self.Add(sp,framesize)
        self.Emit(Opcode.LW,gp,sp,-8)
        self.Emit(Opcode.LW,ra,sp,-4)
        self.Emit(Opcode.JALR,0,ra,0)



    def Write(self,function:Function,f):#Output
        for op in function.ops:
            if op.opcode==Opcode.ADD:
                f.write(util.prune1(f"add x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.SUB:
                f.write(util.prune1(f"sub x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.AND:
                f.write(util.prune1(f"and x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.OR:
                f.write(util.prune1(f"or x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.XOR:
                f.write(util.prune1(f"xor x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.SLL:
                f.write(util.prune1(f"sll x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.SRL:
                f.write(util.prune1(f"srl x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.SRA:
                f.write(util.prune1(f"sra x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.SLT:
                f.write(util.prune1(f"slt x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.SLTU:
                f.write(util.prune1(f"sltu x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.MUL:
                f.write(util.prune1(f"mul x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.DIV:
                f.write(util.prune1(f"div x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.DIVU:
                f.write(util.prune1(f"divu x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.DIV:
                f.write(util.prune1(f"div x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.REM:
                f.write(util.prune1(f"rem x{op.rd}, x{op.r1}, x{op.r2}"))            
            elif op.opcode==Opcode.REMU:
                f.write(util.prune1(f"remu x{op.rd}, x{op.r1}, x{op.r2}"))
            elif op.opcode==Opcode.ADDI:
                f.write(util.prune1(f"addi x{op.rd}, x{op.r1}, {op.r2}"))
            elif op.opcode==Opcode.ANDI:
                f.write(util.prune1(f"andi x{op.rd}, x{op.r1}, {op.r2}"))
            elif op.opcode==Opcode.ORI:
                f.write(util.prune1(f"ori x{op.rd}, x{op.r1}, {op.r2}"))
            elif op.opcode==Opcode.XORI:
                f.write(util.prune1(f"xori x{op.rd}, x{op.r1}, {op.r2}"))
            elif op.opcode==Opcode.SLLI:
                f.write(util.prune1(f"slli x{op.rd}, x{op.r1}, {op.r2}"))
            elif op.opcode==Opcode.SRLI:
                f.write(util.prune1(f"srli x{op.rd}, x{op.r1}, {op.r2}"))
            elif op.opcode==Opcode.SRAI:
                f.write(util.prune1(f"srai x{op.rd}, x{op.r1}, {op.r2}"))
            elif op.opcode==Opcode.SLTI:
                f.write(util.prune1(f"slti x{op.rd}, x{op.r1}, {op.r2}"))
            elif op.opcode==Opcode.SLTIU:
                f.write(util.prune1(f"sltiu x{op.rd}, x{op.r1}, {op.r2}"))
            elif op.opcode==Opcode.LW:
                f.write(util.prune1(f"lw x{op.rd}, {op.r2}(x{op.r1})"))
            elif op.opcode==Opcode.SW:
                f.write(util.prune1(f"sw x{op.rd}, {op.r2}(x{op.r1})"))
            elif op.opcode==Opcode.BNE:
                f.write(util.prune1(f"bne x{op.r1}, x{op.r2}, {op.label}"))
            elif op.opcode==Opcode.JAL:
                f.write(util.prune1(f"jal x{op.rd}, {op.label}"))
            elif op.opcode==Opcode.JALR:
                f.write(util.prune1(f"jalr x{op.rd}, {op.r2}(x{op.r1})"))
            elif op.opcode==Opcode.LUI:
                f.write(util.prune1(f"lui x{op.rd}, {op.r1}"))
            elif op.opcode==Opcode.BLOCK:
                f.write(f"{op.label}:\n")

 


    
    def Generate(self):
        #register parameters
        for function in self.functions:
            self.Register(function)

        for function in self.functions:
            if function.identifier in self.reservedFunctionName:
                continue
            self.ops=[]
            self.Parse(function)
            self.gen.append(Function(identifier=function.identifier,ops=self.ops))
        memcpy='''internal.memcpy:\n    lw a1, 0(t3)\n    sw a1, 0(t4)\n    addi t3, t3, 4\n    addi t4, t4, 4\n    addi t5, t5, -4\n    beq t5, x0, internal.memcpy.ret\n    jal x0, internal.memcpy\ninternal.memcpy.ret:\n    jalr x0, 0(t6)\n'''
        #t3 for src, t4 for dest, t5 for size, t6 for ret_addr

        #output
        with open("prefix.in","r") as f:
            prefix=f.read()
        with open(self.output,"w") as f:
            f.write(prefix)
            for each in self.gen:
                self.Write(each,f)
            f.write(memcpy)