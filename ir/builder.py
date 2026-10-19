from __future__ import annotations
from dataclasses import dataclass,field
from frontend.generated import ast_nodes
from semantic.scope import *
from semantic.checker import Checker
from ir.model import *

class Builder:
    assignmentOps=["+=","-=",">>=","<<=","/=","%=","*=","=","&=","|=","^="]
    comparisonOps=[">","<","==","!=","<=",">="]
    logicOps=["and","or"]
    arithmeticOps=["+","-","*","/",'%',"<<",">>",'@',"|","^"]#@ for &
    unaryOps=['minus','star','!','&','&mut']
    
    basicTypes=['i32','u32','usize','isize','bool']
    integers=['i32','u32','usize','isize']
    def __init__(self,checker:Checker,output:str):
        self.StructDefinitions={}#structName(str)->IRStruct
        self.FunctionDefinitions={}#functionName(str)->IRFunction
        self.FunctionNewNames={}#functionName in checker->functionName in IR
        self.CloneFunctions=[]#built specially for struct clone functions
        self.EqualFunctions=[]#built specially for struct equal functions
        self.checker=checker#already done SemanticCheck
        self.output=output#output_path
        self.tempctr=0
        self.varctr=0
        self.funcctr=0
        self.blockctr=0
        self.block=""
    def beautify(self,s:str)->str:
        lines=s.split('\n')
        t=''
        flag=0
        for i in range(len(lines)):
            lines[i]=lines[i].strip()
            if lines[i].endswith(":"):
                flag=0
                t+=(f'    br label %{lines[i][:-1]}\n' if (not lines[i].startswith('entry') and not lines[i-1].startswith('br')) else '')+lines[i]+'\n'
            elif lines[i].startswith("define") or lines[i].startswith("{") or lines[i].startswith("}"):
                t+=lines[i]+'\n'
            else:
                if flag==0:
                    t+='    '+lines[i]+'\n'
                if lines[i].startswith('ret'):
                    flag=1
        return t
    
    def GenTempName(self)->str:#generate a temporary variable
        self.tempctr+=1
        return f"%temp{self.tempctr}"
    
    def GenVarName(self)->str:#generate a local variable
        self.varctr+=1
        return f"%var{self.varctr}"

    def GenBlockName(self)->str:#generate a local variable
        self.blockctr+=1
        return f"block{self.blockctr}"
    
    def GetIRType(self,type:str)->str:#replace all &mut with &
        return type.replace('&mut','&')

    def GetArrayInfo(self,type:str)->tuple[str,int]:#array innerType and length
        idx=len(type)-1
        while type[idx]!=';':
            idx-=1
        return self.GetIRType(type[1:idx]),int(type[idx+1:-1])

    def GenUnit(self)->IRType:
        res=self.GenTempName()
        self.block+=f"    {res} = freeze %Internal.Unit zeroinitializer\n"
        return IRType(type="()",identifier=res)
    
    def GetAllocSize(self,type:str)->int:
        if type.startswith("&") or type.startswith("Box<"):
            return 4
        elif type.startswith("Vec<"):
            return 12
        elif type=="()":
            return 0
        elif type in ["i32","u32","isize","usize"]:
            return 4
        elif type=="bool":
            return 1
        elif type=='^':
            return 0
        elif type.startswith("["):
            innerType,length=self.GetArrayInfo(type)
            return length*self.GetAllocSize(innerType)
        else:
            return self.StructDefinitions[type].size
        
    def GetAllocType(self,type:str)->str:
        if type.startswith("&") or type.startswith("Box<"):
            return "ptr"
        elif type.startswith("Vec<"):
            return "%Vec"
        elif type=="()":
            return "%Internal.Unit"
        elif type in ["i32","u32","isize","usize"]:
            return "i32"
        elif type=="bool":
            return "i1"
        elif type=='^':
            return type
        elif type.startswith("["):
            innerType,length=self.GetArrayInfo(type)
            return f"[{length} x {self.GetAllocType(innerType)}]"
        else:
            return "%"+type

    def Dereference(self,type:IRType,cnt=1)->tuple[str,str]:#return s,tempname
        s=""
        last=type.identifier
        lasttype=type.type
        for _ in range(cnt):
            temp=self.GenTempName()
            lasttype=lasttype[2:] if lasttype.startswith("& ") else lasttype[4:-1]#Box
            s+=f"   {temp} = load {self.GetAllocType(lasttype)}, ptr {last}\n"
            last=temp
        return s,last
    
    def dereference(self,type:str)->str:#just type operation
        while True:
            if type.startswith("& "):
                type=type[2:]
            elif type.startswith("Box<"):
                type=type[4:-1]
            else:
                break
        return type
    
    def AutoDereference(self,type:IRType,wanted:str=None):#auto derefence type's type to wanted and change's type's identifier, also append s to self.block
        if wanted=='& '+type.type:#special case in self
            type.identifier=type.left
            type.left=None
            type.type=wanted
            return
        while type.type!=wanted:
            temp=self.GenTempName()
            if type.type.startswith("& "):
                type.type=type.type[2:]
            elif type.type.startswith("Box<"):
                type.type=type.type[4:-1]
            else:
                return
            self.block+=f"   {temp} = load {self.GetAllocType(type.type)}, ptr {type.identifier}\n"
            if wanted=='& '+type.type:#special case in self
                type.type=wanted
                return
            type.left=type.identifier
            type.identifier=temp

    def BuildAndStore(self,var1:str,var2:str,type:str)->str:#store var2's value into var1
        alloc_type=self.GetAllocType(type)
        return f"   {var1} = alloca {alloc_type}\n   store {alloc_type} {var2}, ptr {var1}\n"#statement format: Tab{statement}\n
    
    def Store(self,var1:str,var2:str,type:str)->str:#store var2's value into var1
        return f"   store {self.GetAllocType(type)} {var2}, ptr {var1}\n"

    def Calc(self,type1:IRType,type2:IRType,op:str,block_name:str):#return IRType,block_name
        temp=""
        if op in self.assignmentOps:
            if op!="=":
                temp=self.GenTempName()
                self.AutoDereference(type2)
                if op in ["+=","-=","*=","<<="]:
                    self.block+=f"   {temp} = {["add","sub","mul","shl"][["+=","-=","*=","<<="].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
                elif op in ["/=","%=",">>="]:
                    if type1.type in ['i32','isize']:#i
                        self.block+=f"   {temp} = {["sdiv","srem","ashr"][["/=","%=",">>="].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
                    else:#u
                        self.block+=f"   {temp} = {["udiv","urem","lshr"][["/=","%=",">>="].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
                elif op in ["&=","|=","^="]:
                    if type1.type=='bool':#i1
                        self.block+=f"   {temp} = {["and","or","xor"][["&=","|=","^="].index(op)]} i1 {type1.identifier}, {type2.identifier}\n"
                    else:#i32
                        self.block+=f"   {temp} = {["and","or","xor"][["&=","|=","^="].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"      
                self.block+=self.Move(IRType(type=type1.type,identifier=temp),type1.left)
            else:#=
                self.AutoDereference(type2,type1.type)
                self.block+=self.Move(type2,type1.left)
            res=self.GenTempName()
            self.block+=f'    {res} = freeze %Internal.Unit zeroinitializer\n'
            return IRType(type="()",identifier=res),block_name
        
        elif op in self.comparisonOps:
            temp=self.GenTempName()
            if op in ['==','!=']:#compare function needed!
                s,block_name=self.Equal(type1,type2,temp,block_name)
                self.block+=s
                if op=='==':
                    return IRType(type='bool',identifier=temp),block_name
                else:
                    res=self.GenTempName()
                    self.block+=f'   {res} = xor i1 {temp}, true\n'
                    return IRType(type='bool',identifier=res),block_name
            
            elif op in [">","<","<=",">="]:
                self.AutoDereference(type1)
                self.AutoDereference(type2)
                if type1.type in ["i32","isize"]:
                    self.block+=f"   {temp} = icmp {["sgt","slt","sle","sge"][[">","<","<=",">="].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
                elif type1.type in ["u32","usize"]:
                    self.block+=f"   {temp} = icmp {["ugt","ult","ule","uge"][[">","<","<=",">="].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
                else:#bool
                    self.block+=f"   {temp} = icmp {["ugt","ult","ule","uge"][[">","<","<=",">="].index(op)]} i1 {type1.identifier}, {type2.identifier}\n"
                
            return IRType(type="bool",identifier=temp),block_name

        elif op in self.logicOps:
            temp=self.GenTempName()
            self.block+=f"   {temp} = {op} i1 {type1.identifier}, {type2.identifier}\n"
            return IRType(type="bool",identifier=temp),block_name

        elif op in self.arithmeticOps:
            temp=self.GenTempName()
            self.AutoDereference(type1)
            self.AutoDereference(type2)
            if op in ["+","-","*","<<"]:
                self.block+=f"   {temp} = {["add","sub","mul","shl"][["+","-","*","<<"].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
            elif op in ["/","%",">>"]:
                if type1.type in ['i32','isize']:#i
                    self.block+=f"   {temp} = {["sdiv","srem","ashr"][["/","%",">>"].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
                else:#u
                    self.block+=f"   {temp} = {["udiv","urem","lshr"][["/","%",">>"].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
            elif op in ["@","|","^"]:
                self.block+=f"   {temp} = {["and","or","xor"][["@","|","^"].index(op)]} {'i1' if type1.type=='bool' else 'i32'} {type1.identifier}, {type2.identifier}\n"

            return IRType(type=type1.type,identifier=temp),block_name
        
        elif op in self.unaryOps:#type2=None
            if op=='minus':
                temp=self.GenTempName()
                self.AutoDereference(type1)
                self.block+=f"    {temp} = sub i32 0, {type1.identifier}\n"
                return IRType(type=type1.type,identifier=temp),block_name
            elif op=='!':
                temp=self.GenTempName()
                self.AutoDereference(type1)
                self.block+=(f"    {temp} = xor i1 {type1.identifier}, true\n") if type1.type=="bool" else (f"    {temp} = xor i32 {type1.identifier}, -1\n")
                return IRType(type=type1.type,identifier=temp),block_name
            elif op=="star":
                s,temp=self.Dereference(type1)
                self.block+=s
                return IRType(type=type1.type[2:] if type1.type.startswith("& ") else type1.type[4:-1],identifier=temp,left=type1.identifier),block_name
            else:#&
                if type1.left:
                    return IRType(type="& "+type1.type,identifier=type1.left),block_name
                temp=self.GenTempName()
                self.block+=self.BuildAndStore(temp,type1.identifier,type1.type)
                return IRType(type="& "+type1.type,identifier=temp),block_name

    def Equal(self,type1:IRType,type2:IRType,res:str,block_name:str)->tuple[str,str]:#res is the value that stores the answer
        if type1.type=="()":#nothing should happen
            return f'   {res} = freeze i1,true\n',block_name
        elif type1.type in self.basicTypes:
            return f"   {res} = icmp eq {self.GetAllocType(type1.type)} {type1.identifier}, {type2.identifier}\n",block_name
        elif type1.type.startswith("& ") or type1.type.startswith("Box<"):
            innerType=type1.type[2:] if type1.type.startswith('& ') else type1.type[4:-1]
            t1=self.GenTempName()
            t2=self.GenTempName()
            alloc_type=self.GetAllocType(innerType)
            s=f'''{t1} = load {alloc_type}, ptr {type1.identifier}
                {t2} = load {alloc_type}, ptr {type2.identifier}\n'''
            news,block_name=self.Equal(IRType(type=innerType,identifier=t1,left=type1.identifier),IRType(type=innerType,identifier=t2,left=type2.identifier),res,block_name)
            return s+news,block_name
        elif type1.type.startswith("["):
            innerType,length=self.GetArrayInfo(type1.type)
            alloc_type=self.GetAllocType(innerType)
            ctr=self.GenTempName()
            s1=self.GenTempName()
            s2=self.GenTempName()
            t1=self.GenTempName()
            t2=self.GenTempName()
            temp=self.GenTempName()
            temp1=self.GenTempName()
            temp2=self.GenTempName()
            condition=self.GenTempName()
            val=self.GenTempName()

            loop_block=self.GenBlockName()
            condition_block=self.GenBlockName()
            fail_block=self.GenBlockName()
            win_block=self.GenBlockName()
            s=f'''    {ctr} = alloca i32
                store i32 0, ptr {ctr}
                {temp} = alloca i1
                store i1 true, ptr {temp}
            {loop_block}:
                {temp1} = load i32, ptr {ctr}
                {s1} = getelementptr [{length} x {alloc_type}], ptr {type1.left}, i32 0, i32 {temp1}
                {t1} = load {alloc_type}, ptr {s1}
                {s2} = getelementptr [{length} x {alloc_type}], ptr {type2.left}, i32 0, i32 {temp1}
                {t2} = load {alloc_type}, ptr {s2}\n'''
            news,_=self.Equal(IRType(type=innerType,identifier=t1,left=s1),IRType(type=innerType,identifier=t2,left=s2),val,block_name)
            s+=news 
            s+=f'''{temp2} = add i32 {temp1}, 1
                store i32 {temp2}, ptr {ctr}
                br i1 {val}, label %{condition_block}, label %{fail_block}
            {condition_block}:
                {condition} = icmp ne i32 {temp2}, {length}
                br i1 {condition}, label %{loop_block},label %{win_block}
            {fail_block}:
                store i1 false, ptr {temp}
            {win_block}:
                {res} = load i1, ptr {temp}\n'''     
            return s,win_block
        elif type1.type.startswith("Vec<"):
            innerType=type1.type[4:-1]
            cond1=self.GenTempName()
            temp=self.GenTempName()
            temp1=self.GenTempName()
            temp2=self.GenTempName()

            val=self.GenTempName()
            length1=self.GenTempName()
            length2=self.GenTempName()
            zero_length=self.GenTempName()
            p1=self.GenTempName()
            p2=self.GenTempName()
            s1=self.GenTempName()
            s2=self.GenTempName()
            t1=self.GenTempName()
            t2=self.GenTempName()
            condition=self.GenTempName()

            next_block=self.GenBlockName()
            loop_block=self.GenBlockName()
            condition_block=self.GenBlockName()
            fail_block=self.GenBlockName()
            win_block=self.GenBlockName()

            ctr=self.GenTempName()
            alloc_type=self.GetAllocType(innerType)
            s=f'''
                {temp} = alloca i1
                store i1 true, ptr {temp}
                {length1} = extractvalue %Vec {type1.identifier}, 0
                {length2} = extractvalue %Vec {type2.identifier}, 0
                {cond1} = icmp eq i32 {length1}, {length2}
                br i1 {cond1}, label %{next_block}, label %{fail_block}
            {next_block}:
                {p1} = extractvalue %Vec {type1.identifier}, 2
                {p2} = extractvalue %Vec {type2.identifier}, 2
                {ctr} = alloca i32
                store i32 0, ptr {ctr}
                {zero_length} = icmp eq i32 {length1}, 0
                br i1 {zero_length}, label %{win_block}, label %{loop_block}
            {loop_block}:
                {temp1} = load i32, ptr {ctr}
                {s1} = getelementptr {alloc_type}, ptr {p1},i32 {temp1}
                {t1} = load {alloc_type}, ptr {s1}
                {s2} = getelementptr {alloc_type}, ptr {p2},i32 {temp1}
                {t2} = load {alloc_type}, ptr {s2}''' 
            news,_=self.Equal(IRType(type=innerType,identifier=t1,left=s1),IRType(type=innerType,identifier=t2,left=s2),val,block_name)
            s+=news 
            s+=f'''{temp2} = add i32 {temp1}, 1
                store i32 {temp2}, ptr {ctr}
                br i1 {val}, label %{condition_block}, label %{fail_block}
            {condition_block}:
                {condition} = icmp ne i32 {temp2}, {length1}
                br i1 {condition}, label %{loop_block},label %{win_block}
            {fail_block}:
                store i1 false, ptr {temp}
            {win_block}:
                {res} = load i1, ptr {temp}\n'''     
            return s,win_block
        else:#struct
            s=f'    {res} = call i1 @Equal{type1.type}(ptr {type1.left}, ptr {type2.left})\n'
            return s,block_name

        
    def Clone(self,type:IRType,res:str,block_name:str)->tuple[str,str]:#clone struct to res(ptr,already alloced),return s,block_name
        s=""
        if type.type=="()":#nothing should happen
            return s,block_name
        elif type.type in self.basicTypes or type.type.startswith("& "):
            return f"store {self.GetAllocType(type.type)} {type.identifier}, ptr {res}\n",block_name
        elif type.type.startswith("Box<"):
            innerType=type.type[4:-1]
            dest=self.GenTempName()
            src=self.GenTempName()
            alloc_type=self.GetAllocType(innerType)
            alloc_size=self.GetAllocSize(innerType)
            s=f'''{src} = load {alloc_type}, ptr {type.identifier}
                {dest} = call ptr @__rx_alloc(i32 {alloc_size}, i32 4)\n'''
            news,block_name=self.Clone(IRType(type=innerType,identifier=src,left=type.identifier),dest,block_name)
            return s+news+f"    store ptr {dest}, ptr {res}\n",block_name
        elif type.type.startswith("["):
            innerType,length=self.GetArrayInfo(type.type)
            alloc_type=self.GetAllocType(innerType)
            loop_block=self.GenBlockName()
            ctr=self.GenTempName()
            source=self.GenTempName()
            src=self.GenTempName()
            dest=self.GenTempName()
            temp1=self.GenTempName()
            temp2=self.GenTempName()
            condition=self.GenTempName()
            s+=f'''    {ctr} = alloca i32
                store i32 0, ptr {ctr}
            {loop_block}:
                {temp1} = load i32, ptr {ctr}
                {source} = getelementptr [{length} x {alloc_type}], ptr {type.left}, i32 0, i32 {temp1}
                {src} = load {alloc_type}, ptr {source}
                {dest} = getelementptr [{length} x {alloc_type}], ptr {res}, i32 0, i32 {temp1}\n'''    
            news,_=self.Clone(IRType(type=innerType,identifier=src,left=source),dest,block_name)
            s+=news 
            new_block_name=self.GenBlockName()
            s+=f'''{temp2} = add i32 {temp1}, 1
                store i32 {temp2}, ptr {ctr}
                {condition} = icmp ne i32 {temp2}, {length}
                br i1 {condition}, label %{loop_block},label %{new_block_name}
            {new_block_name}:\n'''     
            return s,new_block_name 
        elif type.type.startswith("Vec<"):
            innerType=type.type[4:-1]
            temp=self.GenTempName()
            temp1=self.GenTempName()
            temp2=self.GenTempName()

            length=self.GenTempName()
            zero_length=self.GenTempName()
            length_ptr=self.GenTempName()
            src=self.GenTempName()
            dest=self.GenTempName()
            cap=self.GenTempName()
            cap_ptr=self.GenTempName()
            pointer=self.GenTempName()
            size=self.GenTempName()
            new_res=self.GenTempName()
            source=self.GenTempName()
            condition=self.GenTempName()


            loop_block=self.GenBlockName()
            new_block=self.GenBlockName()
            ctr=self.GenTempName()
            alloc_type=self.GetAllocType(innerType)
            alloc_size=self.GetAllocSize(innerType)
            s+=f'''
                {length} = extractvalue %Vec {type.identifier}, 0
                {cap} = extractvalue %Vec {type.identifier}, 1
                {pointer} = extractvalue %Vec {type.identifier}, 2
                {length_ptr} = getelementptr %Vec, ptr {res}, i32 0, i32 0
                {cap_ptr} = getelementptr %Vec, ptr {res}, i32 0, i32 1
                store i32 {length}, ptr {length_ptr}
                store i32 {cap}, ptr {cap_ptr}
                {temp} = getelementptr %Vec, ptr {res}, i32 0, i32 2
                {size} = mul i32 {cap}, {alloc_size}
                {new_res} = call ptr @__rx_alloc(i32 {size}, i32 4)
                store ptr {new_res}, ptr {temp}
                {ctr} = alloca i32
                store i32 0, ptr {ctr}
                {zero_length} = icmp eq i32 {length}, 0
                br i1 {zero_length}, label %{new_block}, label %{loop_block}
            {loop_block}:
                {temp1} = load i32, ptr {ctr}
                {source} = getelementptr {alloc_type}, ptr {pointer},i32 {temp1}
                {src} = load {alloc_type}, ptr {source}
                {dest} = getelementptr {alloc_type}, ptr {new_res}, i32 {temp1}\n'''    
            news,_=self.Clone(IRType(type=innerType,identifier=src,left=source),dest,block_name)
            s+=news
            s+=f'''{temp2} = add i32 {temp1}, 1
                    store i32 {temp2}, ptr {ctr}
                    {condition} = icmp ne i32 {temp2}, {length}
                    br i1 {condition}, label %{loop_block},label %{new_block}
                {new_block}:\n'''  
            return s,new_block
        else:#struct
            temp=self.GenTempName()
            s=f'    {temp} = call %{type.type} @Clone{type.type}(ptr {type.left})\n  store %{type.type} {temp}, ptr {res}\n'
            return s,block_name

    def Move(self,type:IRType,res:str)->str:#move struct to res(ptr,already alloced),return s,block_name
        if type.type=="()":#nothing should happen
            return ""
        else:
            return f"    store {self.GetAllocType(type.type)} {type.identifier}, ptr {res}\n"
        
    def VecOp(self,innerType:str,func_name:str,block_name:str,args:list[IRType])->tuple[str,IRType,str]:#return s,Type,block_name,args[0].type is &Vec
        temp=self.GenTempName()
        if func_name=="len":
            temp1=self.GenTempName()
            s=f"   {temp1} = getelementptr %Vec, ptr {args[0].identifier}, i32 0, i32 0\n    {temp} = load i32, ptr {temp1}\n"
            return s,IRType(type="usize",identifier=temp),block_name
        elif func_name=="is_empty":
            temp1=self.GenTempName()
            temp2=self.GenTempName()
            s=f"   {temp1} = getelementptr %Vec, ptr {args[0].identifier}, i32 0, i32 0\n    {temp2} = load i32, ptr {temp1}\n   {temp} = icmp eq i32 {temp2},0\n"
            return s,IRType(type="bool",identifier=temp),block_name
        elif func_name=="new":
            alloc_type=self.GetAllocType(innerType)
            alloc_size=self.GetAllocSize(innerType)
            res=self.GenTempName()
            ptr=self.GenTempName()
            length_ptr=self.GenTempName()
            cap_ptr=self.GenTempName()
            pointer=self.GenTempName()
            s=f'''  {temp} = alloca %Vec
                {ptr} = call ptr @__rx_alloc(i32 {alloc_size*2}, i32 4)
                {length_ptr} = getelementptr %Vec, ptr {temp}, i32 0, i32 0
                store i32 0, ptr {length_ptr}
                {cap_ptr} = getelementptr %Vec, ptr {temp}, i32 0, i32 1
                store i32 2, ptr {cap_ptr}
                {pointer} = getelementptr %Vec, ptr {temp}, i32 0, i32 2
                store ptr {ptr}, ptr {pointer}
                {res} = load %Vec, ptr {temp}\n'''
            return s,IRType(type=f"Vec<{innerType}>",identifier=res,left=temp),block_name
        elif func_name=="push":
            length_ptr=self.GenTempName()
            cap_ptr=self.GenTempName()
            pointer_ptr=self.GenTempName()
            length=self.GenTempName()
            cap=self.GenTempName()
            size=self.GenTempName()
            pointer=self.GenTempName()

            if_full=self.GenTempName()
            cap2=self.GenTempName()
            new_pointer=self.GenTempName()
            new_length=self.GenTempName()

            ctr=self.GenTempName()
            temp=self.GenTempName()
            temp1=self.GenTempName()
            temp2=self.GenTempName()
            source=self.GenTempName()
            src=self.GenTempName()
            dest=self.GenTempName()
            condition=self.GenTempName()

            alloc_type=self.GetAllocType(innerType)
            alloc_size=self.GetAllocSize(innerType)
            if_block=self.GenBlockName()
            else_block=self.GenBlockName()
            loop_block=self.GenBlockName()
            s=f'''   {length_ptr} = getelementptr %Vec, ptr {args[0].identifier}, i32 0, i32 0   
                {length} = load i32, ptr {length_ptr}
                {new_length} = add i32 {length},1
                store i32 {new_length}, ptr {length_ptr}
                {cap_ptr} = getelementptr %Vec, ptr {args[0].identifier}, i32 0, i32 1   
                {cap} = load i32, ptr {cap_ptr}
                {pointer_ptr} = getelementptr %Vec, ptr {args[0].identifier}, i32 0, i32 2   
                {pointer} = load ptr, ptr {pointer_ptr}
                {if_full} = icmp eq i32 {length}, {cap}
                br i1 {if_full}, label %{if_block}, label %{else_block}
            {if_block}:
                {cap2} =  add i32 {cap}, {cap}
                {size} = mul i32 {cap2}, {alloc_size}
                {new_pointer} = call ptr @__rx_alloc(i32 {size}, i32 4)
                store ptr {new_pointer}, ptr {pointer_ptr}
                store i32 {cap2}, ptr {cap_ptr}
                {ctr} = alloca i32
                store i32 0, ptr {ctr}
            {loop_block}:
                {temp1} = load i32, ptr {ctr}
                {source} = getelementptr {alloc_type}, ptr {pointer}, i32 {temp1}
                {src} = load {alloc_type}, ptr {source}
                {dest} = getelementptr {alloc_type}, ptr {new_pointer}, i32 {temp1}\n'''    
            s+=self.Move(IRType(type=innerType,identifier=src),dest)

            newdest=self.GenTempName()
            truepointer=self.GenTempName()
            s+=f'''    {temp2} = add i32 {temp1}, 1
                store i32 {temp2}, ptr {ctr}
                {condition} = icmp ne i32 {temp2}, {length}
                br i1 {condition}, label %{loop_block},label %{else_block}
            {else_block}:
                {truepointer} = load ptr, ptr {pointer_ptr}
                {newdest} = getelementptr {alloc_type}, ptr {truepointer}, i32 {length}
            '''
            s+=self.Move(IRType(type=innerType,identifier=args[-1].identifier),newdest)
            s+=f'    {temp} = freeze %Internal.Unit zeroinitializer\n'
            return s,IRType(type="()",identifier=temp),else_block
        elif func_name=="remove":
            length_ptr=self.GenTempName()
            pointer_ptr=self.GenTempName()
            ans_ptr=self.GenTempName()
            left=self.GenTempName()
            length=self.GenTempName()
            new_length=self.GenTempName()
            pointer=self.GenTempName()
            ans=self.GenTempName()
            
            ctr=self.GenTempName()
            idx_1=self.GenTempName()
            idx=self.GenTempName()
            temp2=self.GenTempName()
            source=self.GenTempName()
            src=self.GenTempName()
            dest=self.GenTempName()
            cond=self.GenTempName()
            condition=self.GenTempName()

            alloc_type=self.GetAllocType(innerType)
            prep_block=self.GenBlockName()
            loop_block=self.GenBlockName()
            if_block=self.GenBlockName()
            new_block=self.GenBlockName()
            s=f'''  {length_ptr} = getelementptr %Vec, ptr {args[0].identifier}, i32 0, i32 0   
                {length} = load i32, ptr {length_ptr}
                {new_length} = sub i32 {length},1
                store i32 {new_length}, ptr {length_ptr}
                {pointer_ptr} = getelementptr %Vec, ptr {args[0].identifier}, i32 0, i32 2   
                {pointer} = load ptr, ptr {pointer_ptr}
                {ans_ptr} = getelementptr {alloc_type}, ptr {pointer}, i32 {args[-1].identifier}
                {ans} = load {alloc_type}, ptr {ans_ptr}
                {cond} = icmp eq i32 {new_length}, {args[-1].identifier}
                br i1 {cond}, label %{new_block}, label %{prep_block}
            {prep_block}:
                {ctr} = alloca i32
                store i32 {args[-1].identifier}, ptr {ctr}
            {loop_block}:
                {idx} = load i32, ptr {ctr}
                {idx_1} = add i32 {idx}, 1
                store i32 {idx_1}, ptr {ctr}\n
                {source} = getelementptr {alloc_type}, ptr {pointer}, i32 {idx_1}
                {src} = load {alloc_type}, ptr {source}
                {dest} = getelementptr {alloc_type}, ptr {pointer}, i32 {idx}\n'''    
            s+=self.Move(IRType(type=innerType,identifier=src),dest)
            s+=f'''    {condition} = icmp eq i32 {idx_1}, {new_length}
                br i1 {condition}, label %{new_block}, label %{loop_block}
            {new_block}:\n
                {left} = alloca {alloc_type}
                store {alloc_type} {ans}, ptr {left}\n'''
            return s,IRType(type=innerType,identifier=ans,left=left),new_block
        else:#clone
            res=self.GenTempName()
            val=self.GenTempName()
            src=self.GenTempName()
            s=f'''{res} = alloca %Vec
                {src} = load %Vec, ptr {args[0].identifier}\n'''
            news,block_name=self.Clone(IRType(type=f"Vec<{innerType}>",identifier=src),res,block_name)
            return s+news+f'    {val} = load %Vec, ptr {res}\n',IRType(type=f"Vec<{innerType}>",identifier=val,left=res),block_name


    def BoxOp(self,innerType:str,func_name:str,block_name:str,arg:IRType):#return s,Type,block_name                    
        if func_name=="new":
            res=self.GenTempName()
            val=self.GenTempName()
            alloc_type=self.GetAllocType(innerType)
            alloc_size=self.GetAllocSize(innerType)
            s=f'''  {res} = alloca ptr
                {val} = call ptr @__rx_alloc(i32 {alloc_size}, i32 4)
                store {alloc_type} {arg.identifier}, ptr {val}
                store ptr {val}, ptr {res}\n'''
            return s,IRType(type=f"Box<{innerType}>",identifier=val,left=res),block_name
        else:#clone     
            res=self.GenTempName()
            val=self.GenTempName()
            src=self.GenTempName()
            s=f'''{res} = alloca ptr
            {src} = load ptr, ptr {arg.identifier}\n'''
            news,block_name=self.Clone(IRType(type=f"Box<{innerType}>",identifier=src),res,block_name)
            return s+news+f'    {val} = load ptr, ptr {res}\n',IRType(type=f"Box<{innerType}>",identifier=val,left=res),block_name         
                        
    def CallFunction(self,funcName:str,args:list[ast_nodes.Expression],block_name:str)-> tuple[IRType,str]:
        if funcName.startswith("Vec<"):#vec
            innerType=self.GetIRType(funcName[4:funcName.index("::")-1])
            funcName=funcName[funcName.index("::")+2:]
            if funcName!="new":
                self.AutoDereference(args[0],f"& Vec<{innerType}>")
            if funcName in ["push","remove"]:
                self.AutoDereference(args[-1],innerType if funcName=="push" else "usize")
            s,type,block_name=self.VecOp(innerType,funcName,block_name,args)
            self.block+=s
            return type,block_name
        elif funcName.startswith("Box<"):
            innerType=self.GetIRType(funcName[4:funcName.index("::")-1])
            funcName=funcName[funcName.index("::")+2:]
            if funcName=="clone":
                self.AutoDereference(args[0],f"& Box<{innerType}>")
            else:#new
                self.AutoDereference(args[0],innerType)
            s,type,block_name=self.BoxOp(innerType,funcName,block_name,args[0])
            self.block+=s
            return type,block_name
        else:            
            if funcName.count("::")==1 and funcName[funcName.index("::")+2:]=="clone" and not self.FunctionNewNames.get(funcName):#if defined clone, use the user-defined clone
                struct=funcName[:funcName.index("::")]
                self.AutoDereference(args[0],'& '+struct)
                res=self.GenTempName()
                val=self.GenTempName()
                src=self.GenTempName()
                s=f'''  {res} = alloca %{struct}
                    {src} = load %{struct}, ptr {args[0].identifier}\n'''
                news,block_name=self.Clone(IRType(type=struct,identifier=src),res,block_name)
                self.block+=s+news+f'   {val} = load %{struct}, ptr {res}\n'
                return IRType(type=struct,identifier=val,left=res),block_name     
            else:
                newname=self.FunctionNewNames[funcName]
                func=self.FunctionDefinitions.get(newname)
                s=""
                for i in range(len(args)):
                    self.AutoDereference(args[i],func.param_types[i])
                for i in range(len(args)):
                    s+=f"{self.GetAllocType(args[i].type)} {args[i].identifier}"
                    if i!=len(args)-1:
                        s+=", "
                temp=self.GenTempName()
                if func.retType!="()":
                    ptr=self.GenTempName()
                    alloc_type=self.GetAllocType(func.retType)
                    self.block+=f'''    {ptr} = alloca {alloc_type}\n   {temp} =  call {alloc_type} @{newname}({s})\n  store {alloc_type} {temp}, ptr {ptr}\n'''
                    return IRType(type=func.retType,identifier=temp,left=ptr),block_name
                else:
                    self.block+=f'''    call void @{newname}({s})
                        {temp} = freeze %Internal.Unit zeroinitializer\n'''
                    return IRType(type="()",identifier=temp),block_name  

                
    def ParseExpression(self,scope:IRScope,expression:ast_nodes.Expression,block_name:str,break_name:str=None,continue_name:str=None)->tuple[IRType,str]:
        if isinstance(expression,ast_nodes.PrimitiveExpression):
            if expression.op in self.assignmentOps or expression.op in self.comparisonOps:
                type1,block_name=self.ParseExpression(scope,expression.expressions[1],block_name,break_name=break_name,continue_name=continue_name)
                type0,block_name=self.ParseExpression(scope,expression.expressions[0],block_name,break_name=break_name,continue_name=continue_name)
                type,block_name=self.Calc(type0,type1,expression.op,block_name)
                
                return type,block_name
            
            elif expression.op in self.logicOps:#need short-circuit
                temp=self.GenTempName()
                res=self.GenTempName()
                self.block+=f"  {temp} = alloca i1\n    store i1 {'false' if expression.op=='and' else 'true'}, ptr {temp}\n"
                final_block=self.GenBlockName()
                for i in range(len(expression.expressions)):
                    type,block_name=self.ParseExpression(scope,expression.expressions[i],block_name,break_name=break_name,continue_name=continue_name)
                    next_block=self.GenBlockName()
                    if expression.op=='and':
                        self.block+=f'    br i1 {type.identifier},label %{next_block}, label %{final_block}\n{next_block}:\n'
                    else:#or
                        self.block+=f'    br i1 {type.identifier},label %{final_block}, label %{next_block}\n{next_block}:\n'
                    block_name=next_block
                self.block+=f'    store i1 {'true' if expression.op=='and' else 'false'}, ptr {temp}\n{final_block}:\n    {res} = load i1, ptr {temp}\n'
                return IRType(type='bool',identifier=res),final_block
            
            elif expression.op in self.arithmeticOps:
                type0,block_name=self.ParseExpression(scope,expression.expressions[0],block_name,break_name=break_name,continue_name=continue_name)
                for i in range(1,len(expression.expressions)):
                    type1,block_name=self.ParseExpression(scope,expression.expressions[i],block_name,break_name=break_name,continue_name=continue_name)
                    type0,block_name=self.Calc(type0,type1, expression.ops[i-1] if isinstance(expression, ast_nodes.ExtraExpression) else expression.op,block_name)

                return type0,block_name
            
        elif isinstance(expression,ast_nodes.UnaryExpression):
            type0,block_name=self.ParseExpression(scope,expression.postfixExpression,block_name,break_name=break_name,continue_name=continue_name)
            for op in expression.ops[::-1]:
                if op=='&&' or op=="&&mut":
                    type0,block_name=self.Calc(type0,None,"&",block_name)
                    type0,block_name=self.Calc(type0,None,"&",block_name)
                else:
                    type0,block_name=self.Calc(type0,None,op,block_name)
            return type0,block_name

        elif isinstance(expression,ast_nodes.CastExpression):
            type0,block_name=self.ParseExpression(scope,expression.unaryExpression,block_name,break_name=break_name,continue_name=continue_name)
            type1=expression.typeRefs[-1].typePathSegments[0].identifier #must be i32
            if type0.type=="bool":
                temp=self.GenTempName()
                self.block+=f'    {temp} = zext i1 {type0.identifier} to i32\n'
                type0.identifier=temp
            return IRType(type=type1,identifier=type0.identifier),block_name

        elif isinstance(expression,ast_nodes.PostfixExpression):
            type0,block_name=self.ParseExpression(scope,expression.primaryExpression,block_name,break_name=break_name,continue_name=continue_name)
            for suffix in expression.postfixSuffixes:
                if isinstance(suffix,ast_nodes.CallArguments):#need to dereference first!
                    args=[]
                    for expression in suffix.expressions:
                        type,block_name=self.ParseExpression(scope,expression,block_name,break_name=break_name,continue_name=continue_name)
                        if type.type=='^':
                            return IRType(type='^',identifier=None),block_name
                        args.append(type)
                        
                    type0,block_name = self.CallFunction(type0.type[1:],args,block_name)
                    
                elif isinstance(suffix,ast_nodes.BracketSuffix):#arrays should also have left
                    idx,block_name=self.ParseExpression(scope,suffix.expression,block_name,break_name=break_name,continue_name=continue_name)                             
                    if idx.type=='^':
                        return IRType(type='^',identifier=None),block_name
                    self.AutoDereference(type0)
                    res=self.GenTempName()
                    if type0.type.startswith("Vec<"):
                        temp=self.GenTempName()
                        ptr=self.GenTempName()
                        innerType=type0.type[4:-1]
                        alloc_type=self.GetAllocType(innerType)
                        self.block+=f'''    {temp} = extractvalue %Vec {type0.identifier}, 2
                            {ptr} = getelementptr {alloc_type}, ptr {temp}, i32 {idx.identifier}
                            {res} = load {alloc_type}, ptr {ptr}\n'''
                        type0 = IRType(type=innerType,identifier=res,left=ptr)
                    else:
                        ptr=self.GenTempName()
                        innerType,length=self.GetArrayInfo(type0.type)
                        alloc_type=self.GetAllocType(innerType)
                        self.block+=f'''    {ptr} = getelementptr [{length} x {alloc_type}], ptr {type0.left}, i32 0, i32 {idx.identifier}
                            {res} = load {alloc_type}, ptr {ptr}\n'''
                        type0=IRType(type=innerType,identifier=res,left=ptr)
                            
                elif isinstance(suffix,ast_nodes.DotSuffix):
                    if isinstance(suffix,ast_nodes.DotSuffixData):#structs must have left
                        self.AutoDereference(type0)
                        struct=self.StructDefinitions.get(type0.type)
                        idx=struct.field_names.index(suffix.identifier)
                        data_type=struct.field_types[idx]
                        res=self.GenTempName()
                        ptr=self.GenTempName()
                        self.block+=f'''{ptr} = getelementptr %{type0.type}, ptr {type0.left}, i32 0, i32 {idx}
                            {res} = load {self.GetAllocType(data_type)}, ptr {ptr}\n'''
                        type0=IRType(type=struct.field_types[idx],identifier=res,left=ptr)
            
                    elif isinstance(suffix,ast_nodes.DotSuffixMethod):
                        identifier=suffix.pathExprSegment.identifier
                        if '@' in identifier:#clone or len:
                            if identifier.startswith("clone"):
                                cloneType=identifier[6:]
                                alloc_type=self.GetAllocType(cloneType)
                                self.AutoDereference(type0,cloneType)
                                res=self.GenTempName()
                                val=self.GenTempName()
                                s,block_name=self.Clone(type0,res,block_name)
                                self.block+=f'    {res} = alloca {alloc_type}\n'+s+f'    {val} = load {alloc_type}, ptr {res}\n'
                                type0=IRType(type=cloneType,identifier=val,left=res)
                            else:#array len is fixed!
                                ptr=self.GenTempName()
                                length=self.GetArrayInfo(type0.type)[1]
                                self.block+=f'    {ptr} = alloca i32\n    store i32 {length}, ptr {ptr}\n'
                                type0=IRType(type='usize',identifier=str(length),left=ptr)
                        else:
                            args=[type0]
                            for i in range(len(suffix.callarguments.expressions)):
                                type,block_name=self.ParseExpression(scope,suffix.callarguments.expressions[i],block_name,break_name=break_name,continue_name=continue_name)
                                if type.type=='^':
                                    return IRType(type='^',identifier=None),block_name
                                args.append(type)
                            funcName=self.dereference(type0.type)+"::"+identifier
                            type0,block_name = self.CallFunction(funcName,args,block_name)                   
            return type0,block_name
        elif isinstance(expression,ast_nodes.NonBlockPrimary):
            if expression.type=='literal':
                return self.ParseExpression(scope,expression.expression,block_name,break_name=break_name,continue_name=continue_name)
            
            elif expression.type=='path':
                typePathSegments=expression.expression.typePathSegments
                if not expression.structExprFields:#reference by name
                    if '<' in typePathSegments[0].identifier:#Vec or Box
                        return IRType(type=typePathSegments[0].identifier,identifier=None),block_name
                    else:
                        var=scope.get(typePathSegments[0].identifier)#reference by name,may be function or variable
                        if var.type.startswith("#"):#function
                            return IRType(type=var.type,identifier=None),block_name
                        elif not var.identifier.startswith("%"): #constant
                            return IRType(type=var.type,identifier=var.identifier),block_name
                        else:#variable
                            temp=self.GenTempName()
                            self.block+=f'   {temp} = load {self.GetAllocType(var.type)}, ptr {var.identifier}\n'
                            return IRType(type=var.type,identifier=temp,left=var.identifier),block_name
                else:#build struct
                    struct=self.StructDefinitions.get(typePathSegments[0].identifier)
                    args=[0]*len(expression.structExprFields)
                    for i in range(len(expression.structExprFields)):
                        type,block_name=self.ParseExpression(scope,expression.structExprFields[i].expression,block_name,break_name=break_name,continue_name=continue_name)
                        idx=struct.field_names.index(expression.structExprFields[i].identifier)
                        if type.type=='^':
                            return IRType(type='^',identifier=None),block_name
                        args[idx]=type

                    for i in range(len(args)):
                        self.AutoDereference(args[i],struct.field_types[i])
                    ptr=self.GenTempName()
                    temp=self.GenTempName()
                    self.block+=f'    {ptr} = alloca %{struct.identifier}\n'
                    for i in range(len(args)):
                        src=self.GenTempName()
                        self.block+=f'{src} = getelementptr %{struct.identifier}, ptr {ptr}, i32 0, i32 {i}\n    store {self.GetAllocType(args[i].type)} {args[i].identifier}, ptr {src}\n'
                    self.block+=f'    {temp} = load %{struct.identifier}, ptr {ptr}\n'
                    return IRType(type=struct.identifier,identifier=temp,left=ptr),block_name
            
            elif expression.type=='paren':
                if expression.expression:
                    return self.ParseExpression(scope,expression.expression,block_name,break_name=break_name,continue_name=continue_name)
                else:
                    return self.GenUnit(),block_name
            
            elif expression.type=='array':
                return self.ParseExpression(scope,expression.expression,block_name,break_name=break_name,continue_name=continue_name)
            
            elif expression.type=='break':
                if expression.expression:
                    type,block_name=self.ParseExpression(scope,expression.expression,block_name,break_name=break_name,continue_name=continue_name)
                    if type.type!='^':
                        ret_val,wanted_type,break_block=break_name.split('@')#retval is alloca 
                        self.AutoDereference(type,self.GetIRType(wanted_type))
                        self.block+=f'  store {self.GetAllocType(type.type)} {type.identifier}, ptr {ret_val}\n  br label %{break_block}\n'
                else:
                    ret_val,wanted_type,break_block=break_name.split('@')
                    self.block+=f'  store %Internal.Unit zeroinitializer, ptr {ret_val}\n  br label %{break_block}\n'
                return IRType(type='^',identifier=None),block_name
            
            elif expression.type=='return':
                if expression.expression:
                    type,block_name=self.ParseExpression(scope,expression.expression,block_name,break_name=break_name,continue_name=continue_name)
                    if type.type!='^':
                        self.block+=f'  ret {self.GetAllocType(type.type)} {type.identifier}\n'
                else:#return ()
                    self.block+=f'  ret %Internal.Unit zeroinitializer\n'
                return IRType(type='^',identifier=None),block_name
            
            elif expression.type=='continue':
                self.block+=f'  br label %{continue_name}\n'
                return IRType(type='^',identifier=None),block_name

        elif isinstance(expression,ast_nodes.NormalExpressionWithBlock):
            if expression.loop:
                if expression.conditionExpression:#while
                    while_block=self.GenBlockName()
                    then_block=self.GenBlockName()
                    else_block=self.GenBlockName()
                    ret_val=self.GenTempName()
                    self.block+=f'  {ret_val} = alloca %Internal.Unit\nstore %Internal.Unit zeroinitializer, ptr {ret_val}\n{while_block}:\n' 
                    type0,block_name=self.ParseExpression(scope,expression.conditionExpression,while_block)#condition has no loopContext
                    if type0.type=='^':
                        return IRType(type='^',identifier=None),block_name
                    self.AutoDereference(type0,'bool')
                    self.block+=f'  br i1 {type0.identifier}, label %{then_block}, label %{else_block}\n{then_block}:\n'
                    block_name=then_block
                    type,block_name=self.ParseExpression(scope,expression.blockExpression,block_name,break_name=f'{ret_val}@()@{else_block}',continue_name=while_block)
                    temp=self.GenTempName()
                    self.block+=f'  br label %{while_block}\n{else_block}:\n    {temp} = load %Internal.Unit, ptr {ret_val}\n'
                    block_name=else_block
                    return IRType(type='()',identifier=temp,left=ret_val),block_name
                else:#loop
                    while_block=self.GenBlockName()
                    else_block=self.GenBlockName()
                    ret_val=self.GenTempName()
                    temp=self.GenTempName()
                    if expression.loop!='^':
                        self.block+=f'  {ret_val} = alloca {self.GetAllocType(expression.loop)}\n'
                    self.block+=f'{while_block}:\n'
                    self.ParseExpression(scope,expression.blockExpression,while_block,break_name=f'{ret_val}@{expression.loop}@{else_block}',continue_name=while_block)
                    self.block+=f'  br label %{while_block}\n{else_block}:\n'
                    if expression.loop!='^':
                        self.block+=f'  {temp} = load {self.GetAllocType(expression.loop)}, ptr {ret_val}\n'
                        return IRType(type=self.GetIRType(expression.loop),identifier=temp,left=ret_val),else_block
                    else:
                        return IRType(type='^',identifier=None),else_block
            else:
                return self.ParseExpression(scope,expression.blockExpression,block_name,break_name=break_name,continue_name=continue_name)
        
        
        elif isinstance(expression,ast_nodes.IfExpression):
            type,block_name=self.ParseExpression(scope,expression.conditionExpression,block_name,break_name=break_name,continue_name=continue_name)
            if type.type=='^':
                return IRType(type='^',identifier=None),else_block
            self.AutoDereference(type,'bool')
            if len(expression.thenExpressions)==2:
                then_block=self.GenBlockName()
                else_block=self.GenBlockName()
                after_block=self.GenBlockName()
                self.block+=f'  br i1 {type.identifier}, label %{then_block}, label %{else_block}\n{then_block}:\n'
                type0,new_then_block=self.ParseExpression(scope,expression.thenExpressions[0],then_block,break_name=break_name,continue_name=continue_name)
                if expression.retType!='^':
                    self.AutoDereference(type0,self.GetIRType(expression.retType))
                self.block+=f'  br label %{after_block}\n{else_block}:\n'
                type1,new_else_block=self.ParseExpression(scope,expression.thenExpressions[1],else_block,break_name=break_name,continue_name=continue_name)
                if expression.retType!='^':
                    self.AutoDereference(type1,self.GetIRType(expression.retType))
                self.block+=f'{after_block}:\n'
                if type0.type=='^' and type1.type=='^':
                    return IRType(type='^',identifier=None),after_block
                elif type0.type=='^':
                    return type1,after_block
                elif type1.type=='^':
                    return type0,after_block
                else:
                    ret_val=self.GenTempName()
                    unionType=self.GetAllocType(expression.retType)
                    self.block+=f'  {ret_val} = phi {unionType} [{type0.identifier}, %{new_then_block}], [{type1.identifier}, %{new_else_block}]\n'
                    return IRType(type=self.GetIRType(expression.retType),identifier=ret_val),after_block
            else:
                then_block=self.GenBlockName()
                else_block=self.GenBlockName()
                self.block+=f'  br i1 {type.identifier}, label %{then_block}, label %{else_block}\n{then_block}:\n'
                self.ParseExpression(scope,expression.thenExpressions[0],then_block,break_name=break_name,continue_name=continue_name)
                self.block+=f'{else_block}:\n'
                return self.GenUnit(),else_block


        elif isinstance(expression,ast_nodes.BlockExpression):
            newscope=IRScope(vars={},parent=scope)
            for statement in expression.statements:
                block_name=self.ParseStatement(newscope,statement,block_name,break_name=break_name,continue_name=continue_name)
            type,block_name=self.ParseExpression(newscope,expression.statementexpression,block_name,break_name=break_name,continue_name=continue_name) if expression.statementexpression else (self.GenUnit(),block_name)
            if expression.has_never:
                return IRType(type='^',identifier=None),block_name
            else:
                return type,block_name    


        elif isinstance(expression,ast_nodes.NormalArrayExpresssion):
            innerType,length=self.GetArrayInfo(expression.type)
            if length==0:#UB
                return self.GenUnit(),block_name
            alloc_type=self.GetAllocType(innerType)
            res=self.GenTempName()
            val=self.GenTempName()
            self.block+=f'  {res} = alloca [{length} x {alloc_type}]\n'
            args=[]
            for each in expression.expressions:
                type,block_name=self.ParseExpression(scope,each,block_name,break_name=break_name,continue_name=continue_name)
                if type.type=='^':
                    return IRType(type='^',identifier=None),block_name
                args.append(type)
            for i in range(len(args)):
                self.AutoDereference(args[i],innerType)
                src=self.GenTempName()
                self.block+=f'  {src} = getelementptr [{length} x {alloc_type}], ptr {res}, i32 0, i32 {i}\n    store {alloc_type} {args[i].identifier}, ptr {src}\n'
            self.block+=f'    {val} = load [{length} x {alloc_type}], ptr {res}\n'
            return IRType(type=f'[{innerType};{length}]',identifier=val,left=res),block_name

        
        elif isinstance(expression,ast_nodes.RepeatArrayExpression):
            length=expression.real_length
            if length==0:#UB
                return self.GenUnit(),block_name
            type,block_name=self.ParseExpression(scope,expression.expression,block_name,break_name=break_name,continue_name=continue_name)
            if type.type=='^':
                return IRType(type='^',identifier=None),block_name
            alloc_type=self.GetAllocType(type.type)
            res=self.GenTempName()
            val=self.GenTempName()
            ctr=self.GenTempName()
            temp1=self.GenTempName()
            temp2=self.GenTempName()
            dest=self.GenTempName()
            condition=self.GenTempName()

            loop_block=self.GenBlockName()
            new_block=self.GenBlockName()
            self.block+=f'''  {res} = alloca [{length} x {alloc_type}]
                {ctr} = alloca i32
                store i32 0, ptr {ctr}
            {loop_block}:
                {temp1} = load i32, ptr {ctr}
                {dest} = getelementptr [{length} x {alloc_type}], ptr {res}, i32 0, i32 {temp1}\n'''
            self.block+=self.Move(type,dest)
            self.block+=f''' {temp2} = add i32 {temp1}, 1
                store i32 {temp2}, ptr {ctr}
                {condition} = icmp eq i32 {temp2}, {length}
                br i1 {condition}, label %{new_block}, label %{loop_block}
            {new_block}:
                {val} = load [{length} x {alloc_type}], ptr {res}\n'''
                
            return IRType(type=f'[{type.type};{length}]',identifier=val,left=res),new_block


        elif isinstance(expression,ast_nodes.LiteralExpression):
            if expression.type=='bool':
                return IRType(type='bool',identifier='1' if expression.value else '0'),block_name
            else:
                return IRType(type=expression.type,identifier=str(expression.value)),block_name


    def ParseStatement(self,scope:Scope,statement:ast_nodes.Statement,block_name:str,break_name:str=None,continue_name:str=None)->str:#return block_name
        if isinstance(statement,ast_nodes.LetStatement):
            type,block_name=self.ParseExpression(scope,statement.value,block_name,break_name=break_name,continue_name=continue_name)
            if type.type=='^':
                return block_name
            self.AutoDereference(type,self.GetIRType(statement.type))
            res=self.GenVarName()
            alloc_type=self.GetAllocType(statement.type)
            self.block+=f'    {res} = alloca {alloc_type}\n    store {alloc_type} {type.identifier}, ptr {res}\n'
            scope.register(statement.identifier,IRType(type=type.type,identifier=res))
            return block_name
        else:
            if statement.expression:
                return self.ParseExpression(scope,statement.expression,block_name,break_name=break_name,continue_name=continue_name)[1]


    def Build(self):
        self.StructDefinitions["Vec"]=IRStruct(identifier="Vec",field_names=["length","cap","base"],field_types=["i32","i32","& T"],size=12)
        self.StructDefinitions["Internal.Unit"]=IRStruct(identifier="Internal.Unit",field_names=[],field_types=[],size=0)
        #Box<T> is special ptr

        for structName in self.checker.StructOrder:
            struct=self.checker.StructDefinitions[structName]
            field_names=[]
            field_types=[]
            size=0
            for field_name in struct.fields:
                field_names.append(field_name)
                field_types.append(self.GetIRType(struct.fields[field_name].type))
                delta=self.GetAllocSize(field_types[-1])
                if delta!=1 and size%4!=0:
                    size+=4-size%4
                size+=delta
            if size%4!=0:
                size+=4-size%4
            self.StructDefinitions[structName]=IRStruct(identifier=structName,field_names=field_names,field_types=field_types,size=size)
            
            
            functionName=f"Equal{structName}"
            length=len(field_names)
            temp=self.GenTempName()
            type1=self.GenTempName()
            type2=self.GenTempName()
            res=self.GenTempName()
            fail_block=self.GenBlockName()
            win_block=self.GenBlockName()

            block_name="entry"
            s=f'''define i1 @{functionName}(ptr {type1}, ptr {type2}){{
            entry:   
                {temp} = alloca i1
                store i1 true, ptr {temp}'''
            for i in range(length):
                s1=self.GenTempName()
                s2=self.GenTempName()
                t1=self.GenTempName()
                t2=self.GenTempName()
                val=self.GenTempName()

                alloc_type=self.GetAllocType(field_types[i])
                s+=f'''    {s1} = getelementptr %{structName}, ptr {type1}, i32 0, i32 {i}
                    {t1} = load {alloc_type}, ptr {s1}
                    {s2} = getelementptr %{structName}, ptr {type2}, i32 0, i32 {i}
                    {t2} = load {alloc_type}, ptr {s2}\n'''
                news,block_name=self.Equal(IRType(type=field_types[i],identifier=t1,left=s1),IRType(type=field_types[i],identifier=t2,left=s2),val,block_name)
                if i==length-1:
                    s+=news+f'''    br i1 {val}, label %{win_block}, label %{fail_block}
                    {fail_block}:
                        store i1 false, ptr {temp}\n'''
                else:
                    next_block=self.GenTempName()
                    s+=news+f'   br i1 {val}, label %{next_block}, label %{fail_block}\n{next_block}:\n'
                    block_name=next_block
            s+=f'''{win_block}:\n   {res} = load i1, ptr {temp}\n   ret i1 {res}\n}}\n'''
            self.EqualFunctions.append(s)
    
        
        self.global_scope=IRScope(vars={},parent=None)
        for name in self.checker.scope.values:#register functions into scope
            if self.checker.scope.values[name].type.startswith("#"):
                self.global_scope.register(name,IRType(type='#'+name,identifier=None))
                if name.endswith("::clone") and not self.checker.FunctionDefinitions.get(name):# clone
                    structName=name[:name.index("::")]
                    functionName=f'Clone{structName}'
                    struct=self.StructDefinitions[structName]
                    length=len(struct.field_names)

                    origin=self.GenTempName()
                    res=self.GenTempName()
                    val=self.GenTempName()

                    block_name='entry'
                    s=f'''define %{structName} @{functionName}(ptr {origin})\n{{    
                    entry:
                        {res} = alloca %{structName}\n'''
                    for i in range(length):
                        source=self.GenTempName()
                        src=self.GenTempName()
                        dest=self.GenTempName()
                        s+=f'''{source} = getelementptr %{structName}, ptr {origin}, i32 0, i32 {i}
                            {src} = load {self.GetAllocType(struct.field_types[i])}, ptr {source}
                            {dest} = getelementptr %{structName}, ptr {res}, i32 0, i32 {i}\n'''
                        news,block_name=self.Clone(IRType(type=struct.field_types[i],identifier=src,left=source),dest,block_name)
                        s+=news
                    s+=f'   {val} = load %{structName}, ptr {res}\n    ret %{structName} {val}\n}}\n'
                    self.CloneFunctions.append(s)


        for name in self.checker.ConstValues:
            self.global_scope.register(name,IRType(type=self.checker.ConstValues[name].type,identifier=str(int(self.checker.ConstValues[name].value))))

    
        for name in ['print_i32','println_i32','get_i32']:
            self.FunctionNewNames[name]=name
            self.FunctionDefinitions[name]=IRFunction(identifier=name,retType='i32' if name=="get_i32" else "()",param_names=['%param1'] if name!='get_i32' else [],param_types=['i32'] if name!='get_i32' else [],block=None,scope=None,body=None)
            
        for functionName in self.checker.FunctionDefinitions:
            if functionName in ['print_i32','println_i32','get_i32']:
                continue
            func=self.checker.FunctionDefinitions[functionName]
            self.funcctr+=1
            newFuncName=f"func{self.funcctr}" if functionName!="main" else "rx_source_main"
            self.FunctionNewNames[functionName]=newFuncName
            param_names=[]
            param_types=[]
            paramctr=0
            self.block="entry:\n"
            function_scope=IRScope(vars={},parent=self.global_scope)
            #register function parameters
            if func.self:
                impl=functionName[:functionName.index("::")]
                paramctr+=1
                varname=f'%prm{paramctr}'
                param_names.append("%param1")
                param_types.append("& "+impl if func.self.amp else impl)
                function_scope.register("self",IRType(identifier=varname,type=param_types[-1]))
                self.block+=self.BuildAndStore(varname,f"%param{paramctr}",param_types[-1])
            for i in range(len(func.paramNames)):#function params should have addr
                paramctr+=1
                varname=f'%prm{paramctr}'
                param_names.append(f"%param{paramctr}")
                param_types.append(self.GetIRType(func.params[i].type))
                function_scope.register(func.paramNames[i],IRType(identifier=varname,type=param_types[-1]))
                self.block+=self.BuildAndStore(varname,f"%param{paramctr}",param_types[-1])
            self.FunctionDefinitions[newFuncName]=IRFunction(identifier=functionName,retType=self.GetIRType(func.returnType.type) if func.returnType else "()",param_names=param_names,param_types=param_types,block=self.block,scope=function_scope,body=func.body)

        for newFuncName in self.FunctionDefinitions:
            if newFuncName in ['print_i32','println_i32','get_i32']:
                continue
            self.tempctr=self.varctr=self.blockctr=0
            self.block="" 
            func=self.FunctionDefinitions[newFuncName]
            type=self.ParseExpression(func.scope,func.body,"entry")[0]
            if type.type!='^':
                self.block+=f'    ret {self.GetAllocType(type.type)} {type.identifier}\n'
            func.block+=self.block
        #define main
        self.FunctionDefinitions['main']=IRFunction(identifier=name,retType='i32',param_names=[],param_types=[],block='    call %Internal.Unit @rx_source_main()\n   ret i32 0\n',scope=None,body=None)
        #output
        with open(self.output,"w") as f:
            f.write('target triple = "riscv32-unknown-unknown-elf"\n\ndeclare void @print_i32(i32)\ndeclare void @println_i32(i32)\ndeclare i32 @get_i32()\ndeclare ptr @__rx_alloc(i32, i32)\n\n')
            #output StructDefinitions
            for structName in self.StructDefinitions:
                description=", ".join([self.GetAllocType(field_type) for field_type in self.StructDefinitions[structName].field_types])
                f.write(f"%{structName} = type{{ {description} }}\n\n")
            for each in self.CloneFunctions:
                f.write(self.beautify(each)+'\n')
            for each in self.EqualFunctions:
                f.write(self.beautify(each)+'\n')
            for functionName in self.FunctionDefinitions:
                if functionName in ['print_i32','println_i32','get_i32']:
                    continue
                func=self.FunctionDefinitions[functionName]
                params=", ".join([self.GetAllocType(func.param_types[i])+" "+func.param_names[i] for i in range(len(func.param_names))])
                f.write(f"define {self.GetAllocType(func.retType)} @{functionName}({params})")
                f.write("{\n")
                f.write(self.beautify(func.block))
                f.write("}\n\n")


            
