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
    arithmeticOps=["+","-","*","/",'%',"shift",'@',"|","^"]#@ for &
    unaryOps=['minus','star','!','&','&mut']
    
    basicTypes=['i32','u32','usize','isize','bool']
    integers=['i32','u32','usize','isize']
    def __init__(self,checker:Checker,output:str):
        self.StructDefinitions={}#structName(str)->IRStruct
        self.FunctionDefinitions={}#functionName(str)->IRFunction
        self.FunctionNewNames={}#functionName in checker->functionName in IR
        self.checker=checker#already done SemanticCheck
        self.output=output#output_path
        self.tempctr=0
        self.varctr=0
        self.funcctr=0
        self.blockctr=0
        self.block=""

    def CountPtr(self,type:str)->int,str:
        cnt=0
        while True:
            if type.startswith("& "):
                type=type[2:]
                cnt+=1
            elif type.startswith("&mut "):
                type=type[5:]
                cnt+=1
            elif type.startswith("Box<"):
                type=type[4:-1]
                cnt+=1
            else:
                break
        return cnt,type
        
    def GenTempName(self)->str:#generate a temporary variable
        self.tempctr+=1
        return f"%temp{self.tempctr}"
    
    def GenVarName(self)->str:#generate a local variable
        self.varctr+=1
        return f"%var{self.varctr}"

    def GenBlockName(self)->str:#generate a local variable
        self.blockctr+=1
        return f"block{self.varctr}"
    
    def GetIRType(type:str)->str:#replace all &mut with &
        return type.replace('&mut','&')

    def GetArrayInfo(self,type:str)->tuple[str,int]:#array innerType and length
        idx=len(type)-1
        while type[idx]!=';':
            idx-=1
        return type[1:idx],int(type[idx+1:-1])

    
    def GetAllocType(self,type:str)->str:
            if type.startswith("&") or type.startswith("Box<"):
                return "ptr"
            elif type.startswith("Vec<"):
                return "%Vec"
            elif type=="()":
                return "%Unit"
            elif type in ["i32","u32","isize","usize"]:
                return "i32"
            elif type=="bool":
                return "i1"
            elif type.startswith("["):
                innerType,length=self.GetArrayInfo(type)
                return f"[{length} x {self.GetAllocType(innerType)}]"
            else:
                return "%"+type

    def Dereference(self,type:IRType,cnt=1):#return s,tempname
        s=""
        last=type.identifier
        lasttype=type.type
        for _ in range(cnt):
            temp=self.GenTempName()
            lasttype=lasttype[2:] if lasttype.startswith("& ") else lasttype[4:-1]#Box
            s+=f"   {temp} = load {self.GetAllocType(lasttype)}, ptr {last}\n"
            last=temp
        return s,last
    def dereference(self,type:str)->str:
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
            elif    type.type.startswith("Box<"):
                type.type=type.type[4:-1]
            else:
                return
            self.block+=f"   {temp} = load {self.GetAllocType(type.type)}, ptr {type.identifier}\n"
            type.left=type.identifier
            type.identifier=temp

    def BuildAndStore(self,var1:str,var2:str,type:str)->str:#store var2's value into var1
        return f"   {var1} = alloca {type}\n   store {type} {var2}, ptr {var1}\n"#statement format: Tab{statement}\n
    
    def Store(self,var1:str,var2:str,type:str)->str:#store var2's value into var1
        return f"   store {type} {var2}, ptr {var1}\n"

    def Calc(self,type1:IRType,type2:IRType,op:str,block_name:str):#return str,IRType,block_name
        s=""
        temp=""
        block_name=""
        if op in self.assignmentOps:
            if op!="=":
                temp=self.GenTempName()
                if type2.type.startswith("& "):
                    temp2=self.GenTempName()
                    s+=f"    {temp2} = load {self.Bitsize(type2.type[2:])}, ptr {type2.identifier}\n"
                    type2.identifier=temp2
                if op in ["+=","-=","*=","<<="]:
                    s+=f"   {temp} = {["add","sub","mul","shl"][["+=","-=","*=","<<="].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
                elif op in ["/=","%=",">>="]:
                    if type1.type in ['i32','isize']:#i
                        s+=f"   {temp} = {["sdiv","srem","ashr"][["/=","%=",">>="].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
                    else:#u
                        s+=f"   {temp} = {["udiv","urem","lshr"][["/=","%=",">>="].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
                elif op in ["&=","|=","^="]:
                    if type1.type=='bool':#i1
                        s+=f"   {temp} = {["and","or","xor"][["&=","|=","^="].index(op)]} i1 {type1.identifier}, {type2.identifier}\n"
                    else:#i32
                        s+=f"   {temp} = {["and","or","xor"][["&=","|=","^="].index(op)]} i32 {type1.identifier}, {type2.identifier}\n"
            else:#=
                s,temp=self.Dereference(type2,cnt=self.CountPtr(type2.type)[0]-self.CountPtr(type1.type)[0])
                news,block_name=self.Clone(IRType(type=type1.type,identifier=temp),type1.left,block_name)
            res=self.GenTempName()
            return s+news+f"    {res} = freeze %Unit zeroinitializer\n",IRType(type="()",identifier=res),block_name
        
        elif op in self.comparisonOps:
            temp=self.GenTempName()
            if op in ['==','!=']:
                s=f"   {temp} = icmp {("eq" if op=='==' else "ne")} {self.GetAllocType(type1.type)} {type1.identifier},{type2.identifier}\n"
            
            elif op in [">","<","<=",">="]:
                cnt1,type=self.CountPtr(type1.type)
                s1,temp1=self.Dereference(type1,cnt=cnt1)
                s2,temp2=self.Dereference(type2,cnt=self.CountPtr(type2.type)[0])
                if type in ["i32","isize"]:
                    s=s1+s2+f"   {temp} = icmp {["sgt","slt","sge","sle"][[">","<","<=",">="].index(op)]} i32 {temp1}, {temp2}\n"
                if type in ["u32","usize"]:
                    s=s1+s2+f"   {temp} = icmp {["ugt","ult","uge","ule"][[">","<","<=",">="].index(op)]} i32 {temp1}, {temp2}\n"
                else:#bool
                    s=s1+s2+f"   {temp} = icmp {["ugt","ult","uge","ule"][[">","<","<=",">="].index(op)]} i1 {temp1}, {temp2}\n"
                
            return s,IRType(type="bool",identifier=temp),block_name

        elif op in self.logicOps:
            temp=self.GenTempName()
            return f"   {temp} = {op} i1 {type1.identifier}, {type2.identifier}\n",IRType(type="bool",identifier=temp),block_name

        elif op in self.arithmeticOps:
            temp=self.GenTempName()
            cnt1,type=self.CountPtr(type1.type)
            s1,temp1=self.Dereference(type1,cnt=cnt1)
            s2,temp2=self.Dereference(type2,cnt=self.CountPtr(type2.type)[0])
            if op in ["+","-","*","<<"]:
                s=f"   {temp} = {["add","sub","mul","shl"][["+","-","*","<<"].index(op)]} i32 {temp1}, {temp2}\n"
            elif op in ["/","%",">>"]:
                if type in ['i32','isize']:#i
                    s=f"   {temp} = {["sdiv","srem","ashr"][["/","%",">>"].index(op)]} i32 {temp1}, {temp2}\n"
                else:#u
                    s=f"   {temp} = {["udiv","urem","lshr"][["/","%",">>"].index(op)]} i32 {temp1}, {temp2}\n"
            elif op in ["&","|","^"]:
                if type1.type=='bool':#i1
                    s=f"   {temp} = {["and","or","xor"][["&","|","^"].index(op)]} i1 {temp1}, {temp2}\n"
                else:#i32
                    s=f"   {temp} = {["and","or","xor"][["&","|","^"].index(op)]} i32 {temp1}, {temp2}\n"
            return s,IRType(type=type,identifier=temp),block_name
        
        elif op in self.unaryOps:#type2=None
            if op=='minus':
                temp=self.GenTempName()
                cnt,type=self.CountPtr(type1.type)
                s1,temp1=self.Dereference(type1,cnt=self.CountPtr(type1.type))
                s=s1+f"    {temp} = sub i32 0, {temp1}\n"
                return s,IRType(type=type,identifier=temp),block_name
            elif op=='!':
                temp=self.GenTempName()
                cnt,type=self.CountPtr(type1.type)
                s1,temp1=self.Dereference(type1,cnt=cnt)
                s=s1+(f"    {temp} = xor i1 {temp1}, true\n" if type=="bool" else f"    {temp} = xor i32 {temp1}, -1\n")
                return s,IRType(type=type,identifier=temp),block_name
            elif op=="star":
                s,temp=self.Dereference(type1)
                return s,IRType(type=type1.type[2:],identifier=temp),block_name
            else:#&
                temp=self.GenTempName()
                return self.BuildAndStore(temp,type1.identifier,self.GetAllocType(type1.type)),IRType(type="& "+type1.type,identifier=temp),block_name

    def Clone(self,type:IRType,res:str,block_name:str):#clone struct to res(ptr,already alloced),return s,block_name
        s=""
        if type.type=="()":#nothing should happen
            return s,block_name
        elif type.type in self.basicTypes or type.type.startswith("& "):
            return f"store {self.GetAllocType(type)} {type.identifier}, ptr {res}\n",block_name
        elif type.type.startswith("Box<"):
            dest=self.GenTempName()
            src=self.GenTempName()
            alloc_type=self.GetAllocType(innerType)
            innerType=type.type[4:-1]
            s=f'''{src} = load {self.GetAllocType(innerType)}, ptr {type.identifier}\n
                {dest} = alloca {alloc_type}\n'''
            news,block_name=self.Clone(IRType(type=innerType,identifier=src),dest,block_name)
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
            new_res=self.GenTempName()
            condition=self.GenTempName()
            s+=f'''     {new_res} = load [{length} x {alloc_type}], ptr {res}
                {ctr} = alloca i32
                store i32 0, ptr {ctr}
            {loop_block}:
                {temp1} = load i32, ptr {ctr}
                {source} = getelementptr {alloc_type}, ptr {type.identifier}, i32 {temp1}
                {src} = load {alloc_type}, ptr {source}
                {dest} = getelementptr {alloc_type}, ptr {new_res}, i32 {temp1}\n'''    
            news,_=self.Clone(IRType(type=innerType,identifier=src),dest,block_name)
            s+=news 
            new_block_name=self.GenBlockName()
            s+=f'''{temp2} = add i32 {temp1}, 1
                store i32 {temp2}, ptr {ctr}
                {condition} = icmp ne i32 {temp2}, {length}
                br i1 {condition}, label {loop_block},label {new_block_name}
            {new_block_name}:\n'''     
            return s,new_block_name 
        elif type.type.startswith("Vec<"):
            innerType=type.type[4:-1]
            temp=self.GenTempName()
            temp1=self.GenTempName()
            temp2=self.GenTempName()

            length=self.GenTempName()
            length_ptr=self.GenTempName()
            src=self.GenTempName()
            dest=self.GenTempName()
            cap=self.GenTempName()
            cap_ptr=self.GenTempName()
            pointer=self.GenTempName()
            new_res=self.GenTempName()
            source=self.GenTempName()
            condition=self.GenTempName()

            loop_block=self.GenBlockName()
            ctr=self.GenTempName()
            alloc_type=self.GetAllocType(innerType)
            s+=f'''
                {length} = extractvalue %Vec {type.identifier}, 0
                {cap} = extractvalue %Vec {type.identifier}, 1
                {pointer} = extractvalue %Vec {type.identifier}, 2
                {length_ptr} = getelementptr %Vec, ptr {res}, i32 0, i32 0
                {cap_ptr} = getelementptr %Vec, ptr {res}, i32 0, i32 1
                store i32 {length}, ptr {length_ptr}
                store i32 {cap}, ptr {cap_ptr}
                {pointer} = load ptr, ptr {temp3}
                {temp} = getelementptr %Vec, ptr {res}, i32 0, i32 2
                {new_res} = alloca {alloc_type}, i32 {cap}
                store ptr {new_res}, ptr {temp}
                {ctr} = alloca i32
                store i32 0, ptr {ctr}
            {loop_block}:
                {temp1} = load i32, ptr {ctr}
                {source} = getelementptr {alloc_type}, ptr {pointer},i32 {temp1}
                {src} = load {alloc_type}, ptr {source}
                {dest} = getelementptr {alloc_type}, ptr {new_res}, i32 {temp1}\n'''    
            news,_=self.Clone(IRType(type=innerType,identifier=src),dest,block_name)
            s+=news 
            new_block_name=self.GenBlockName()
            s+=f'''{temp2} = add i32 {temp1}, 1
                    store i32 {temp2}, ptr {ctr}
                    {condition} = icmp ne i32 {temp2}, {length}
                    br i1 {condition}, label {loop_block},label {new_block_name}
                {new_block_name}:\n'''  
            return s,new_block_name 
        else:#struct
            struct=self.StructDefinitions[type.type]
            length=len(struct.field_names)
            for i in range(length):
                src=self.GenTempName()
                dest=self.GenTempName()
                s+=f'''{src} = extractvalue %{struct} {type.identifier}, i32 {i}
                    {dest} = getelementptr %{struct}, ptr {res}, i32 0, i32 {i}\n'''
                news,block_name=self.Clone(IRType(type=struct.field_types[i],identifier=src),dest,block_name)
                s+=news
            return s,block_name

    def Move(self,type:IRType,res:str):#move struct to res(ptr,already alloced),return s,block_name
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
            res=self.GenTempName()
            ptr=self.GenTempName()
            s=f'''  {temp} = alloca %Vec
                {ptr} = alloca [2 x {alloc_type}]
                store %Vec {{ i32 0, i32 2, ptr {ptr} }}, ptr {temp}
                {res} = load %Vec, ptr {temp}\n'''
            return s,IRType(type=f"Vec<{innerType}>",identifier=res,left=temp),block_name
        elif func_name=="push":
            length_ptr=self.GenTempName()
            cap_ptr=self.GenTempName()
            pointer_ptr=self.GenTempName()
            length=self.GenTempName()
            cap=self.GenTempName()
            pointer=self.GenTempName()

            if_full=self.GenTempName()
            cap2=self.GenTempName()
            new_pointer=self.GenTempName()
            new_length=self.GenTempName()

            ctr=self.GenTempName()
            temp1=self.GenTempName()
            temp2=self.GenTempName()
            source=self.GenTempName()
            src=self.GenTempName()
            dest=self.GenTempName()
            condition=self.GenTempName()

            alloc_type=self.GetAllocType(innerType)
            if_block=self.GenBlockName()
            else_block=self.GenBlockName()
            loop_block=self.GenBlockName()
            s=f'''   {length_ptr} = getelementptr %Vec, ptr {args[0].identifier}, i32 0, i32 0   
                {length} = load i32, ptr {length_ptr}
                {new_length} = add i32 {length},1
                store i32 {new_length}, ptr {length_ptr}
                {cap_ptr} = getelementptr %Vec, ptr {args[0].identifier}, i32 0, i32 1   
                {cap} = load i32, ptr {length_ptr}
                {pointer_ptr} = getelementptr %Vec, ptr {args[0].identifier}, i32 0, i32 2   
                {pointer} = load ptr, ptr {pointer_ptr}
                {if_full} = icmp eq i32 {length}, {cap}
                br i1 {if_full}, label {if_block}, label {else_block}
            {if_block}:
                {cap2} =  add i32 {cap}, {cap}
                {new_pointer} = alloca {alloc_type}, i32 {cap2}
                store ptr {new_pointer}, ptr {pointer_ptr}
                store i32 {cap2}, ptr {cap_ptr}
                {ctr} = alloca i32
                store i32 0, ptr {ctr}
            {loop_block}:
                {temp1} = load i32, ptr {ctr}
                {source} = getelementptr {alloc_type}, ptr {pointer}, i32 {temp1}
                {src} = load {alloc_type}, ptr {source}
                {dest} = getelementptr {alloc_type}, ptr {new_pointer}, i32 {temp1}\n'''    
            s+=self.Move(IRType(type=innerType,identifier=src),dest,loop_block)

            newdest=self.GenTempName()
            truepointer=self.GenTempName()
            s+=f'''    {temp2} = add i32 {temp1}, 1
                store i32 {temp2}, ptr {ctr}
                {condition} = icmp ne i32 {temp2}, {length}
                br i1 {condition}, label {loop_block},label {else_block}
            {else_block}:
                {truepointer} = load ptr, ptr {pointer_ptr}
                {newdest} = getelementptr {alloc_type}, ptr {truepointer}, i32 {length}
            '''
            s+=self.Move(IRType(type=innerType,identifier=args[-1].identifier),newdest,else_block)
            return s,IRType(type="()",identifier=temp),else_block
        elif func_name=="remove":
            length_ptr=self.GenTempName()
            pointer_ptr=self.GenTempName()
            ans_ptr=self.GenTempName()
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
            cond=self.GenBlockName()
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
                {ans_ptr} = getelementptr {alloc_type}, ptr {pointer}, i32 {args[0].identifier}
                {ans} = load {alloc_type}, ptr {ans_ptr}
                {cond} = icmp eq i32 {new_length}, {args[-1].identifier}
                br i1 {cond}, label {new_block}, label {prep_block}
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
                br i1 {condition}, label {new_block}, label {loop_block}
            {new_block}:\n'''
            return s,IRType(type=innerType,identifier=ans),new_block
        else:#clone
            res=self.GenTempName()
            val=self.GenTempName()
            src=self.GenTempName()
            s=f'''{res} = alloca %Vec
                {src} = load %Vec, ptr {args[0].identifier}\n'''
            news,block_name=self.Clone(IRType(type=f"Vec<{innerType}",identifier=src),res,block_name)
            return s+news+f'    {val} = load %Vec, ptr {res}\n',IRType(type=f"Vec<{innerType}>",identifier=val,left=res),block_name


    def BoxOp(self,type:IRType,innerType:str,func_name:str,block_name:str,arg:IRType):#return s,Type,block_name                    
        if func_name=="new":
            res=self.GenTempName()
            val=self.GenTempName()
            alloc_type=self.GetAllocType(innerType)
            s=f'''  {res} = alloca ptr
                {val} = alloca {alloc_type}
                store {alloc_type} {arg.identifier}, ptr {val}
                store ptr {val}, ptr {res}\n'''
            return s,IRType(type=f"Box<{innerType}>",identifier=val,left=res),block_name
        else:#clone     
            res=self.GenTempName()
            val=self.GenTempName()
            src=self.GenTempName()
            s=f'''{res} = alloca ptr
            {src} = load ptr, ptr {arg.identifier}\n'''
            news,block_name=self.Clone(IRType(type=f"Box<{innerType}",identifier=src),res,block_name)
            return s+news+f'    {val} = load %Vec, ptr {res}\n',IRType(type=f"Box<{innerType}>",identifier=val,left=res),block_name         
                        
    def CallFunction(self,funcName:str,args:list[ast_nodes.Expression],block_name:str)-> tuple[IRType,str]:
        if funcName.startswith("Vec<"):#vec
            innerType=funcName[4:funcName("::")]
            funcName=funcName[funcName.index("::")+2:]
            if funcName!="new":
                self.AutoDereference(args[0],f"& Vec<{innerType}>")
            if funcName in ["push","remove"]:
                self.AutoDereference(args[-1],innerType if funcName=="push" else "usize")
            s,type,block_name=self.VecOp(innerType,funcName,block_name,args)
            self.block+=s
            return type,block_name
        elif funcName.startswith("Box<"):
            innerType=funcName[4:funcName("::")]
            funcName=funcName[funcName.index("::")+2:]
            if funcName=="clone":
                self.AutoDereference(args[0],f"& Box<{innerType}>")
            else:#new
                self.AutoDereference(args[0],innerType)
            s,type,block_name=self.BoxOp(innerType,funcName,block_name,args[0])
            self.block+=s
            return type,block_name
        else:            
            if funcName.count("::")==1 and funcName[funcName.index("::")+2:]=="clone":#if defined clone, use the user-defined clone
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
                    self.block+=f''' {temp} =  call {self.GetAllocType(func.retType)} @{newname}({s})\n'''
                    return IRType(type=func.retType,identifier=temp),block_name
                else:
                    self.block+=f'''    call void @{newname}({s})
                        {temp} = freeze %Unit zeroinitializer\n'''
                    return IRType(type="()",identifier=temp),block_name  

                
    def ParseExpression(self,scope:IRScope,expression:ast_nodes.Expression,block_name:str,break_name:str=None,continue_name:str=None)->tuple[IRType,str]:
        if isinstance(expression,ast_nodes.PrimitiveExpression):
            if expression.op in self.assignmentOps or expression.op in self.comparisonOps:
                type0,block_name=self.ParseExpression(scope,expression.expressions[0],block_name,break_name=break_name,continue_name=continue_name)
                type1,block_name=self.ParseExpression(scope,expression.expressions[1],block_name,break_name=break_name,continue_name=continue_name)
                s,type,block_name=self.Calc(type0,type1,expression.op,block_name)
                self.block+=s
                return type,block_name
            elif expression.op in self.logicOps or expression.op in self.arithmeticOps:
                type0,block_name=self.ParseExpression(scope,expression.expressions[0],block_name,break_name=break_name,continue_name=continue_name)
                for i in range(1,len(expression.expressions)):
                    type1,block_name=self.ParseExpression(scope,expression.expressions[i],block_name,break_name=break_name,continue_name=continue_name)
                    s,type0,block_name=self.Calc(type0,type1,expression.op if expression.op in self.logicOps else expression.ops[i-1],block_name)
                    self.block+=s
                return type0,block_name
        elif isinstance(expression,ast_nodes.UnaryExpression):
            type0,block_name=self.ParseExpression(scope,expression.postfixExpression,block_name,break_name=break_name,continue_name=continue_name)
            for op in expression.ops[::-1]:
                if op=='&&' or op=="&&mut":
                    s,type0,block_name=self.Calc(type0,None,"&",block_name)
                    self.block+=s
                    s,type0,block_name=self.Calc(type0,None,"&",block_name)
                    self.block+=s
                else:
                    s,type0,block_name=self.Calc(type0,None,op,block_name)
                    self.block+=s
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
                        args.append(type)
                    type0,block_name = self.CallFunction(type0.type[1:],args,block_name)
                    
                elif isinstance(suffix,ast_nodes.BracketSuffix):
                    idx,block_name=self.ParseExpression(scope,suffix.expression,block_name,break_name=break_name,continue_name=continue_name)                             
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
                        innerType=self.GetArrayInfo(type0.type)[0]
                        alloc_type=self.GetAllocType(innerType)
                        self.block+=f'''    {ptr} = getelementptr {alloc_type}, ptr {temp}, i32 {idx.identifier}
                            {res} = load {alloc_type}, ptr {ptr}\n'''
                        type0=IRType(type=innerType,identifier=res,left=ptr)
                            
                elif isinstance(suffix,ast_nodes.DotSuffix):
                    if isinstance(suffix,ast_nodes.DotSuffixData):#structs must have left
                        self.AutoDereference(type0)
                        struct=self.StructDefinitions.get(type0)
                        idx=struct.fields_names.index(suffix.identifier)
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
                                cloneType=self.GetIRType(cloneType)
                                alloc_type=self.GetAllocType(cloneType)
                                self.AutoDereference(type0,cloneType)
                                res=self.GenTempName()
                                val=self.GenTempName()
                                s,block_name=self.Clone(type0,res,block_name)
                                self.block+=f'    {res} = alloca {alloc_type}\n'+s+f'    {val} = load {alloc_type}, ptr {res}\n'
                                type0=IRType(type=cloneType,identifier=val,left=res)
                            else:#array len is fixed!
                                return IRType(type='usize',identifier=str(self.GetArrayInfo(type0.type)[1]))
                        else:
                            args=[type0]
                            for i in range(len(suffix.callarguments.expressions)):
                                type,block_name=self.ParseExpression(scope,suffix.callarguments.expressions[i],block_name,break_name=break_name,continue_name=continue_name)
                                args.append(type)
                            funcName=self.dereference(type0.type)+"::"+identifier
                            type0,block_name = self.CallFunction(funcName,args,block_name)                   
            return type0,block_name
        elif isinstance(expression,ast_nodes.NonBlockPrimary):
            if expression.type=='literal':
                return self.ParseExpression(scope,expression.expression,block_name,break_name=break_name,continue_name=continue_name)
            elif expression.type=='path':
                if expression.structExprFields==None:#reference by name
                    typePathSegments=expression.expression.typePathSegments
                    if '<' in typePathSegments[0].identifier:#Vec or Box
                        return IRType(type=f"#{typePathSegments[0].identifier}::{typePathSegments[1].identifier}",identifier=None),block_name
              
                    else:
                        #check genericArgs
                        for each in typePathSegments:
                            if len(each.genericArgs)>0:
                                raise SemanticError(f"genericArgs!")
                        name=typePathSegments[-1].identifier
                        if len(typePathSegments)==2:#impl
                            if typePathSegments[0].identifier=="Self":
                                if impl:
                                    typePathSegments[0].identifier==impl
                                else:
                                    raise SemanticError(f"invalid use of Self!")
                            name=typePathSegments[0].identifier+"::"+name
                        var=scope.get(name)#reference by name,may be function or variable
                        if expected and not self.CanTransform(var.type,expected,var.mut_blocked):
                            raise SemanticError(f"expression type error! {var.type} != {expected}")
                        return Type(mut=var.mut,mut_blocked=var.mut_blocked,left=var.left,type=expected if expected else var.type)
                else:#build Struct
                    typePathSegments=expression.expression.typePathSegments
                    args=expression.structExprFields
                    if len(typePathSegments)!=1 or len(typePathSegments[0].genericArgs)!=0:
                        raise SemanticError("invalid struct!")
                    if typePathSegments[0].identifier=="Self":
                        if impl:
                            typePathSegments[0].identifier=impl
                        else:
                            raise SemanticError("use Self outside impl!")
                    struct=self.StructDefinitions.get(typePathSegments[0].identifier)
                    if not struct:
                        raise SemanticError(f"struct {typePathSegments[0].identifier} doesn't exist!")
                    identifiers=[arg.identifier for arg in args]
                    if len(identifiers)!=len(list(set(identifiers))):
                        raise SemanticError(f"repetitive args for struct {struct.type} construction!")
                    if len(struct.fields)!=len(identifiers):
                        raise SemanticError(f"invalid struct len! {len(struct.fields)}!={len(identifiers)}")
                    for arg in args:
                        structField=struct.fields.get(arg.identifier)
                        if not structField:
                            raise SemanticError(f"invalid arg name {arg.identifer} for struct {struct.type}")
                        self.ParseExpression(scope,arg.expression,expected=structField.type,impl=impl,inloop=inloop)
                    if expected and not self.CanTransform(typePathSegments[0].identifier,expected):
                        raise SemanticError(f"expression type error! {typePathSegments[0].identifier} != {expected}")
                    return Type(mut=False,mut_blocked=False,left=False,type=expected if expected else typePathSegments[0].identifier)
                            

            elif expression.type=='paren':
                if expression.expression:
                    return self.ParseExpression(scope,expression.expression,expected=expected,impl=impl,inloop=inloop)
                else:
                    if expected and not self.CanTransform("()",expected):
                        raise SemanticError(f"expression type error! () != {expected}")
                    return Type(mut=False,mut_blocked=False,left=False,type=expected if expected else "()")
            elif expression.type=='array':
                return self.ParseExpression(scope,expression.expression,expected=expected,impl=impl,inloop=inloop)
            elif expression.type=='break':
                if inloop and inloop.loop:
                    if expression.expression:
                        if inloop.loop=="while":
                            raise SemanticError("break expr inside while!")
                        new_type=self.ParseExpression(scope,expression.expression,expected=inloop.expectedType,impl=impl,inloop=inloop).type
                        if not inloop.expectedType:
                            inloop.retType=self.MergeType(inloop.retType,new_type)
                    else:#return ()
                        if not inloop.expectedType:
                            inloop.retType=self.MergeType(inloop.retType,"()")
                        elif not self.CanTransform("()",inloop.expectedType):
                            raise SemanticError(f"expression type error! () != {inloop.expectedType}")
                    inloop.has_break=inloop.has_never=True
                    return Type(mut=False,mut_blocked=False,left=False,type="^")
                else:
                    raise SemanticError("break outside loop!")
            elif expression.type=='return':
                retType=self.FunctionDefinitions.get(self.functionName).returnType
                type=retType.type if retType else "()"
                if expression.expression:
                    self.ParseExpression(scope,expression.expression,expected=type,impl=impl,inloop=inloop)
                else:#return ()
                    if type and not self.CanTransform("()",type):
                        raise SemanticError(f"function return type error! () != {type}")
                inloop.has_never=True
                return Type(mut=False,mut_blocked=False,left=False,type="^")
            elif expression.type=='continue':
                if not inloop or not inloop.loop:
                    raise SemanticError("continue outside loop!")
                inloop.has_never=True
                return Type(mut=False,mut_blocked=False,left=False,type="^")

        


    def Build(self):
        self.StructDefinitions["Vec"]=IRStruct(identifier="Vec",field_names=["length","cap","base"],field_types=["i32","i32","ptr"])
        self.StructDefinitions["Unit"]=IRStruct(identifier="Unit",field_names=[],field_types=[])
        #Box<T> is special ptr

        self.global_scope=IRScope(vars={},parent=global_scope)
        for name in self.checker.FunctionDefinitions:
            self.global_scope.register(name,Variable(mut=False,mut_blocked=False,left=False,type=f'#{name}',name=name))
        for name in self.checker.ConstValues:
            self.global_scope.register(name,IRType(type=self.ConstValues[name].type,name=name))

        for structName in self.checker.StructOrder:
            struct=self.checker.StructDefinitions[structName]
            self.StructDefinitions[structName]=IRStruct(identifier=structName,field_names=[field_name for field_name in struct.fields],field_types=[self.GetIRType(struct.fields[field_name]) for field_name in struct.fields])
        for functionName in self.checker.FunctionDefinitions:
            func=self.checker.FunctionDefinitions[functionName]
            self.funcctr+=1
            newFuncName=f"func{self.funcctr}" if functionName!="main" else "main"
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
                function_scope.register("self",IRType(identifier=varname,type=impl if not func.self.amp else '& '+impl))
                self.block+=self.BuildAndStore(varname,f"%param{paramctr}",param_types[-1])
            for i in range(len(func.paramNames)):#function params should have addr
                paramctr+=1
                varname=f'%prm{paramctr}'
                param_names.append(f"%param{paramctr}")
                param_types.append(self.GetIRType(func.params[i].type))
                function_scope.register(func.paramNames[i],IRType(identifier=varname,type=func.params[i].type))
                self.block+=self.BuildAndStore(varname,f"%param{paramctr}",param_types[-1])
            self.FunctionDefinitions[newFuncName]=IRFunction(identifier=functionName,retType=func.returnType.type,param_names=param_names,param_types=param_types,block=self.block,scope=function_scope,body=func.body)

        for newFuncName in self.FunctionDefinitions:
            self.tempctr=self.varctr=self.blockctr=0
            self.block="" 
            func=self.FunctionDefinitions[newFuncName]
            self.ParseExpression(func.scope,func.body,"entry")  
            func.block+=self.block

        #output
        with open(self.output,"w") as f:
            #output StructDefinitions
            for structName in self.StructDefinitions:
                description=", ".join([field_type] for field_type in self.StructDefinitions[structName].field_types)
                f.write(f"%{structName} = type{{ {description} }}\n\n")
            for functionName in self.FunctionDefinitions:
                func=self.FunctionDefinitions[functionName]
                params=", ".join([func.param_types[i]+" "+func.param_names[i]] for i in range(len(func.param_names)))
                f.write(f"define {func.retType} @{functionName}({params})")
                f.write("{\n")
                f.write(func.block)
                f.write("}\n\n")


            
