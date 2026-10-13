from __future__ import annotations
from dataclasses import dataclass,field
from frontend.generated import ast_nodes
from semantic.scope import *
from semantic.checker import Checker
from ir.model import *


class Builder:
    def __init__(self,crate:ast_nodes.Crate,checker:Checker,output:str):
        self.StructDefinitions={}#structName(str)->IRStruct
        self.FunctionDefinitions={}#functionName(str)->IRFunction
        self.FunctionNewNames={}#functionName in checker->functionName in IR
        self.checker=checker#already done SemanticCheck
        self.output=output#output_path
        self.crate=crate
        self.tempctr=0
        self.varctr=0
        self.funcctr=0

    def GenTempName(self)->str:#generate a temporary variable
        self.tempctr+=1
        return f"%temp{self.tempctr}"
    
    def GenVarName(self)->str:#generate a local variable
        self.varctr+=1
        return f"%var{self.varctr}"
    
    def GetIRType(self,type:str)->str:
        if type.startswith("&") or type.startswith("Box<"):
            return "ptr"
        elif type.startswith("Vec"):
            return "%Vec"
        elif type=="()":
            return "%Unit"
        elif type in ["i32","u32","isize","usize"]:
            return "i32"
        elif type=="bool":
            return "i1"
        else:
            return "%"+type

    def BuildAndStore(var1:str,var2:str,type:str)->str:#store var2's value into var1
        return f"   {var1} = alloca {type}\n   store {type} {var2}, ptr {var1}\n"#statement format: Tab{statement}\n
    
    def Store(var1:str,var2:str,type:str)->str:#store var2's value into var1
        return f"store {type} {var2}, ptr {var1}\n    "
    
    def ParseExpression(self,scope:IRScope,expression:ast_nodes.Expression,block_name:str,break_name:str=None,continue_name:str=None):

    def Build(self):
        self.StructDefinitions["Vec"]=IRStruct(identifier="Vec",field_names=["length","cap","T_length","base"],field_types=["i32","i32","i32","ptr"])
        self.StructDefinitions["Unit"]=IRStruct(identifier="Unit",field_names=[],field_types=[])
        #Box<T> is just ptr

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
            self.tempctr=self.varctr=0
            self.funcctr+=1
            newFuncName=f"func{self.funcctr}" if functionName!="main" else "main"
            self.FunctionNewNames[functionName]=newFuncName
            param_names=[]
            param_types=[]
            paramctr=0
            self.blocks={"entry":IRBlock(identifier="entry",statements="")}
            self.blockOrder=["entry"]
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
            self.FunctionDefinitions[newFuncName]=IRFunction(identifier=functionName,retType=self.GetIRType(func.returnType.type),param_names=param_names,param_types=param_types,blocks=func_blocks)
             



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
                for block in func.blocks:
                    f.write(f"{block.identifier}:\n")
                    f.write(block.statements)
                f.write("}\n\n")


            
