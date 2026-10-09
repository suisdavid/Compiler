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
    value: Object

@dataclass
class Vec(Object):#Vec<T>, supports new,len,is_empty,push,remove
    elements:list[Object]
    def len(self):
        return len(self.elements)
    def is_empty(self):
        return len(self.elements)==0
    def push(self,value: Object):
        if value.type!=self.type: #can be determined in compilation
            raise SemanticError(f"wrong type! {value.type} != {self.type[4:-1]}")
        self.elements.append(value)
    def remove(self,index:int):#check index in runtime
        return self.elements().pop(index)
        

@dataclass
class Reference(Object):# &T
    addr: str #the name of the variable it points to.
    mut:bool #whether mutable reference

@dataclass
class Type:
    mut:bool
    mut_blocked:bool #used for reference
    left:bool #whether left value
    type:str #function starts with #

@dataclass
class Variable(Type):#every variable（including function) has a name!
    name: str

@dataclass
class FunctionInfo:
    name: str
    self: ast_nodes.SelfParam
    returnType: Object
    paramNames: list[str]
    params: list[Variable]#can be mutable
    body: ast_nodes.BlockExpression

@dataclass
class LoopContext:
    loop:str #loop,while
    has_break: bool
    retType:str

@dataclass
class Scope:
    values: dict[str,Variable]#functions sit in global scope
    parent: Scope=None
    def registered(self,name: str): 
        scope=self
        while scope!=None and scope.values.get(name)==None:
            scope=scope.parent
        return scope
    
    def register(self,name:str,variable:Variable): #check registered in advance
        if self.values.get(name):
            raise SemanticError(f"name already registered! {name}")
        self.values[name]=variable

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



    

