from __future__ import annotations
from dataclasses import dataclass,field
from frontend.generated import ast_nodes
from semantic.scope import *

@dataclass
class IRType:
    type:str#concrete type defined in SemanticCheck
    identifier:str#begin with % 

@dataclass
class IRStruct:#basic struct names or vec
    identifier: str
    field_names: list[str]
    field_types: list[str]

@dataclass
class IRVec(IRStruct):
    T: str
    #field: length(i32), cap(i32), T_length(i32),base(ptr)
    def push(self,x:IRType):
        pass

    def remove(self,idx:int)->IRType:
        pass

    def len(self):
        pass

    def is_empty(self):
        pass

@dataclass
class IRBlock:
    identifier:str #block name
    statements:str #statements in block

@dataclass
class IRFunction:
    identifier:str #function name
    retType:str
    param_names:list[str]
    param_types:list[str]
    blocks:list[IRBlock]


@dataclass
class IRScope:
    vars: dict[str,IRType]
    parent:IRScope
    def registered(self,name: str): 
        scope=self
        while scope!=None and scope.vars.get(name)==None:
            scope=scope.parent
        return scope
        
    def register(self,name:str,type:IRType): 
        self.values[name]=type
    
        def get(self,name: str):
            scope=self.registered(name)
            if scope==None:
                raise SemanticError(f"name not registered! {name}")
            return scope.values[name]
    

