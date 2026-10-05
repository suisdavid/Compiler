from dataclasses import dataclass,field
from semantic.errors import SemanticError
from frontend.generated import ast_nodes
@dataclass
class Object:
    type: str

@dataclass
class Basic(Object):# basic types,i32,u32,isize,usize,bool,()
    value: int

@dataclass
class Array(Object):# [T;length]
    T: Object
    length: int
    elements: list[Object]

@dataclass
class Struct(Object):
    outerAttributes:list[str] #Copy,Clone,PartialEq,Eq
    fields:dict[str,Object]

@dataclass
class Box(Object):#Box<T>, supports new
    T: Object
    value: Object

@dataclass
class Vec(Object):#Vec<T>, supports new,len,is_empty,push,remove
    T: Object
    elements:list[Object]
    def len(self):
        return len(self.elements)
    def is_empty(self):
        return len(self.elements)==0
    def push(self,value: Object):
        if value.type!=self.type: #can be determined in compilation
            raise SemanticError(f"wrong type! {value.type} != {self.T.type}")
        self.elements.append(value)
    def remove(self,index:int):#check index in runtime
        return self.elements().pop(index)
        

@dataclass
class Reference(Object):# &T
    value: Object
    mut:bool #whether mutable reference

@dataclass
class Variable:
    mut: bool
    value: Object

@dataclass
class FunctionInfo:
    name: str
    self: ast_nodes.SelfParam
    returnType: Object
    params: dict[str,Variable]#can be mutable
    body: ast_nodes.BlockExpression


@dataclass
class Scope:
    values: dict[str,Variable]
    parent: Scope=None
    def registered(self,name: str, value: Object): #check registered in advance
        scope=self
        while scope!=None and scope.values.get(name)==None:
            scope=scope.parent
        return scope
    
    def register(self,name: str, mut: bool, value: Object): #check registered in advance
        self.values[name]=Variable(mut=mut,value=value)

    def get(self,name: str):
        scope=self.registered(name)
        if scope==None:
            raise SemanticError(f"name not registered! {name}")
        return scope.values[name].value

    def update(self, name: str, value: Object):
        scope=self.registered(name)
        if scope==None:
            raise SemanticError(f"name not registered! {name}")
        if value.type!=scope.values[name].type:
            raise SemanticError(f"wrong type! {value.type} != {self.values[name].type}")
        if not scope.values[name].mut:
            raise SemanticError(f"not mutable! {name}")
        scope.values[name].value=value



    

