from dataclasses import dataclass,field
from semantic.errors import SemanticError
from frontend.generated import ast_nodes
from semantic.scope import *

class Checker:
    assignmentOps=["+=","-=",">>=","<<=","/=","%=","*=","=","&=","|=","^="]
    comparisonOps=[">","<","==","!=","<=",">="]
    logicOps=["and","or"]
    arithmeticOps=["+","-","*","/",'%',"<<",">>",'&',"|","^"]
    unaryOps=['minus','star','!','&','&mut']

    basicTypes=['i32','u32','usize','isize','bool']
    integers=['i32','u32','usize','isize']
    def __init__(self,crate:ast_nodes.Crate):
        self.crate=crate
        self.FunctionDefinitions={}#FunctionDefinition[function_name]->FunctionInfo
        self.ConstValues={}#same->Basic
        self.StructDefinitions={}#same->Struct
        self.ConstantLocations={}#identifier->(type:str,ConstValue)
        self.StructLocations={}#identifier->(type:str,StructDefinition)
        self.FunctionLocations={}#identifier->(type:str,FunctionDefinition)
        self.vis={}#use in dfs
    def GetArrayInner(self,s:str):
        idx=len(s)-1
        while s[idx]!=';':
            idx-=1
        return s[1:idx]
    
    def RegisterConstant(self, constant: ast_nodes.ConstantItem,impl=None):
        if impl==None and constant.identifier in ["get_i32", "print_i32","println_i32"]:
            raise SemanticError(f"{constant.identifier} is reserved!")
        name=impl+"::"+constant.identifier if impl else constant.identifier
        if self.ConstantLocations.get(name) or self.FunctionLocations.get(name):
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
        if len(struct.outerAttributes)!=len(list(set(struct.outerAttributes))):
            raise SemanticError(f"struct {struct.identifier} has repetitive outerAttributes!")
        if ("Copy" in struct.outerAttributes and "Clone" not in struct.outerAttributes) or ("Eq" in struct.outerAttributes and "PartialEq" not in struct.outerAttributes):
            raise SemanticError(f"struct {struct.identifier} has invalid outerAttributes!")
        self.StructLocations[struct.identifier]=struct

    def RegisterFunction(self, function: ast_nodes.FunctionDefinition,impl=None):
        if impl==None and function.identifier in ["get_i32", "print_i32", "println_i32"]:
            raise SemanticError(f"{function.identifier} is reserved!")
        name=impl+"::"+function.identifier if impl else function.identifier
        if self.ConstantLocations.get(name) or self.FunctionLocations.get(name):
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
            if len(path.typePathSegments)!=1 and len(path.typePathSegments)!=2:
                raise SemanticError("wrong type! RX only supports 1/2 typePathSegments") 
            segment=path.typePathSegments[-1]
            if len(segment.genericArgs)!=0:
                raise SemanticError(f"wrong type! {len(segment.genericArgs)} arguments inside {segment.identifier} instead of 0!")
            next_name=segment.identifier
            if len(path.typePathSegments)==2:#impl
                impl=path.typePathSegments[0]
                if len(impl.genericArgs)!=0:
                    raise SemanticError(f"wrong type! {len(impl.genericArgs)} arguments inside {impl.identifier} instead of 0!")
                if impl.identifier=='Self':
                    if "::" in name:
                        next_name=name[:name.index("::")]+"::"+next_name
                    else:
                        raise SemanticError(f"undefined Self! {next_name}") 
                else:
                    next_name=impl.identifier+"::"+next_name
                
            if not self.ConstantLocations.get(next_name):
                raise SemanticError(f"undefined constant! {next_name}") 
            next_type,next_value=self.ConstantLocations[next_name]
            basicValue=self.ParseConstantItem(next_name,next_value,next_type)
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
    
    def ParseTypeRef(self,typeref:ast_nodes.TypeRef,impl=None,typeonly=False,structName=None):#return Object
        if isinstance(typeref,ast_nodes.TypePath):
            if len(typeref.typePathSegments)!=1:
                raise SemanticError("wrong type! RX doesn't support !=1 typePathSegments")
            segment=typeref.typePathSegments[0]
            if segment.identifier=='Vec' or segment.identifier=='Box':
                if len(segment.genericArgs)!=1:
                    raise SemanticError(f"wrong type! {len(segment.genericArgs)} arguments inside {segment.identifier} instead of 1!")
                T=self.ParseTypeRef(segment.genericArgs[0],impl=impl,typeonly=True)
                return Vec(type='Vec<'+T.type+'>',elements=[]) if segment.identifier=='Vec' else Box(type='Box<'+T.type+'>',value=None)
            else:
                if len(segment.genericArgs)!=0:
                    raise SemanticError(f"wrong type! {len(segment.genericArgs)} arguments inside {segment.identifier} instead of 0!")
                if segment.identifier in ["i32","u32","isize","usize","bool"]:
                    return self.ParseBasic(segment.identifier)
                if segment.identifier=='Self':
                    if structName or impl:
                        segment.identifier=structName or impl
                    else:
                        raise SemanticError("use Self outside struct definition!")
                elif self.StructLocations.get(segment.identifier):
                    if typeonly:
                        return Struct(type=segment.identifier,outerAttributes=[],fields={})
                    else:
                        return self.ParseStruct(self.StructLocations[segment.identifier])
                else:
                    raise SemanticError(f"{segment.identifier} not defined!")
        elif isinstance(typeref,ast_nodes.ReferenceType):
            T=self.ParseTypeRef(typeref.inner,impl=impl,typeonly=True)
            return Reference(mut=typeref.mut,type='&'+('mut ' if typeref.mut else ' ')+T.type,name=None)
        elif isinstance(typeref,ast_nodes.ArrayType):
            T=self.ParseTypeRef(typeref.inner,impl=impl,typeonly=typeonly)
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
            fields[structField.identifier]=self.ParseTypeRef(structField.typeref,impl=None,typeonly=False,structName=None)
        self.vis[name]=0
        result=Struct(type=name,outerAttributes=struct.outerAttributes,fields=fields)
        self.StructDefinitions[name]=result
        return result

    def ParseFunction(self,name:str,function:ast_nodes.FunctionDefinition):#return functionInfo
        paramNames=[]
        params=[]
        impl=name[:name.index("::")] if "::" in name else None
        if "::" not in name and function.functionParameters and function.functionParameters.selfParam:
            raise SemanticError("top-level functions cannot have selfparam!")
        if function.functionParameters:
            for each in function.functionParameters.parameters:
                if each.identifier in paramNames:
                    raise SemanticError(f"parameter {each.identifier} repeated in function {name}")
                paramNames.append(each.identifier)
                params.append(Variable(mut=each.mut,mut_blocked=False,left=True,type=self.ParseTypeRef(each.typeref,impl=impl).type,name=name+"@"+each.identifier))#@ stands for scope change

        result=FunctionInfo(name=name,self=function.functionParameters.selfParam if function.functionParameters else None,paramNames=paramNames,params=params,returnType=self.ParseTypeRef(function.typeref,impl=impl) if function.typeref else None,body=function.blockExpression)
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
        #check main
        if not self.FunctionLocations.get("main"):
            raise SemanticError("main function not defined!")
        main=self.FunctionLocations["main"]
        if main.hasGeneric:
            raise SemanticError("main function cannot have genericArgs!")
        if main.functionParameters or main.typeref:
            raise SemanticError("main function has no arg or returnType")
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

    def CheckAttribute(self,type:str, attribute:str):
        while True:
            if type in self.basicTypes:
                return True
            if type.startswith("& "):
                if attribute in ["Copy","Clone"]:
                    return True
                else:
                    type=type[2:]
            elif type.startswith("&mut "):
                if attribute in ["Copy","Clone"]:
                    return False
                else:
                    type=type[2:]
            elif type.startswith("["):
                type=self.GetArrayInner(type)
            elif type.startswith("Box<") or type.startswith("Vec<"):
                if attribute=="Copy":
                    return False
                else:
                    type=type[4:-1]
            else:
                struct=self.StructDefinitions.get(type)
                if not struct:
                    raise SemanticError(f"struct {type} does not exist!")
                return attribute in struct.outerAttributes

    def dereference(self,type:str):
        while True:
            if type.startswith("& "):
                type=type[2:]
            elif type.startswith("&mut "):
                type=type[5:]
            elif type.startswith("Box<"):
                type=type[4:-1]
            else:
                return type
            
    def CanTransform(self,right:str,left:str):#type already fixed 
        if right==left or right=='^':#^ for never type
            return True
        if left.startswith("&mut "):
            if right.startswith("&mut "):
                S=right[5:]
                T=left[5:]
                while S!=T:
                    if S.startswith("Box<"):
                        S=S[4:-1]
                    elif S.startswith("&mut "):
                        S=S[5:]
                    else:
                        return False
                return True
            else:
                return False
        elif left.startswith("& "):
            if not right.startswith("&"):
                return False
            S=right[2:] if right.startswith("& ") else right[5:]
            T=left[2:]
            while S!=T:
                if S.startswith("Box<"):
                    S=S[4:-1]
                elif S.startswith("&mut "):
                    S=S[5:]
                elif S.startswith("& "):
                    S=S[2:]
                else:
                    return False
            return True
        else:
            return False
    
    def CheckOp(self,type0:Type,type1:Type,op:str):#type already fixed
        if type0.type.startswith("#") or (type1 and type1.type.startswith("#")):
            raise SemanticError(f"operations with functions! {type0.type} {type1.type}")
        if op in self.assignmentOps:
            if type0.left==False or type0.mut==False:
                raise SemanticError(f"different types cannot op! {type0.type} {op} {type1.type}")
            if op=='=':
                if not self.CanTransform(type1.type,type0.type):
                    raise SemanticError(f"different types cannot transform! {type0.type}<-{type1.type}")
            elif op in ['+=','-=','*=','/=','%=']:
                if type0.type not in self.integers or type1.type!=type0.type:
                    raise SemanticError(f"not integer types! {type0.type} {op} {type1.type}")
            elif op in ['&=','^=','|=']:
                if type0.type not in self.basicTypes or type1.type!=type0.type:
                    raise SemanticError(f"not integer or boolean types! {type0.type} {op} {type1.type}")  
            elif op in ['<<=','>>=']:
                if type0.type not in self.integers or type1 not in self.integers:
                    raise SemanticError(f"not integer types! {type0.type} {op} {type1.type}")
        elif op in self.comparisonOps:
            if op in ['==','!=']:
                if type0.type!=type1.type or not self.CheckAttribute(type0.type,'PartialEq'):
                    raise SemanticError(f"cannot compare! {type0.type} {op} {type1.type}")
            elif op in ['<', '<=','>', '>=']:
                if type0.type not in self.basicTypes or type1.type!=type0.type:
                    raise SemanticError(f"cannot compare! {type0.type} {op} {type1.type}")
        elif op in self.logicOps:
            if type0.type !='bool' or type1.type!='bool':
                raise SemanticError(f"cannot logic! {type0.type} {op} {type1.type}")
        elif op in self.arithmeticOps:
            if op in ["+","-", "*","/", "%"]:
                if type0.type not in self.integers or type1.type!=type0.type:
                    raise SemanticError(f"not integer types! {type0.type} {op} {type1.type}")
            elif op in ["&","|","^"]:
                if type0.type not in self.basicTypes or type1.type!=type0.type:
                    raise SemanticError(f"not integer or boolean types! {type0.type} {op} {type1.type}")
            elif op in ["<<",">>"]:
                if type0.type not in self.integers or type1 not in self.integers:
                    raise SemanticError(f"not integer types! {type0.type} {op} {type1.type}")
        elif op in self.unaryOps:
            if op=='!':
                if type0.type not in self.basicTypes:
                    raise SemanticError(f"not integer or boolean types! {op} {type0.type}")
            elif op=='minus':
                if type0.type not in ['i32','isize']:
                    raise SemanticError(f"cannot minus! {op} {type0.type}")
            elif op=='star':
                if not type0.type.startswith("&") and not type0.type.startswith("Box<"):
                    raise SemanticError(f"cannot dereference! {op} {type0.type}")
                type0.left=True
                if type0.type.startswith("& "):
                    type0.mut=False
                    type0.mut_blocked=True
                    type0.type=type0.type[2:]
                elif type0.type.startswith("&mut "):
                    type0.mut=type0.mut_blocked
                    type0.type=type0.type[5:]
                else:#Box<T>
                    type0.mut=(type0.mut or not type0.left) and not type0.mut_blocked
                    type0.type=type0.type[4:-1]
            else:#&,&mut
                if 'mut' in op and (type0.left and not type0.mut):
                    raise SemanticError(f"left type not mut type! {op} {type0.type}")
                type0.mut=False
                type0.left=False
                type0.type='&mut ' if 'mut' in op else '& '+type0.type
    def CheckVecBox(self,VecBox:str,func_name:str,scope:Scope,arguments:str,innerType:str,directCall=False,impl=None,inloop="",type0:Type=None):#return Type
        if VecBox=="Vec":
            if func_name=='new':
                if directCall==False:
                    raise SemanticError("indirect call of Vec<>::new!")
                if len(arguments)!=0:
                    raise SemanticError(f"param number not align!  {len(arguments)}!=0")
                return Type(mut=False,mut_blocked=False,left=False,type=f"Vec<{innerType}>")
            elif func_name=="len":#direct call
                if len(arguments)!=directCall:
                    raise SemanticError(f"param number not align!  {len(arguments)}!={directCall}")
                if directCall:
                    self.ParseExpression(scope,arguments[0],expected=f'& Vec<{innerType}>',impl=impl,inloop=inloop)
                return Type(mut=False,mut_blocked=False,left=False,type="usize")
            elif func_name=="is_empty":
                if len(arguments)!=directCall:
                    raise SemanticError(f"param number not align!  {len(arguments)}!={directCall}")
                if directCall:
                    self.ParseExpression(scope,arguments[0],expected=f'& Vec<{innerType}>',impl=impl,inloop=inloop)
                return Type(mut=False,mut_blocked=False,left=False,type="bool")
            elif func_name=="push":
                if len(arguments)!=1+directCall:
                    raise SemanticError(f"param number not align!  {len(arguments)}!={1+directCall}")
                if directCall:
                    self.ParseExpression(scope,arguments[0],expected=f'&mut Vec<{innerType}>',impl=impl,inloop=inloop)
                else:
                    if not (type0.mut and not type0.mut_blocked):
                        raise SemanticError("not mut self!")
                self.ParseExpression(scope,arguments[-1],expected=innerType,impl=impl,inloop=inloop)
                return Type(mut=False,mut_blocked=False,left=False,type="()")
            elif func_name=="remove":
                if len(arguments)!=1+directCall:
                    raise SemanticError(f"param number not align!  {len(arguments)}!={1+directCall}")
                if directCall:
                    self.ParseExpression(scope,arguments[0],expected=f'&mut Vec<{innerType}>',impl=impl,inloop=inloop)
                else:
                    if not (type0.mut and not type0.mut_blocked):
                        raise SemanticError("not mut self!")
                self.ParseExpression(scope,arguments[-1],expected='usize',impl=impl,inloop=inloop)
                return Type(mut=False,mut_blocked=False,left=False,type=innerType)
            elif func_name=="clone":
                if len(arguments)!=directCall:
                    raise SemanticError(f"param number not align!  {len(arguments)}!={directCall}")
                if not self.CheckAttribute(innerType,"Clone"):
                    raise SemanticError(f"{innerType} cannot clone!")
                if directCall:
                    self.ParseExpression(scope,arguments[0],expected=f'& Vec<{innerType}>',impl=impl,inloop=inloop)
                return Type(mut=False,mut_blocked=False,left=False,type=f"Vec<{innerType}>")
            else:
                raise SemanticError(f"No such function {func_name} in Vec<T>!")
        else:#Box
            if func_name=="new":
                if directCall==False:
                    raise SemanticError("indirect call of Vec<>::new!")
                if len(arguments)!=0:
                    raise SemanticError(f"param number not align!  {len(arguments)}!=0")
                return Type(mut=False,mut_blocked=False,left=False,type=f"Box<{innerType}>")
            elif func_name=="clone":
                if len(arguments)!=directCall:
                     raise SemanticError(f"param number not align!  {len(arguments)}!={directCall}")
                if not self.CheckAttribute(innerType,"Clone"):
                    raise SemanticError(f"{innerType} cannot clone!")
                if directCall:
                    self.ParseExpression(scope,arguments[0],expected=f'& Box<{innerType}>',impl=impl,inloop=inloop)
                return Type(mut=False,mut_blocked=False,left=False,type=f"Box<{innerType}>")
            else:
                raise SemanticError(f"No such function {func_name} in Box<T>!")

    #inloop: "if"+type,"while"+type,"loop"+type,""
    def ParseExpression(self,scope:Scope,expression:ast_nodes.Expression,expected:str=None,impl=None,inloop=""):#return Type
        if isinstance(expression,ast_nodes.PrimitiveExpression):
            if expression.op in self.assignmentOps:#assignment
                if expected and expected!="()":
                    raise SemanticError(f"expression type error! () != {expected}")
                type0=self.ParseExpression(scope,expression.expressions[0],impl=impl,inloop=inloop)
                type1=self.ParseExpression(scope,expression.expressions[1],type0.type if expression.op=='=' else None,impl=impl,inloop=inloop)
                self.CheckOp(type0,type1,expression.op)
                return Type(mut=False,mut_blocked=False,left=False,type="()")
            elif expression.op in self.comparisonOps:
                if expected and expected!="bool":
                    raise SemanticError(f"expression type error! bool != {expected}")
                type0=self.ParseExpression(scope,expression.expressions[0],impl=impl,inloop=inloop)
                type1=self.ParseExpression(scope,expression.expressions[1],impl=impl,inloop=inloop)
                self.CheckOp(type0,type1,expression.op)
                return Type(mut=False,mut_blocked=False,left=False,type="bool")
            elif expression.op in self.logicOps or expression.op in self.arithmeticOps:
                type0=self.ParseExpression(scope,expression.expressions[0],impl=impl,inloop=inloop)
                for i in range(1,len(expression.expressions)):
                    type1=self.ParseExpression(scope,expression.expressions[i],impl=impl,inloop=inloop)
                    self.CheckOp(type0,type1,expression.op)
                type='bool' if expression.op in self.logicOps else type0.type
                if expected and expected!=type:
                    raise SemanticError(f"expression type error! {type} != {expected}")
                return Type(mut=False,mut_blocked=False,left=False,type=type)

            
        elif isinstance(expression,ast_nodes.UnaryExpression):
            type=self.ParseExpression(scope,expression.postfixExpression,expected=expected if len(expression.ops)==0 else None,impl=impl,inloop=inloop)
            for op in expression.ops[::-1]:
                if op=='&&':
                    self.CheckOp(type,None,'&')
                    self.CheckOp(type,None,'&')
                elif op=='&&mut':
                    self.CheckOp(type,None,'&mut')
                    self.CheckOp(type,None,'&')
                else:
                    self.CheckOp(type,None,op)
            if expected and expected!=type.type:
                raise SemanticError(f"expression type error! {type.type} != {expected}")
            return type

        elif isinstance(expression,ast_nodes.CastExpression):
            type0=self.ParseExpression(scope,expression.unaryExpression,expected=expected if len(expression.typeRefs)==0 else None,impl=impl,inloop=inloop)
            for each in expression.typeRefs:
                type1=self.ParseTypeRef(each,impl=impl).type
                if type0.type not in self.basicTypes or type1 not in self.integers:
                    raise SemanticError(f"cannot cast! {type0.type} as {type1}")
                type0.type=type1
            if expected and expected!=type0.type:
                raise SemanticError(f"expression type error! {type0.type} != {expected}")
            return type0

        
        elif isinstance(expression,ast_nodes.PostfixExpression):
            type0=self.ParseExpression(scope,expression.primaryExpression,expected=expected if len(expression.postfixSuffixes)==0 else None,impl=impl,inloop=inloop)
            for suffix in expression.postfixSuffixes:
                if isinstance(suffix,ast_nodes.CallArguments):
                    if type0.type.startswith("#"):#function
                        if type0.type.startswith("#Vec<") or type0.type.startswith("#Box<"):#Vec operations        
                            type0=self.CheckVecBox(type0.type[1:4],type0.type[type0.type.index("::")+2:],scope,suffix.expression,type0.type[5:type0.type.index("::")-1],directCall=True,impl=impl,inloop=inloop)
                        else:
                            type=type0.type[1:]
                            func=self.FunctionDefinitions.get(type)
                            if not func:
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
                    if type0.type.startswith("Vec<") or type0.type.startswith("["):
                         self.ParseExpression(scope,suffix.expression,expected='usize',impl=impl,inloop=inloop)
                         type0=Type(mut=type0.mut,mut_blocked=type0.mut_blocked if type0.type.startswith("[") else (type0.mut_blocked or not type0.mut),left=True,type=self.GetArrayInner(type0.type) if type0.type.startswith("[") else type0.type[4:-1])
                    else:
                        raise SemanticError(f"not array! {type0.type}")
                elif isinstance(suffix,ast_nodes.DotSuffix):
                    type=self.dereference(type0.type)
                    struct=self.StructDefinitions.get(type)
                    if not type.startswith("Vec<") and not type.startswith("Box<") and not struct:
                        raise SemanticError(f"struct {type} does not exist!")
                    if isinstance(suffix,ast_nodes.DotSuffixData):
                        if type.startswith("Vec<") or type.startswith("Box<"):
                            raise SemanticError("Vec or Box has not data member!")
                        structField=struct.fields.get(suffix.identifier)
                        if not structField:
                            raise SemanticError(f"field {suffix.identifier} does not exist in struct {type}!")
                        type0=Type(mut=type0.mut and not type0.mut_blocked,mut_blocked=False,left=True,type=structField.type)
                    elif isinstance(suffix,ast_nodes.DotSuffixMethod):
                        if suffix.pathExprSegment.genericArgs:
                            raise SemanticError(f"function {type}::{suffix.pathExprSegment.identifier} has genericArgs!")
                        if type.startswith("Vec<") or type.startswith("Box<"):
                            type0=self.CheckVecBox(type[:3],suffix.pathExprSegment.identifier,scope,suffix.callarguments.expressions,type[4:-1],impl=impl,inllop=inloop,type0=type0)
                        else:
                            if suffix.pathExprSegment.identifier=="clone":
                                if len(arguments.expressions)!=0:
                                    raise SemanticError(f"param number not align!  {len(arguments.expressions)}!=0")
                                if not self.CheckAttribute(type,"Clone"):
                                    raise SemanticError(f"struct {type} cannot clone!")
                                type0=Type(mut=False,mut_blocked=False,left=False,type=type)
                            else:
                                func=self.FunctionDefinitions.get(type+"::"+suffix.pathExprSegment.identifier)
                                if not func:
                                    raise SemanticError(f"function {type}::{suffix.pathExprSegment.identifier} does not exist!")
                                if not func.self:
                                    raise SemanticError(f"function {type}::{suffix.pathExprSegment.identifier} does not have self param!")
                                if func.self.mut and func.self.amp and (not (type0.mut and not type0.mut_blocked)):
                                    raise SemanticError("not mut self!")
                                arguments=suffix.callarguments
                                if len(arguments.expressions)!=len(func.paramNames):
                                    raise SemanticError(f"param number not align!  {len(arguments.expressions)}!={len(func.paramNames)}")
                                for i in range(1,len(arguments.expressions)):
                                    self.ParseExpression(scope,arguments.expressions[i],expected=func.params[i-1].type,impl=impl,inloop=inloop)
                                type0=Type(mut=False,mut_blocked=False,left=False,type=func.returnType.type if func.returnType else "()")
            return type0


        
        elif isinstance(expression,ast_nodes.NonBlockPrimary):
            if expression.type=='literal':
                return self.ParseExpression(scope,expression.expression,expected=expected,impl=impl,inloop=inloop)
            elif expression.type=='path':
                if expression.structExprFields==None:#reference by name
                    typePathSegments=expression.expression.typePathSegments
                    if len(typePathSegments)!=1 and len(typePathSegments)!=2:
                        raise SemanticError("invalid typePath!")
                    if (typePathSegments[0].identifier=="Vec" or typePathSegments[0].identifier=="Box") and len(typePathSegments[0].genericArgs)==1:
                        if expected:
                            raise SemanticError(f"function type doesn't match {expected}")  
                        type=typePathSegments[0].identifier+"<"+self.ParseTypeRef(typePathSegments[0].genericArgs[0]).type+">"
                        if len(typePathSegments)==2:#function
                            if len(typePathSegments[1].genericArgs)!=0:
                                raise SemanticError(f"function {typePathSegments[1].identifier} has genericArgs!")  
                            return Type(mut=False,mut_blocked=False,left=False,type=f"#{type}::{typePathSegments[1].identifier}")
                        else:
                            raise SemanticError(f"invalid reference of {typePathSegments[0].identifier}!")
                    else:
                        #check genericArgs
                        for each in typePathSegments:
                            if len(each.genericArgs)>0:
                                raise SemanticError(f"genericArgs!")
                        name=typePathSegments[-1].identifier
                        if len(typePathSegments)==2:#impl
                            if typePathSegments[0].identifier=="Self" and not impl:
                                raise SemanticError(f"invalid use of Self!")
                            name=(impl if typePathSegments[0].identifier=="Self" else typePathSegments[0].identifier)+"::"+name
                        var=scope.get(name)#reference by name,may be function or variable
                        if expected and expected!=var.type:
                            raise SemanticError(f"expression type error! {var.type} != {expected}")
                        return Type(mut=var.mut,mut_blocked=var.mut_blocked,left=var.left,type=var.type)
                else:#build Struct
                    typePathSegments=expression.expression.typePathSegments
                    args=expression.structExprFields
                    if len(typePathSegments)!=1 or (typePathSegments[0].genericArgs)!=0:
                        raise SemanticError("invalid struct!")
                    struct=self.StructDefinitions.get(typePathSegments[0].identifier)
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
                          

            elif expression.type=='paren':
                if expression.expression:
                    return self.ParseExpression(scope,expression.expression,expected=expected,impl=impl,inloop=inloop)
                else:
                    return Type(mut=False,mut_blocked=False,left=False,type="()")
            elif expression.type=='array':
                return self.ParseExpression(scope,expression.expression,expected=expected,impl=impl,inloop=inloop)
            elif expression.type=='break':
                if inloop.startswith("loop") or (expression.expression and inloop.startswith("while")):
                    loop_expectancy=inloop[4:] if inloop.startswith("loop") else inloop[5:]
                    if expression.expression:
                        return self.ParseExpression(scope,expression.expression,expected=loop_expectancy,impl=impl,inloop=inloop)
                    else:#return ()
                        if loop_expectancy:
                            raise SemanticError(f"loop return type error! () != {loop_expectancy}")
                    return Type(mut=False,mut_blocked=False,left=False,type="^")
                else:
                    raise SemanticError("break outside loop!")
            elif expression.type=='return':
                retType=self.FunctionDefinitions.get(self.functionName).returnType
                type=retType.type if retType else "()"
                if expression.expression:
                    return self.ParseExpression(scope,expression.expression,expected=type,impl=impl,inloop=inloop)
                else:#return ()
                    if type and type!="()":
                        raise SemanticError(f"function return type error! () != {type}")
                    return Type(mut=False,mut_blocked=False,left=False,type="^")
            elif expression.type=='continue':
                if not (inloop.startswith("loop") or inloop.startswith("while")):
                    raise SemanticError("continue outside loop!")
            return type0

        elif isinstance(expression,ast_nodes.NormalExpressionWithBlock):
        elif isinstance(expression,ast_nodes.IfExpression):
            



                    
        



                
                


                



                
            
                

                
    def ParseLetStatement(self,scope:Scope,statement:ast_nodes.LetStatement,prefix:str,impl=None,inloop=""):
        type=self.ParseTypeRef(statement.typeRef).type if statement.typeRef else None
        variable=Variable(mut=statement.mut,name=prefix+statement.identifier,type=type,left=True)
        newtype=self.ParseExpression(scope,statement.value,expected=type,impl=impl,inloop=inloop)
        variable.type=newtype.type
        scope.register(statement.identifier,variable)

    
    def ParseBlockExpression(self,scope:Scope,block:ast_nodes.BlockExpression,prefix:str,expected=None,impl=None,inloop=""):#prefix is used for variable renaming
        for statement in block.statements:
            if isinstance(statement,ast_nodes.LetStatement):
                self.ParseLetStatement(scope,statement,prefix,impl=impl,inloop=inloop)

    def SemanticCheck(self):
        self.scope=Scope(values={})#global scope
        self.SymbolCollection()
        #register global constants and functions
        self.FunctionDefinitions["print_i32"]=FunctionInfo(name="print_i32",self=None,returnType=None,paramNames=['a'],params=[Variable(mut=False,mut_blocked=False,left=True,type='i32',name='print_i32@a')],body=None)
        self.FunctionDefinitions["println_i32"]=FunctionInfo(name="println_i32",self=None,returnType=None,paramNames=['a'],params=[Variable(mut=False,mut_blocked=False,left=True,type='i32',name='println_i32@a')],body=None)
        self.FunctionDefinitions["get_i32"]=FunctionInfo(name="get_i32",self=None,returnType=Object(type='i32'),paramNames=[],params=[],body=None)           
        for name in self.FunctionDefinitions:
            self.scope.register(name,Variable(mut=False,mut_blocked=False,left=False,type=f'#{name}',name=name))
        for name in self.ConstValues:
            self.scope.register(name,Variable(mut=False,mut_blocked=False,left=True,type=self.ConstValues[name].type,name=name))
        for name in self.FunctionDefinitions:
            if name in ['print_i32','println_i32','get_i32']:
                continue
            functionInfo=self.FunctionDefinitions[name]
            function_scope=Scope(values=functionInfo.params,parent=self.scope)
            if functionInfo.self:
                if not functionInfo.self.amp:
                    function_scope.values["self"]=Variable(mut=functionInfo.self.mut,mut_blocked=False,name=name+"@self",value=None,type=name,left=True)
                else:
                    function_scope.values["self"]=Variable(mut=functionInfo.self.mut,mut_blocked=not functionInfo.self.mut,name=name+"@self",value=None,type=('&mut' if functionInfo.self.mut else '& ')+name,left=True)
            self.functionName=name
            self.ParseBlockExpression(function_scope,functionInfo.body,name+"@",expected=functionInfo.returnType,impl=name[:name.index("::")] if "::" in name else None)
        


   

                            


