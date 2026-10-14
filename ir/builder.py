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

    def CountPtr(self,type:str)->int:
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
    
    def GetIRType(self,type:str)->str:
        if type.startswith("&") or type.startswith("Box<") or type.startswith("["):
            return "ptr"
        elif type.startswith("Vec<"):
            return "%Vec"
        elif type=="()":
            return "%Unit"
        elif type in ["i32","u32","isize","usize"]:
            return "i32"
        elif type=="bool":
            return "i1"
        else:
            return "%"+type
    
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
                innerType=type[1:type.index(";")]
                length=int(type[type.index(";")+1:-1])
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
            s+=f"   {temp} = load {self.GetIRType(lasttype)}, ptr {last}\n"
            last=temp
        return s,last
    
    def BuildAndStore(self,var1:str,var2:str,type:str)->str:#store var2's value into var1
        return f"   {var1} = alloca {type}\n   store {type} {var2}, ptr {var1}\n"#statement format: Tab{statement}\n
    
    def Store(self,var1:str,var2:str,type:str)->str:#store var2's value into var1
        return f"   store {type} {var2}, ptr {var1}\n"

    def Calc(self,type1:IRType,type2:IRType,op:str):#return str,IRType
        s=""
        temp=""
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
            return s+f"    store {self.GetIRType(type1.type)} {temp}, ptr {type1.left}\n",IRType(type="()",identifier=None)
        
        elif op in self.comparisonOps:
            temp=self.GenTempName()
            if op in ['==','!=']:
                s=f"   {temp} = icmp {("eq" if op=='==' else "ne")} {self.GetIRType(type1.type)} {type1.identifier},{type2.identifier}\n"
            
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
                
            return s,IRType(type="bool",identifier=temp)

        elif op in self.logicOps:
            temp=self.GenTempName()
            return f"   {temp} = {op} i1 {type1.identifier}, {type2.identifier}\n",IRType(type="bool",identifier=temp)

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
            return s,IRType(type=type,identifier=temp)
        
        elif op in self.unaryOps:#type2=None
            if op=='minus':
                temp=self.GenTempName()
                cnt,type=self.CountPtr(type1.type)
                s1,temp1=self.Dereference(type1,cnt=self.CountPtr(type1.type))
                s=s1+f"    {temp} = sub i32 0, {temp1}\n"
                return s,IRType(type=type,identifier=temp)
            elif op=='!':
                temp=self.GenTempName()
                cnt,type=self.CountPtr(type1.type)
                s1,temp1=self.Dereference(type1,cnt=cnt)
                s=s1+(f"    {temp} = xor i1 {temp1}, true\n" if type=="bool" else f"    {temp} = xor i32 {temp1}, -1\n")
                return s,IRType(type=type,identifier=temp)
            elif op=="star":
                s,temp=self.Dereference(type1)
                return s,IRType(type=type1.type[2:],identifier=temp)
            else:#&
                temp=self.GenTempName()
                return self.BuildAndStore(temp,type1.identifier,self.GetIRType(type1.type)),IRType(type="& "+type1.type,identifier=temp)

    def Clone(self,type:IRType,res:str,block_name:str):#clone struct to res(ptr,already alloced),return s,block_name
        s=""
        if type.type=="()":#nothing should happen
            return s,block_name
        elif type.type in self.basicTypes or type.type.startswith("& "):
            return f"store {self.GetIRType(type)} {type.identifier}, ptr {res}\n",block_name
        elif type.type.startswith("Box<"):
            dest=self.GenTempName()
            src=self.GenTempName()
            alloc_type=self.GetAllocType(innerType)
            innerType=type.type[4:-1]
            s=f'''{src} = load {self.GetIRType(innerType)}, ptr {type.identifier}\n
                {dest} = alloca {alloc_type}\n'''
            news,block_name=self.Clone(IRType(type=innerType,identifier=src),dest,block_name)
            return s+news+f"    store ptr {dest}, ptr {res}\n",block_name
        elif type.type.startswith("["):
            length=int(type.type[type.type.index(";")+1:-1])
            innerType=type[1:type.type.index(";")]
            alloc_type=self.GetallocType(innerType)
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
                {source} = getelementptr [{length} x {alloc_type}], ptr {type.identifier}, i32 0, i32 {temp1}
                {src} = load {{self.GetIRType(innerType)}}, ptr {source}
                {dest} = getelementptr [{length} x {alloc_type}], ptr {res}, i32 0, i32 {temp1}\n'''    
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
            struct=self.StructDefinitions['Vec']
            for i in range(3):
                temp=self.GenTempName()
                src=self.GenTempName()
                dest=self.GenTempName()
                s+=f'''{temp} = getelementptr %{struct}, ptr {type.identifier}, i32 0, i32 {i}
                    {src} = load {self.GetIRType(struct.field_types[i])}, ptr {temp}
                    {dest} = getelementptr %{struct}, ptr {res}, i32 0, i32 {i}\n'''
                news,block_name=self.Clone(IRType(type=struct.field_types[i],identifier=src),dest,block_name)
                s+=news
            temp=self.GenTempName()
            length=self.GenTempName()
            loop_block=self.GenBlockName()
            ctr=self.GenTempName()
            source=self.GenTempName()
            src=self.GenTempName()
            dest=self.GenTempName()
            temp1=self.GenTempName()
            temp2=self.GenTempName()
            temp3=self.GenTempName()
            temp4=self.GenTempName()
            temp5=self.GenTempName()
            cap=self.GenTempName()
            condition=self.GenTempName()
            pointer=self.GenTempName()
            new_res=self.GenTempName()
            alloc_type=self.GetAllocType(innerType)
            s+=f'''
                {temp} = getelementptr %Vec, ptr {type.identifier}, i32 0, i32 0
                {length} = load i32, ptr {temp}
                {temp3} = getelementptr %Vec, ptr {type.identifier}, i32 0, i32 3
                {pointer} = load ptr, ptr {temp3}
                {temp4} = getelementptr %Vec, ptr {res}, i32 0, i32 3
                {temp5} = getelementptr %Vec, ptr {res}, i32 0, i32 3
                {new_res} = load ptr, ptr {temp5}
                {ctr} = alloca i32
                store i32 0, ptr {ctr}
            {loop_block}:
                {temp1} = load i32, ptr {ctr}
                {source} = getelementptr {alloc_type}, ptr {pointer}, i32 0, i32 {temp1}
                {src} = load {self.GetIRType(innerType)}, ptr {source}
                {dest} = getelementptr {alloc_type}, ptr {new_res}, i32 0, i32 {temp1}\n'''    
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
                temp=self.GenTempName()
                src=self.GenTempName()
                dest=self.GenTempName()
                s+=f'''{temp} = getelementptr %{struct}, ptr {type.identifier}, i32 0, i32 {i}
                    {src} = load {self.GetIRType(struct.field_types[i])}, ptr {temp}
                    {dest} = getelementptr %{struct}, ptr {res}, i32 0, i32 {i}\n'''
                news,block_name=self.Clone(IRType(type=struct.field_types[i],identifier=src),dest,block_name)
                s+=news
            return s,block_name




                
                
    def VecOp(self,type:IRType,innerType:str,func_name:str):
        temp=self.GenTempName()
        if func_name=="len":
            temp1=self.GenTempName()
            s="   {temp1} = getelementptr %S, ptr {type.identifier}, i32 0, i32 0\n    {temp} = load i32, ptr {temp1}\n"
            return s,IRType(type="usize",identifier=temp)

        else#clone



                                    
                                            
                                    
                

    def ParseExpression(self,scope:IRScope,expression:ast_nodes.Expression,block_name:str,break_name:str=None,continue_name:str=None)->IRType:
        if isinstance(expression,ast_nodes.PrimitiveExpression):
            if expression.op in self.assignmentOps or expression.op in self.comparisonOps:
                type0=self.ParseExpression(scope,expression.expressions[0],block_name,break_name=break_name,continue_name=continue_name)
                type1=self.ParseExpression(scope,expression.expressions[1],block_name,break_name=break_name,continue_name=continue_name)
                s,type=self.Calc(type0,type1,expression.op)
                self.block+=s
                return type
            elif expression.op in self.logicOps or expression.op in self.arithmeticOps:
                type0=self.ParseExpression(scope,expression.expressions[0],block_name,break_name=break_name,continue_name=continue_name)
                for i in range(1,len(expression.expressions)):
                    type1=self.ParseExpression(scope,expression.expressions[i],block_name,break_name=break_name,continue_name=continue_name)
                    s,type0=self.Calc(type0,type1,expression.op if expression.op in self.logicOps else expression.ops[i-1])
                    self.block+=s
                return type0
        elif isinstance(expression,ast_nodes.UnaryExpression):
            type0=self.ParseExpression(scope,expression.postfixExpression,block_name,break_name=break_name,continue_name=continue_name)
            for op in expression.ops[::-1]:
                if op=='&&' or op=="&&mut":
                    s,type0=self.Calc(type0,None,"&")
                    self.block+=s
                    s,type0=self.Calc(type0,None,"&")
                    self.block+=s
                else:
                    s,type0=self.Calc(type0,None,op)
                    self.block+=s
            return type0

        elif isinstance(expression,ast_nodes.CastExpression):
            type0=self.ParseExpression(scope,expression.unaryExpression,block_name,break_name=break_name,continue_name=continue_name)
            type1=expression.typeRefs[-1].typePathSegments[0].identifier #must be i32
            if type0.type=="bool":
                temp=self.GenTempName()
                self.block[block_name]+=f'    {temp} = zext i1 {type0.identifier} to i32\n'
                type0.identifier=temp
            return IRType(type=type1,identifier=type0.identifier)

        elif isinstance(expression,ast_nodes.PostfixExpression):
            type0=self.ParseExpression(scope,expression.primaryExpression,block_name,break_name=break_name,continue_name=continue_name)
            for suffix in expression.postfixSuffixes:
                if isinstance(suffix,ast_nodes.CallArguments):
                    #if type0 is a function, type0.type is function old name, type0.identifier is self variable(if exists)
                    if type0.type.startswith("Vec<"):#vec
                        s,temp=self.VecOp(type0,type0.type[4:type0.type.index(">")],type0.type[type0.type.index("::")+2:])
                        self.block[block_name]+=s
                    elif type0.type.startswith("Box<"):
                        #clone

                    else:
                                        
                                        if type.count("::")==1 and type[type.index("::")+2:]=="clone":#if defined clone, use the user-defined clone
                                            structName=type[:type.index("::")]
                                            if self.CheckAttribute(structName,"Clone"):
                                                if len(suffix.expressions)!=1:
                                                    raise SemanticError(f"param number not align!  {len(suffix.expressions)}!=1")
                                                self.ParseExpression(scope,suffix.expressions[0],expected=f"& {structName}",impl=impl,inloop=inloop)
                                                type0=Type(mut=False,mut_blocked=False,left=False,type=structName)
                                            else:
                                                raise SemanticError(f"struct {structName} cannot clone!")
                                        else:
                                            raise SemanticError(f"function {type} does not exist!")
                                    else:
                                        has_self=(func.self is not None)
                                        if len(suffix.expressions)!=len(func.paramNames)+has_self:
                                            raise SemanticError(f"param number not align!  {len(suffix.expressions)}!={len(func.paramNames)+has_self}")
                                        for i in range(has_self,len(suffix.expressions)):
                                            self.ParseExpression(scope,suffix.expressions[i],expected=func.params[i-has_self].type,impl=impl,inloop=inloop)
                                        if has_self:
                                            self_type=("&mut " if (func.self.amp and func.self.mut) else ("& " if func.self.amp else ""))+func.name[:func.name.index("::")]#impl
                                            self.ParseExpression(scope,suffix.expressions[0],expected=self_type,impl=impl,inloop=inloop)
                                        type0=Type(mut=False,mut_blocked=False,left=False,type=func.returnType.type if func.returnType else "()")
                            else:
                                raise SemanticError(f"not function! {type0.type}")
                        elif isinstance(suffix,ast_nodes.BracketSuffix):
                            type=self.dereference(type0)
                            if not type.left:#materialize right value
                                type.left = True
                                type.mut = not type.mut_blocked
                            if type.type.startswith("Vec<") or type.type.startswith("["):
                                self.ParseExpression(scope,suffix.expression,expected='usize',impl=impl,inloop=inloop)
                                type0=Type(mut=type.mut,mut_blocked=type.mut_blocked if type.type.startswith("[") else (type.mut_blocked or not type.mut),left=True,type=self.GetArrayInner(type.type)[0] if type.type.startswith("[") else type.type[4:-1])
                            else:
                                raise SemanticError(f"not array! {type0.type}")
                        elif isinstance(suffix,ast_nodes.DotSuffix):
                            type=self.dereference(type0).type
                            struct=self.StructDefinitions.get(type)
                            if (not struct or not self.FunctionDefinitions.get(type+"::clone")) and isinstance(suffix,ast_nodes.DotSuffixMethod) and suffix.pathExprSegment.identifier=="clone" and not suffix.pathExprSegment.genericArgs and len(suffix.callarguments.expressions)==0:#special check for built-in clone!
                                type0=Type(mut=False,mut_blocked=False,left=False,type=self.GetClone(type0.type))
                            elif self.dereference(type0).type.startswith("[") and isinstance(suffix,ast_nodes.DotSuffixMethod) and suffix.pathExprSegment.identifier=="len" and not suffix.pathExprSegment.genericArgs and  len(suffix.callarguments.expressions)==0:#len
                                type0=Type(mut=False,mut_blocked=False,left=False,type="usize")
                            else:
                                type0=self.dereference(type0)
                                if not type0.left:
                                    type0.left = True
                                    type0.mut = not type0.mut_blocked
                                if not struct and not type.startswith("Vec<") and not type.startswith("Box<") :
                                    raise SemanticError(f"struct {type} does not exist!")
                                if isinstance(suffix,ast_nodes.DotSuffixData):
                                    if type.startswith("Vec<") or type.startswith("Box<"):
                                        raise SemanticError("Vec or Box has not data member!")
                                    structField=struct.fields.get(suffix.identifier)
                                    if not structField:
                                        raise SemanticError(f"field {suffix.identifier} does not exist in struct {type}!")
                                    type0=Type(mut=type0.mut and not type0.mut_blocked,mut_blocked=type0.mut_blocked,left=True,type=structField.type)
                                elif isinstance(suffix,ast_nodes.DotSuffixMethod):
                                    arguments=suffix.callarguments
                                    if suffix.pathExprSegment.genericArgs:
                                        raise SemanticError(f"function {type}::{suffix.pathExprSegment.identifier} has genericArgs!")
                                    if type.startswith("Vec<") or type.startswith("Box<"):
                                        type0=self.CheckVecBox(type[:3],suffix.pathExprSegment.identifier,scope,suffix.callarguments.expressions,type[4:-1],impl=impl,inloop=inloop,type0=type0)
                                    else:
                                        func=self.FunctionDefinitions.get(type+"::"+suffix.pathExprSegment.identifier)
                                        if not func:
                                            raise SemanticError(f"function {type}::{suffix.pathExprSegment.identifier} does not exist!")
                                        if not func.self:
                                            raise SemanticError(f"function {type}::{suffix.pathExprSegment.identifier} does not have self param!")
                                        if func.self.mut and func.self.amp and (not (type0.mut and not type0.mut_blocked)):
                                            raise SemanticError("not mut self!")
                                        if len(arguments.expressions)!=len(func.paramNames):
                                            raise SemanticError(f"param number not align!  {len(arguments.expressions)}!={len(func.paramNames)}")
                                        for i in range(len(arguments.expressions)):
                                            self.ParseExpression(scope,arguments.expressions[i],expected=func.params[i].type,impl=impl,inloop=inloop)
                                        type0=Type(mut=False,mut_blocked=False,left=False,type=func.returnType.type if func.returnType else "()")
                    if expected:
                        if not self.CanTransform(type0.type,expected,type0.mut_blocked):
                            raise SemanticError(f"expression type error! {type0.type} != {expected}")
                        type0.type=expected
                    return type0
        


    def Build(self):
        self.StructDefinitions["Vec"]=IRStruct(identifier="Vec",field_names=["length","cap","T_length","base"],field_types=["i32","i32","i32","ptr"])
        self.StructDefinitions["Unit"]=IRStruct(identifier="Unit",field_names=[],field_types=[])
        #Box<T> is special ptr

        for structName in self.checker.StructOrder:
            struct=self.checker.StructDefinitions[structName]
            field_names=[]
            field_types=[]
            for field_name in struct.fields:
                field_names.append(field_name)
                field_types.append(self.GetIRType(struct.fields[field_name].type))
            self.StructDefinitions[structName]=IRStruct(identifier=structName,field_names=field_names,field_types=field_types)

        for functionName in self.checker.FunctionDefinitions:
            func=self.checker.FunctionDefinitions[functionName]
            self.tempctr=self.varctr=self.blockctr=0
            self.funcctr+=1
            newFuncName=f"func{self.funcctr}" if functionName!="main" else "main"
            self.FunctionNewNames[functionName]=newFuncName
            param_names=[]
            param_types=[]
            paramctr=0
            self.block="entry:\n"
            function_scope=IRScope(vars={},parent=None)
            #register function parameters
            if func.self:
                impl=functionName[:functionName.index("::")]
                paramctr+=1
                varname=self.GenVarName()
                param_names.append("%param1")
                param_types.append("ptr" if func.self.amp else f"%{impl}")
                function_scope.register("self",IRType(identifier=varname,type=impl if not func.self.amp else (f'& {impl}' if not func.self.mut else f'&mut {impl}')))
                self.blocks["entry"].statements+=self.BuildAndStore(varname,f"%param{paramctr}",param_types[-1])
            for i in range(len(func.paramNames)):#function params should have addr
                paramctr+=1
                varname=self.GenVarName()
                param_names.append(f"%param{paramctr}")
                param_types.append(self.GetIRType(func.params[i].type))
                function_scope.register(func.paramNames[i],IRType(identifier=varname,type=func.params[i].type))
                self.blocks["entry"].statements+=self.BuildAndStore(varname,f"%param{paramctr}",param_types[-1])
            self.ParseExpression(function_scope,func.body,"entry")
            func_blocks=[]
            for each in self.blockOrder:
                func_blocks.append(self.blocks[each])
            self.FunctionDefinitions[newFuncName]=IRFunction(identifier=functionName,retType=self.GetIRType(func.returnType.type),param_names=param_names,param_types=param_types,block=self.block)
             



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


            
