from dataclasses import dataclass,field
from semantic.errors import SemanticError
from frontend.generated import ast_nodes
from semantic.scope import *

class Checker:
    def __init__(self,crate:ast_nodes.Crate):
        self.crate=crate
        self.FunctionDefinitions={}#FunctionDefinition[function_name]->FunctionInfo
        self.ConstValues={}#same->Basic
        self.StructDefinitions={}#same->Struct
        self.ConstantLocations={}#identifier->(type:str,ConstValue)
        self.StructLocations={}#identifier->(type:str,StructDefinition)
        self.FunctionLocations={}#identifier->(type:str,FunctionDefinition)
        self.vis={}#use in dfs

    def RegisterConstant(self, constant: ast_nodes.ConstantItem,impl=None):
        if impl==None and constant.identifier in ["get_i32", "print_i32","println_i32"]:
            raise SemanticError(f"{constant.identifier} is reserved!")
        name=impl+"::"+constant.identifier if impl else constant.identifier
        if self.ConstantLocations.get(name):
           raise SemanticError(f"constant {name} already registered!")
        typeref=constant.typeref
        if not isinstance(typeref,ast_nodes.TypePath):
                raise SemanticError("wrong constant type!") 
        if len(typeref.typePathSegments)!=1:
            raise SemanticError("wrong type! RX doesn't support !=1 typePathSegments") 
        segment=typeref.typePathSegments[0]
        type=segment.identifier
        if type!='isize' and type!='usize' and type!='u32' and type!='i32' and type!='bool':
            raise SemanticError(f"{type} not basic type!")
        if len(segment.genericArgs)!=0:
            raise SemanticError(f"wrong type! {len(segment.genericArgs)} arguments inside {segment.identifier} instead of 0!")
        self.ConstantLocations[name]=(type,constant.constValue)

    def RegisterStruct(self, struct: ast_nodes.StructDefinition):
        if struct.identifier=="i32":
            raise SemanticError(f"{struct.identifier} is reserved!")
        if self.StructLocations.get(struct.identifier):
            raise SemanticError(f"struct {struct.identifier} already registered!")
        self.StructLocations[struct.identifier]=struct

    def RegisterFunction(self, function: ast_nodes.FunctionDefinition,impl=None):
        if function.identifier in ["get_i32", "print_i32", "println_i32"]:
            raise SemanticError(f"{function.identifier} is reserved!")
        name=impl+"::"+function.identifier if impl else function.identifier
        if self.FunctionLocations.get(name):
            raise SemanticError(f"function {name} already registered!")
        self.FunctionLocations[name]=function

    def ParseBasic(self, name:str):
        if name=='i32' or name=='u32' or name=='()' or name=='isize' or name=='usize' or name=='bool':
            return Basic(type=name,value=0)
        else:
            raise SemanticError(f"wrong type! {name} not basic type!")

    def ParseConstantItem(self,name:str,constvalue:ast_nodes.ConstValue,mustbe:str):
        if self.ConstValues.get(name):
             return self.ConstValues[name]
        if self.vis.get(name)==1:
             raise SemanticError("loop detected in constantItems!")
        self.vis[name]=1
        if constvalue.pathInExpression:
            path=constvalue.pathInExpression
            if len(path.typePathSegments)!=1:
                raise SemanticError("wrong type! RX doesn't support !=1 typePathSegments") 
            segment=path.typePathSegments[0]
            if len(segment.genericArgs)!=0:
                raise SemanticError(f"wrong type! {len(segment.genericArgs)} arguments inside {segment.identifier} instead of 0!")
            next_name=segment.identifier
            #handle Self
            if next_name.startswith("Self::"):
                if "::" in name:
                    next_name=name[:name.index("::")]+next_name[4:]
                else:
                    raise SemanticError(f"undefined Self! {next_name}") 
            if not self.ConstantLocations.get(next_name):
                raise SemanticError(f"undefined constant! {next_name}") 
            next_type,constValue=self.ConstantLocations[next_name]
            basicValue=self.ParseConstantItem(next_name,self.ConstantLocations[next_name],next_type)
            constvalue.type=basicValue.type
            constvalue.value=basicValue.value
        if (constvalue.type=='u32' or constvalue.type=='usize' or constvalue.type=='bool' or mustbe=='u32' or mustbe=='usize' or mustbe=='bool') and constvalue.minus:
            raise SemanticError("cannot use - for unsigned types!")
        if constvalue.type and mustbe and constvalue.type!=mustbe:
             raise SemanticError(f"unaligned types! {constvalue.type}!={mustbe}")
        if mustbe=='bool' and not constvalue.type:
            raise SemanticError(f"boolean conversion not available")
        self.vis[name]=0
        result=Basic(type=constvalue.type or mustbe,value=(-constvalue.value)%(1<<32) if constvalue.minus else constvalue.value)
        if name and not name.endswith("::"):#for compatability with ParseConst
            self.ConstValues[name]=result
        return result
    
    def ParseConst(self,constvalue:ast_nodes.ConstValue,mustbe=None,impl=None):
        return self.ParseConstantItem(impl+"::" if impl else "",constvalue,mustbe)
    
    def ParseTypeRef(self,typeref:ast_nodes.TypeRef,impl=None):#return Object
        if isinstance(typeref,ast_nodes.TypePath):
            if len(typeref.typePathSegments)!=1:
                raise SemanticError("wrong type! RX doesn't support !=1 typePathSegments")
            segment=typeref.typePathSegments[0]
            if segment.identifier=='Vec' or segment.identifier=='Box':
                if len(segment.genericArgs)!=1:
                    raise SemanticError(f"wrong type! {len(segment.genericArgs)} arguments inside {segment.identifier} instead of 1!")
                T=self.ParseTypeRef(segment.genericArgs[0])
                return Vec(type='Vec<'+T.type+'>',T=T,elements=[]) if segment.identifier=='Vec' else Box(type='Box<'+T.type+'>',T=T)
            else:
                if len(segment.genericArgs)!=0:
                    raise SemanticError(f"wrong type! {len(segment.genericArgs)} arguments inside {segment.identifier} instead of 0!")
                if segment.identifier in ["i32","u32","isize","usize","bool"]:
                    return self.ParseBasic(segment.identifier)
                elif self.StructLocations.get(segment.identifier):
                    return self.ParseStruct(self.StructLocations[segment.identifier])
                else:
                    raise SemanticError(f"{segment.identifier} not defined!")
        elif isinstance(typeref,ast_nodes.ReferenceType):
            T=self.ParseTypeRef(typeref.inner)
            return Reference(mut=typeref.mut,value=T,type='&'+('mut ' if typeref.mut else ' ')+T.type)
        elif isinstance(typeref,ast_nodes.ArrayType):
            T=self.ParseTypeRef(typeref.inner)
            length=self.ParseConst(typeref.length,mustbe='usize',impl=impl)
            return Array(T=T,length=length.value,type=f'[{T.type};{length.value}]',elements=None)
        else:
            return Basic(type='()',value=0)
                                
    def ParseStruct(self,struct:ast_nodes.StructDefinition):
        name=struct.identifier
        if self.StructDefinitions.get(name):
            return self.StructDefinitions[name]
        if self.vis.get(name)==1:
            raise SemanticError("loop detected in structDefinitions!")
        self.vis[name]=1
        fields={}
        for structField in struct.fields:
            if fields.get(structField.identifier):
                raise SemanticError(f"{structField.identifier} already defined in struct {name}")
            fields[structField.identifier]=self.ParseTypeRef(structField.typeref)
        self.vis[name]=0
        result=Struct(type=name,outerAttributes=struct.outerAttributes,fields=fields)
        self.StructDefinitions[name]=result
        return result

    def ParseFunction(self,name:str,function:ast_nodes.FunctionDefinition):#return functionInfo
        params={}
        if function.functionParameters:
            for each in function.functionParameters.parameters:
                if params.get(each.identifier):
                    raise SemanticError(f"parameter {each.identifier} repeated in function {name}")
                params[each.identifier]=Variable(mut=each.mut,value=self.ParseTypeRef(each.typeref))

        result=FunctionInfo(name=name,self=function.functionParameters.selfParam if function.functionParameters else None,params=params,returnType=self.ParseTypeRef(function.typeref),body=function.blockExpression)
        self.FunctionDefinitions[name]=result
        return result
    
    def SymbolCollection(self):
        #register
        for item in self.crate.Items:
            if isinstance(item,ast_nodes.ConstantItem):
                self.RegisterConstant(item)
            elif isinstance(item,ast_nodes.StructDefinition):
                self.RegisterStruct(item)
            elif isinstance(item,ast_nodes.FunctionDefinition):
                self.RegisterFunction(item)

        for item in self.crate.Items:
            if isinstance(item,ast_nodes.InherentImpl):
                typeref=item.typeRef
                if not isinstance(typeref,ast_nodes.TypePath):
                    raise SemanticError("wrong impl type!") 
                if len(typeref.typePathSegments)!=1:
                    raise SemanticError("wrong type! RX doesn't support >1 typePathSegments")
                segment=typeref.typePathSegments[0]
                if not self.StructLocations.get(segment.identifier):
                    raise SemanticError(f"{segment.identifier} not registered!")
                if len(segment.genericArgs)!=0:
                    raise SemanticError(f"wrong type! {len(segment.genericArgs)} arguments inside {segment.identifier} instead of 0!")
                name=segment.identifier
                for each in item.associatedItems:
                    if isinstance(each,ast_nodes.ConstantItem):
                        self.RegisterConstant(each,impl=name)
                    else:
                        self.RegisterFunction(each,impl=name)


        #parse constants
        for name in self.ConstantLocations:
            type,constValue=self.ConstantLocations[name]
            self.ParseConstantItem(name,constValue,type)

        #parse structs
        self.vis={}
        for name in self.StructLocations:
            self.ParseStruct(self.StructLocations[name])

        #parse functions
        self.vis={}
        for name in self.FunctionLocations:
            self.ParseFunction(name,self.FunctionLocations[name])



                            


