from dataclasses import dataclass,field

def parseIntegerLiteral(s:str):
    s=s.replace("_","")
    val=0
    type=''
    if s.endswith('i32'):
        s=s[:-3]
        type='i32'
    elif s.endswith('u32'):
        s=s[:-3]
        type='u32'
    elif s.endswith('isize'):
        s=s[:-5]
        type='isize'
    elif s.endswith('usize'):
        s=s[:-5]
        type='usize'
    if s.startswith("0b"):
        val=int(s,2)
    elif s.startswith('0o'):
        val=int(s,8)
    elif s.startswith('0x'):
        val=int(s,16)
    else:
        val=int(s,10)
    val%=(1<<32)
    return val,type

@dataclass
class GenericParams: #discarded
    pass

@dataclass
class Expression:
    pass


@dataclass
class TypeRef(Expression):
    pass


@dataclass
class TypePathSegment:#think about Vec<T>
    identifier: str
    genericArgs: list[TypeRef]

@dataclass
class TypePath(TypeRef):
   typePathSegments: list[TypePathSegment]

@dataclass
class ReferenceType(TypeRef):
    mut: bool
    inner: TypeRef

@dataclass
class Item:#base class
    pass

@dataclass
class UseDeclaration(Item):#discarded
    pass

@dataclass
class SelfParam:
    amp: bool #whether pass by reference
    mut : bool
    lifetime : str

@dataclass
class FunctionParam:
    mut: bool
    identifier: str
    typeref: TypeRef

@dataclass
class StructField:
    identifier: str
    typeref: TypeRef

@dataclass
class FunctionParameters:
    selfParam: SelfParam
    parameters: list[FunctionParam]


@dataclass
class StructDefinition(Item):
    outerAttributes: list[str]
    identifier: str
   # genericParams: GenericParams
    #whereClause: WhereClause
    fields: list[StructField]


@dataclass
class InherentImpl(Item):
   # genericParams: GenericParams
    typeRef: TypeRef
   # whereClause: WhereClause
    associatedItems: list[Item]#constantItem or functionDefinition

@dataclass
class StructExprField:
    identifier: str
    expression: Expression

@dataclass
class Statement:
    pass

@dataclass
class NonLetStatement(Statement):
    semi:bool
    expression: Expression

@dataclass
class StatementExpression(Expression):
    pass

@dataclass
class PrimitiveExpression(StatementExpression):
    op: str #and, or, &,|,^, assignment, comparison
    expressions: list[Expression]

@dataclass
class ExtraExpression(PrimitiveExpression):
    ops: list[str]

@dataclass
class PrimaryExpression(Expression):
    pass


@dataclass
class PostfixSuffix():
    pass

@dataclass
class CallArguments(PostfixSuffix):
    expressions: list[Expression]

@dataclass
class DotSuffix(PostfixSuffix):
    pass

@dataclass
class DotSuffixMethod(DotSuffix):
    pathExprSegment: TypePathSegment
    callarguments: CallArguments

@dataclass
class DotSuffixData(DotSuffix):
    identifier: str

@dataclass
class BracketSuffix(PostfixSuffix):
    expression: Expression

@dataclass
class PostfixExpression(Expression):
    primaryExpression: PrimaryExpression
    postfixSuffixes: list[PostfixSuffix]

@dataclass
class StatementPostfixExpression(PostfixExpression):
    dotSuffix: DotSuffix

@dataclass
class UnaryExpression(Expression):
    ops: list[str]
    postfixExpression: PostfixExpression

@dataclass
class CastExpression(Expression):
    unaryExpression: UnaryExpression
    typeRefs: list[TypeRef]


@dataclass
class ConditionPrimary(PrimaryExpression):
    pass

@dataclass
class ExpressionWithBlock(ConditionPrimary):
    pass

@dataclass 
class NonBlockPrimary(PrimaryExpression):
    expression: Expression
    type: str
    structExprFields: list[StructExprField]


@dataclass
class BlockExpression(ConditionPrimary):
    statements: list[Statement]
    statementexpression: Expression

@dataclass 
class WhileExpression(Expression):
    conditionExpression: Expression 
    blockExpression: BlockExpression


@dataclass 
class NormalExpressionWithBlock(ExpressionWithBlock):
    loop: bool
    blockExpression: BlockExpression
    conditionExpression: Expression
    
@dataclass
class IfExpression(ExpressionWithBlock):#switch expressions
    conditionExpression: Expression
    thenExpressions: list[Expression]
    #len(blockExpressions)= len(conditionExpressions) or len(conditionExpressions)+1

@dataclass
class LiteralExpression(Expression):
    value: int
    type: str

@dataclass
class ConstValue(LiteralExpression):
    pathInExpression: TypePath 
    minus: bool=False

@dataclass
class ArrayType(TypeRef):
    inner: TypeRef
    length: ConstValue


@dataclass
class ConstantItem(Item):
    identifier: str
    typeref: TypeRef
    constValue: ConstValue

@dataclass
class ArrayExpresssion(Expression):
    pass

@dataclass
class NormalArrayExpresssion(Expression):
    expressions: list[Expression]

@dataclass
class RepeatArrayExpression(Expression):
    expression: Expression
    length: ConstValue


@dataclass
class LetStatement(Statement):
    mut: bool
    identifier: str
    typeRef: TypeRef
    value: Expression


@dataclass
class FunctionDefinition(Item):
    identifier: str
    #genericParams: GenericParams
    functionParameters: FunctionParameters
    typeref: TypeRef
    #whereClause: WhereClause
    blockExpression: BlockExpression
    hasGeneric: bool #only used for main check

@dataclass
class Crate:
    Items: list[Item]
