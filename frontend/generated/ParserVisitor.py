# Generated from grammar/Parser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .Parser import Parser
else:
    from Parser import Parser
from frontend.generated import ast_nodes

# This class defines a complete generic visitor for a parse tree produced by Parser.

class ParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by Parser#crate.
    def visitCrate(self, ctx:Parser.CrateContext):
        #print("Visited crate",len(ctx.item()))
        return ast_nodes.Crate(Items=[self.visit(ctx.item(i)) for i in range(len(ctx.item()))])


    # Visit a parse tree produced by Parser#item.
    def visitItem(self, ctx:Parser.ItemContext):
        if ctx.useDeclaration():
            return self.visit(ctx.useDeclaration())
        if ctx.functionDefinition():
            return self.visit(ctx.functionDefinition())
        if ctx.structDefinition():
            return self.visit(ctx.structDefinition())
        if ctx.constantItem():
            return self.visit(ctx.constantItem())
        if ctx.inherentImpl():
            return self.visit(ctx.inherentImpl())


    # Visit a parse tree produced by Parser#useDeclaration.
    def visitUseDeclaration(self, ctx:Parser.UseDeclarationContext):#discard use
        return ast_nodes.UseDeclaration()


    # Visit a parse tree produced by Parser#useTree.
    def visitUseTree(self, ctx:Parser.UseTreeContext):#discarded
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Parser#usePath.
    def visitUsePath(self, ctx:Parser.UsePathContext):#discarded
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Parser#usePathSegment.
    def visitUsePathSegment(self, ctx:Parser.UsePathSegmentContext):#discarded
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Parser#functionDefinition.
    def visitFunctionDefinition(self, ctx:Parser.FunctionDefinitionContext):
        return ast_nodes.FunctionDefinition(identifier=self.visit(ctx.identifier()), functionParameters=self.visit(ctx.functionParameters()) if ctx.functionParameters() else None, typeref=self.visit(ctx.typeRef()) if ctx.typeRef() else None,  blockExpression=self.visit(ctx.blockExpression()),hasGeneric=ctx.genericParams() is not None)


    # Visit a parse tree produced by Parser#functionParameters.
    def visitFunctionParameters(self, ctx:Parser.FunctionParametersContext):
        return ast_nodes.FunctionParameters(selfParam=self.visit(ctx.selfParam()) if ctx.selfParam() else None, parameters=[self.visit(ctx.functionParam(i)) for i in range(len(ctx.functionParam()))])


    # Visit a parse tree produced by Parser#selfParam.
    def visitSelfParam(self, ctx:Parser.SelfParamContext):
        return ast_nodes.SelfParam(amp=ctx.AMP() is not None, mut=ctx.MUT() is not None, lifetime=self.visit(ctx.lifetime()) if ctx.lifetime() else None)


    # Visit a parse tree produced by Parser#functionParam.
    def visitFunctionParam(self, ctx:Parser.FunctionParamContext):
        tpl=self.visit(ctx.identifierBinding())
        return ast_nodes.FunctionParam(mut=tpl[0], identifier=tpl[1], typeref=self.visit(ctx.typeRef()))


    # Visit a parse tree produced by Parser#structDefinition.
    def visitStructDefinition(self, ctx:Parser.StructDefinitionContext):
        outerAttributes =[]
        for i in range(len(ctx.outerAttribute())):
            outerAttributes+=self.visit(ctx.outerAttribute(i))
        #need to check unique
        return ast_nodes.StructDefinition(outerAttributes=outerAttributes, identifier=self.visit(ctx.identifier()), fields=[self.visit(ctx.structField(i)) for i in range(len(ctx.structField()))])


    # Visit a parse tree produced by Parser#structField.
    def visitStructField(self, ctx:Parser.StructFieldContext):
        #print("Visited structField",ctx.getText())
        return ast_nodes.StructField(identifier=self.visit(ctx.identifier()), typeref=self.visit(ctx.typeRef()))


    # Visit a parse tree produced by Parser#outerAttribute.
    def visitOuterAttribute(self, ctx:Parser.OuterAttributeContext):
        return [self.visit(ctx.deriveName(i)) for i in range(len(ctx.deriveName()))]


    # Visit a parse tree produced by Parser#deriveName.
    def visitDeriveName(self, ctx:Parser.DeriveNameContext):
        return ctx.getText()


    # Visit a parse tree produced by Parser#constantItem.
    def visitConstantItem(self, ctx:Parser.ConstantItemContext):
        return ast_nodes.ConstantItem(identifier=self.visit(ctx.identifier()), typeref=self.visit(ctx.typeRef()), constValue=self.visit(ctx.constValue()))


    # Visit a parse tree produced by Parser#inherentImpl.
    def visitInherentImpl(self, ctx:Parser.InherentImplContext):
        return ast_nodes.InherentImpl(typeRef=self.visit(ctx.typeRef()), associatedItems=[self.visit(ctx.associatedItem(i)) for i in range(len(ctx.associatedItem()))])


    # Visit a parse tree produced by Parser#associatedItem.
    def visitAssociatedItem(self, ctx:Parser.AssociatedItemContext):
        return self.visit(ctx.constantItem()) if ctx.constantItem() else self.visit(ctx.functionDefinition())


    # Visit a parse tree produced by Parser#genericParams.
    def visitGenericParams(self, ctx:Parser.GenericParamsContext):
        #discarded
        return None

    # Visit a parse tree produced by Parser#lifetimeParam.
    def visitLifetimeParam(self, ctx:Parser.LifetimeParamContext):
        return None


    # Visit a parse tree produced by Parser#lifetime.
    def visitLifetime(self, ctx:Parser.LifetimeContext):
        return None


    # Visit a parse tree produced by Parser#lifetimeBounds.
    def visitLifetimeBounds(self, ctx:Parser.LifetimeBoundsContext):
        return None


    # Visit a parse tree produced by Parser#typeParamBounds.
    def visitTypeParamBounds(self, ctx:Parser.TypeParamBoundsContext):
        return None


    # Visit a parse tree produced by Parser#whereClause.
    def visitWhereClause(self, ctx:Parser.WhereClauseContext):
        #discarded
        return None


    # Visit a parse tree produced by Parser#whereClauseItem.
    def visitWhereClauseItem(self, ctx:Parser.WhereClauseItemContext):
        return None


    # Visit a parse tree produced by Parser#typeRef.
    def visitTypeRef(self, ctx:Parser.TypeRefContext):
        if ctx.typeRef():
            return self.visit(ctx.typeRef())
        elif ctx.typePath():
            return self.visit(ctx.typePath())
        elif ctx.referenceType():
            return self.visit(ctx.referenceType())
        elif ctx.arrayType():
            return self.visit(ctx.arrayType())
        else:
            return ast_nodes.TypeRef()


    # Visit a parse tree produced by Parser#referenceType.
    def visitReferenceType(self, ctx:Parser.ReferenceTypeContext):
        #each & a layer
        if ctx.AMP():
            return ast_nodes.ReferenceType(mut=ctx.MUT() is not None, inner=self.visit(ctx.typeRef()))
        elif ctx.ANDAND():
            return ast_nodes.ReferenceType(mut=False, inner=ast_nodes.ReferenceType(mut=ctx.MUT() is not None, inner=self.visit(ctx.typeRef())))


    # Visit a parse tree produced by Parser#arrayType.
    def visitArrayType(self, ctx:Parser.ArrayTypeContext):
        return ast_nodes.ArrayType(inner=self.visit(ctx.typeRef()),length=self.visit(ctx.constValue()))


    # Visit a parse tree produced by Parser#typePath.
    def visitTypePath(self, ctx:Parser.TypePathContext):
        return ast_nodes.TypePath(typePathSegments=[self.visit(ctx.typePathSegment(i)) for i in range(len(ctx.typePathSegment()))])


    # Visit a parse tree produced by Parser#typePathSegment.
    def visitTypePathSegment(self, ctx:Parser.TypePathSegmentContext):
        return ast_nodes.TypePathSegment(identifier=self.visit(ctx.pathIdentSegment()),genericArgs=self.visit(ctx.genericArgs()) if ctx.genericArgs() else [])


    # Visit a parse tree produced by Parser#pathInExpression.
    def visitPathInExpression(self, ctx:Parser.PathInExpressionContext):#equals typePath
       return ast_nodes.TypePath(typePathSegments=[self.visit(ctx.pathExprSegment(i)) for i in range(len(ctx.pathExprSegment()))])
       


    # Visit a parse tree produced by Parser#pathExprSegment.
    def visitPathExprSegment(self, ctx:Parser.PathExprSegmentContext):# equals typePathSegment
        return ast_nodes.TypePathSegment(identifier=self.visit(ctx.pathIdentSegment()),genericArgs=self.visit(ctx.genericArgs()) if ctx.genericArgs() else [])
        


    # Visit a parse tree produced by Parser#pathIdentSegment.
    def visitPathIdentSegment(self, ctx:Parser.PathIdentSegmentContext):
        #return identifier str
        return ctx.getText()


    # Visit a parse tree produced by Parser#genericArgs.
    def visitGenericArgs(self, ctx:Parser.GenericArgsContext):
        genericArgs=[]
        for i in range(len(ctx.genericArg())):
            genericArg=self.visit(ctx.genericArg(i))
            if genericArg:
                genericArgs.append(genericArg)
        return genericArgs


    # Visit a parse tree produced by Parser#genericArg.
    def visitGenericArg(self, ctx:Parser.GenericArgContext):
        #discard lifetime branch
        return self.visit(ctx.typeRef()) if ctx.typeRef() else None


    # Visit a parse tree produced by Parser#genericClose.
    def visitGenericClose(self, ctx:Parser.GenericCloseContext):
        return '>' 


    # Visit a parse tree produced by Parser#closedCastType.
    def visitClosedCastType(self, ctx:Parser.ClosedCastTypeContext):#equals TypeRef
        if ctx.typeRef():
            return self.visit(ctx.typeRef())
        elif ctx.pathIdentSegment():
            return ast_nodes.TypePath(typePathSegments=[self.visit(ctx.typePathSegment(i)) for i in range(len(ctx.typePathSegment()))]+[ast_nodes.TypePathSegment(identifier=self.visit(ctx.pathIdentSegment()),genericArgs=self.visit(ctx.genericArgs()))])
        elif ctx.AMP() or ctx.ANDAND():
            if ctx.AMP():
                return ast_nodes.ReferenceType(mut=ctx.MUT() is not None, inner=self.visit(ctx.typeRef()))
            elif ctx.ANDAND():
                return ast_nodes.ReferenceType(mut=False, inner=ast_nodes.ReferenceType(mut=ctx.MUT() is not None, inner=self.visit(ctx.typeRef())))
        elif ctx.arrayType():
            return self.visit(ctx.arrayType())
        else:
            return ast_nodes.TypeRef()


    # Visit a parse tree produced by Parser#constValue.
    def visitConstValue(self, ctx:Parser.ConstValueContext):
        if ctx.constValue():
            return self.visit(ctx.constValue())
        elif ctx.TRUE():
            return ast_nodes.ConstValue(value=True,type="bool",pathInExpression=None)
        elif ctx.FALSE():
            return ast_nodes.ConstValue(value=False,type="bool",pathInExpression=None)
        elif ctx.INTEGER_LITERAL():
            value,type=ast_nodes.parseIntegerLiteral(ctx.INTEGER_LITERAL().getText())
            return ast_nodes.ConstValue(value=value,type=type,pathInExpression=None)
        elif ctx.MINUS():
            val=self.visit(ctx.magnitude())
            if isinstance(val,ast_nodes.TypePath):
                return ast_nodes.ConstValue(minus=True,type='',value=None,pathInExpression=val)
            else:
                return ast_nodes.ConstValue(minus=True,value=val[0],type=val[1],pathInExpression=None)
        else:
            return ast_nodes.ConstValue(value=None,type='', pathInExpression=self.visit(ctx.pathInExpression()))
    
    
    # Visit a parse tree produced by Parser#magnitude.
    def visitMagnitude(self, ctx:Parser.MagnitudeContext):
        if ctx.magnitude():
            return self.visit(ctx.magnitude())
        elif ctx.pathInExpression():
            return self.visit(ctx.pathInExpression())
        else:
            return ast_nodes.parseIntegerLiteral(ctx.INTEGER_LITERAL().getText())


    # Visit a parse tree produced by Parser#identifierBinding.
    def visitIdentifierBinding(self, ctx:Parser.IdentifierBindingContext): #return (bool, str)
        return (ctx.MUT() is not None,  self.visit(ctx.identifier()))


    # Visit a parse tree produced by Parser#letStatement.
    def visitLetStatement(self, ctx:Parser.LetStatementContext):
        binding=self.visit(ctx.identifierBinding())
        return ast_nodes.LetStatement(mut=binding[0],identifier=binding[1],typeRef=self.visit(ctx.typeRef()) if ctx.typeRef() else None, value=self.visit(ctx.expression()))


    # Visit a parse tree produced by Parser#blockExpression.
    def visitBlockExpression(self, ctx:Parser.BlockExpressionContext):
        statements=[self.visit(ctx.statement(i)) for i in range(len(ctx.statement()))]
        if ctx.statementExpression():
            return ast_nodes.BlockExpression(statements=statements,statementexpression=self.visit(ctx.statementExpression()))
        elif len(statements)>0 and isinstance(statements[-1],ast_nodes.NonLetStatement) and statements[-1].semi==False:
            return ast_nodes.BlockExpression(statements=statements[:-1],statementexpression=statements[-1].expression)
        else:
            return ast_nodes.BlockExpression(statements=statements,statementexpression=None)

    # Visit a parse tree produced by Parser#statement.
    def visitStatement(self, ctx:Parser.StatementContext):
        if ctx.letStatement():
            return self.visit(ctx.letStatement())
        elif ctx.expressionWithBlock():
            return ast_nodes.NonLetStatement(semi=True if ctx.SEMI() else False,expression=self.visit(ctx.expressionWithBlock()))
        elif ctx.statementExpression():
            return ast_nodes.NonLetStatement(semi=True,expression=self.visit(ctx.statementExpression()))
        else:
            return ast_nodes.NonLetStatement(semi=True,expression=None)


    # Visit a parse tree produced by Parser#expressionWithBlock.
    def visitExpressionWithBlock(self, ctx:Parser.ExpressionWithBlockContext):
        if ctx.ifExpression():
            return self.visit(ctx.ifExpression())
        else:
            return ast_nodes.NormalExpressionWithBlock(blockExpression=self.visit(ctx.blockExpression()),loop=ctx.LOOP() or ctx.WHILE(),conditionExpression=self.visit(ctx.conditionExpression()) if ctx.conditionExpression() else None)


    # Visit a parse tree produced by Parser#ifExpression.
    def visitIfExpression(self, ctx:Parser.IfExpressionContext):
        if ctx.ELSE():
            if ctx.ifExpression():
                return ast_nodes.IfExpression(conditionExpression=self.visit(ctx.conditionExpression()),thenExpressions=[self.visit(ctx.blockExpression(0)),self.visit(ctx.ifExpression())])
            else:
                return ast_nodes.IfExpression(conditionExpression=self.visit(ctx.conditionExpression()),thenExpression=[self.visit(ctx.blockExpression(0)),self.visit(ctx.blockExpression(1))])
        else:
            return ast_nodes.IfExpression(conditionExpression=self.visit(ctx.conditionExpression()),thenExpressions=[self.visit(ctx.blockExpression(0))])           


    # Visit a parse tree produced by Parser#expression.
    def visitExpression(self, ctx:Parser.ExpressionContext):#same as assignmentExpression
        return self.visit(ctx.assignmentExpression())


    # Visit a parse tree produced by Parser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:Parser.AssignmentExpressionContext):
        if ctx.assignmentOperator():
            return ast_nodes.PrimitiveExpression(op=self.visit(ctx.assignmentOperator()),expressions=[self.visit(ctx.logicalOrExpression()),self.visit(ctx.expression())])
        else:
            return self.visit(ctx.logicalOrExpression())


    # Visit a parse tree produced by Parser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:Parser.LogicalOrExpressionContext):
        if len(ctx.logicalAndExpression())>1:
            return ast_nodes.PrimitiveExpression(op="or",expressions=[self.visit(ctx.logicalAndExpression(i)) for i in range(len(ctx.logicalAndExpression()))])
        else:
            return self.visit(ctx.logicalAndExpression(0))


    # Visit a parse tree produced by Parser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:Parser.LogicalAndExpressionContext):
        if len(ctx.comparisonExpression())>1:
            return ast_nodes.PrimitiveExpression(op="and",expressions=[self.visit(ctx.comparisonExpression(i)) for i in range(len(ctx.comparisonExpression()))])
        else:
            return self.visit(ctx.comparisonExpression(0))


    # Visit a parse tree produced by Parser#comparisonExpression.
    def visitComparisonExpression(self, ctx:Parser.ComparisonExpressionContext):
        if ctx.LT():
            return ast_nodes.PrimitiveExpression(op="<",expressions=[self.visit(ctx.closedBitOrExpression()),self.visit(ctx.bitOrExpression(0))])
        elif ctx.comparisonExceptLt():
            return ast_nodes.PrimitiveExpression(op=self.visit(ctx.comparisonExceptLt()),expressions=[self.visit(ctx.bitOrExpression(0)),self.visit(ctx.bitOrExpression(1))])
        else:
            return self.visit(ctx.bitOrExpression(0))


    # Visit a parse tree produced by Parser#bitOrExpression.
    def visitBitOrExpression(self, ctx:Parser.BitOrExpressionContext):
        if len(ctx.bitXorExpression())>1:
            return ast_nodes.PrimitiveExpression(op="|",expressions=[self.visit(ctx.bitXorExpression(i)) for i in range(len(ctx.bitXorExpression()))])
        else:
            return self.visit(ctx.bitXorExpression(0))


    # Visit a parse tree produced by Parser#closedBitOrExpression.
    def visitClosedBitOrExpression(self, ctx:Parser.ClosedBitOrExpressionContext):
        if len(ctx.bitXorExpression())==0:
            return self.visit(ctx.closedBitXorExpression())
        return ast_nodes.PrimitiveExpression(op="|",expressions=[self.visit(ctx.bitXorExpression(i)) for i in range(len(ctx.bitXorExpression()))]+[self.visit(ctx.closedBitXorExpression())])


    # Visit a parse tree produced by Parser#bitXorExpression.
    def visitBitXorExpression(self, ctx:Parser.BitXorExpressionContext):
        if len(ctx.bitAndExpression())>1:
            return ast_nodes.PrimitiveExpression(op="^",expressions=[self.visit(ctx.bitAndExpression(i)) for i in range(len(ctx.bitAndExpression()))])
        else:
            return self.visit(ctx.bitAndExpression(0))


    # Visit a parse tree produced by Parser#closedBitXorExpression.
    def visitClosedBitXorExpression(self, ctx:Parser.ClosedBitXorExpressionContext):
        if len(ctx.bitAndExpression())==0:
            return self.visit(ctx.closedBitAndExpression())
        return ast_nodes.PrimitiveExpression(op="^",expressions=[self.visit(ctx.bitAndExpression(i)) for i in range(len(ctx.bitAndExpression()))]+[self.visit(ctx.closedBitAndExpression())])


    # Visit a parse tree produced by Parser#bitAndExpression.
    def visitBitAndExpression(self, ctx:Parser.BitAndExpressionContext):
        if len(ctx.shiftExpression())>1:
            return ast_nodes.PrimitiveExpression(op="&",expressions=[self.visit(ctx.shiftExpression(i)) for i in range(len(ctx.shiftExpression()))])
        else:
            return self.visit(ctx.shiftExpression(0))


    # Visit a parse tree produced by Parser#closedBitAndExpression.
    def visitClosedBitAndExpression(self, ctx:Parser.ClosedBitAndExpressionContext):
        if len(ctx.shiftExpression())==0:
            return self.visit(ctx.closedShiftExpression())
        return ast_nodes.PrimitiveExpression(op="&",expressions=[self.visit(ctx.shiftExpression(i)) for i in range(len(ctx.shiftExpression()))]+[self.visit(ctx.closedShiftExpression())])
        


    # Visit a parse tree produced by Parser#shiftExpression.
    def visitShiftExpression(self, ctx:Parser.ShiftExpressionContext):
        if ctx.SHL() or ctx.shiftRight():
            ops=[]
            expressions=[]
            for i in range(0,ctx.getChildCount()-1,2):
                expressions.append(self.visit(ctx.getChild(i)))
                ops.append(ctx.getChild(i+1).getText())
            expressions.append(self.visit(ctx.getChild(ctx.getChildCount()-1)))
            return ast_nodes.ExtraExpression(op='shift',expressions=expressions,ops=ops)
        else:
            return self.visit(ctx.additiveExpression(0))



    # Visit a parse tree produced by Parser#closedShiftExpression.
    def visitClosedShiftExpression(self, ctx:Parser.ClosedShiftExpressionContext):
        if ctx.SHL() or ctx.shiftRight():
            ops=[]
            expressions=[]
            for i in range(0,ctx.getChildCount()-1,2):
                expressions.append(self.visit(ctx.getChild(i)))
                ops.append(ctx.getChild(i+1).getText())
            expressions.append(self.visit(ctx.getChild(ctx.getChildCount()-1)))
            return ast_nodes.ExtraExpression(op='shift',expressions=expressions,ops=ops)
        else:
            return self.visit(ctx.closedAdditiveExpression(0))


    # Visit a parse tree produced by Parser#additiveExpression.
    def visitAdditiveExpression(self, ctx:Parser.AdditiveExpressionContext):
        if len(ctx.multiplicativeExpression())>1:
            return ast_nodes.ExtraExpression(op="+",expressions=[self.visit(ctx.multiplicativeExpression(i)) for i in range(len(ctx.multiplicativeExpression()))],ops=['+']+[self.visit(ctx.additiveOperator(i)) for i in range(len(ctx.additiveOperator()))])
        else:
            return self.visit(ctx.multiplicativeExpression(0))


    # Visit a parse tree produced by Parser#closedAdditiveExpression.
    def visitClosedAdditiveExpression(self, ctx:Parser.ClosedAdditiveExpressionContext):
        if len(ctx.multiplicativeExpression())==0:
            return self.visit(ctx.closedMultiplicativeExpression())
        return ast_nodes.ExtraExpression(op="+",expressions=[self.visit(ctx.multiplicativeExpression(i)) for i in range(len(ctx.multiplicativeExpression()))]+[self.visit(ctx.closedMultiplicativeExpression())],ops=['+']+[self.visit(ctx.additiveOperator(i)) for i in range(len(ctx.additiveOperator()))])
       


    # Visit a parse tree produced by Parser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:Parser.MultiplicativeExpressionContext):
        if len(ctx.castExpression())>1:
            return ast_nodes.ExtraExpression(op="*",expressions=[self.visit(ctx.castExpression(i)) for i in range(len(ctx.castExpression()))],ops=['*']+[self.visit(ctx.multiplicativeOperator(i)) for i in range(len(ctx.multiplicativeOperator()))])
        else:
            return self.visit(ctx.castExpression(0))
        


    # Visit a parse tree produced by Parser#closedMultiplicativeExpression.
    def visitClosedMultiplicativeExpression(self, ctx:Parser.ClosedMultiplicativeExpressionContext):
        if len(ctx.castExpression())==0:
            return self.visit(ctx.closedCastExpression())
        return ast_nodes.ExtraExpression(op="*",expressions=[self.visit(ctx.castExpression(i)) for i in range(len(ctx.castExpression()))]+[self.visit(ctx.closedCastExpression())],ops=['*']+[self.visit(ctx.multiplicativeOperator(i)) for i in range(len(ctx.multiplicativeOperator()))])
               


    # Visit a parse tree produced by Parser#castExpression.
    def visitCastExpression(self, ctx:Parser.CastExpressionContext):
        if len(ctx.typeRef())>0:
            return ast_nodes.CastExpression(unaryExpression=self.visit(ctx.unaryExpression()),typeRefs=[self.visit(ctx.typeRef(i)) for i in range(len(ctx.typeRef()))])
        else:
            return self.visit(ctx.unaryExpression())

    # Visit a parse tree produced by Parser#closedCastExpression.
    def visitClosedCastExpression(self, ctx:Parser.ClosedCastExpressionContext):
        if ctx.unaryExpression():
            return self.visit(ctx.unaryExpression())
        castExpression=self.visit(ctx.castExpression())
        return ast_nodes.CastExpression(unaryExpression=castExpression.unaryExpression,typeRefs=castExpression.typeRefs+[self.visit(ctx.closedCastType())])


    # Visit a parse tree produced by Parser#unaryExpression.
    def visitUnaryExpression(self, ctx:Parser.UnaryExpressionContext):
        if ctx.unaryOperator():
            unaryExpression=self.visit(ctx.unaryExpression())
            #quadratic time, may need to optimize!
            return ast_nodes.UnaryExpression(ops=[self.visit(ctx.unaryOperator())]+unaryExpression.ops,postfixExpression=unaryExpression.postfixExpression)
        return ast_nodes.UnaryExpression(ops=[],postfixExpression=self.visit(ctx.postfixExpression()))
        


    # Visit a parse tree produced by Parser#postfixExpression.
    def visitPostfixExpression(self, ctx:Parser.PostfixExpressionContext):
        return ast_nodes.PostfixExpression(primaryExpression=self.visit(ctx.primaryExpression()),postfixSuffixes=[self.visit(ctx.postfixSuffix(i)) for i in range(len(ctx.postfixSuffix()))])


    # Visit a parse tree produced by Parser#conditionExpression.
    def visitConditionExpression(self, ctx:Parser.ConditionExpressionContext):#same as conditionAssignmentExpression
        return self.visit(ctx.conditionAssignmentExpression())


    # Visit a parse tree produced by Parser#conditionAssignmentExpression.
    def visitConditionAssignmentExpression(self, ctx:Parser.ConditionAssignmentExpressionContext):#treat like normal expression first
        if ctx.assignmentOperator():
            return ast_nodes.PrimitiveExpression(op=self.visit(ctx.assignmentOperator()),expressions=[self.visit(ctx.conditionLogicalOrExpression()),self.visit(ctx.conditionExpression())])
        else:
            return self.visit(ctx.conditionLogicalOrExpression())


    # Visit a parse tree produced by Parser#conditionLogicalOrExpression.
    def visitConditionLogicalOrExpression(self, ctx:Parser.ConditionLogicalOrExpressionContext):
        if len(ctx.conditionLogicalAndExpression())>1:
            return ast_nodes.PrimitiveExpression(op="or",expressions=[self.visit(ctx.conditionLogicalAndExpression(i)) for i in range(len(ctx.conditionLogicalAndExpression()))])
        else:
            return self.visit(ctx.conditionLogicalAndExpression(0))


    # Visit a parse tree produced by Parser#conditionLogicalAndExpression.
    def visitConditionLogicalAndExpression(self, ctx:Parser.ConditionLogicalAndExpressionContext):
        if len(ctx.conditionComparisonExpression())>1:
            return ast_nodes.PrimitiveExpression(op="and",expressions=[self.visit(ctx.conditionComparisonExpression(i)) for i in range(len(ctx.conditionComparisonExpression()))])
        else:
            return self.visit(ctx.conditionComparisonExpression(0))


    # Visit a parse tree produced by Parser#conditionComparisonExpression.
    def visitConditionComparisonExpression(self, ctx:Parser.ConditionComparisonExpressionContext):
        if ctx.LT():
            return ast_nodes.PrimitiveExpression(op="<",expressions=[self.visit(ctx.conditionClosedBitOrExpression()),self.visit(ctx.conditionBitOrExpression(0))])
        elif ctx.comparisonExceptLt():
            return ast_nodes.PrimitiveExpression(op=self.visit(ctx.comparisonExceptLt()),expressions=[self.visit(ctx.conditionBitOrExpression(0)),self.visit(ctx.conditionBitOrExpression(1))])
        else:
            return self.visit(ctx.conditionBitOrExpression(0))


    # Visit a parse tree produced by Parser#conditionBitOrExpression.
    def visitConditionBitOrExpression(self, ctx:Parser.ConditionBitOrExpressionContext):
        if len(ctx.conditionBitXorExpression())>1:
            return ast_nodes.PrimitiveExpression(op="|",expressions=[self.visit(ctx.conditionBitXorExpression(i)) for i in range(len(ctx.conditionBitXorExpression()))])
        else:
            return self.visit(ctx.conditionBitXorExpression(0))


    # Visit a parse tree produced by Parser#conditionClosedBitOrExpression.
    def visitConditionClosedBitOrExpression(self, ctx:Parser.ConditionClosedBitOrExpressionContext):
        if len(ctx.conditionBitXorExpression())==0:
                return self.visit(ctx.conditionClosedBitXorExpression())
        return ast_nodes.PrimitiveExpression(op="|",expressions=[self.visit(ctx.conditionBitXorExpression(i)) for i in range(len(ctx.conditionBitXorExpression()))]+[self.visit(ctx.conditionClosedBitXorExpression())])
        


    # Visit a parse tree produced by Parser#conditionBitXorExpression.
    def visitConditionBitXorExpression(self, ctx:Parser.ConditionBitXorExpressionContext):
        if len(ctx.conditionBitAndExpression())>1:
            return ast_nodes.PrimitiveExpression(op="^",expressions=[self.visit(ctx.conditionBitAndExpression(i)) for i in range(len(ctx.conditionBitAndExpression()))])
        else:
            return self.visit(ctx.conditionBitAndExpression(0))


    # Visit a parse tree produced by Parser#conditionClosedBitXorExpression.
    def visitConditionClosedBitXorExpression(self, ctx:Parser.ConditionClosedBitXorExpressionContext):
        if len(ctx.conditionBitAndExpression())==0:
                return self.visit(ctx.conditionClosedBitAndExpression())
        return ast_nodes.PrimitiveExpression(op="^",expressions=[self.visit(ctx.conditionBitAndExpression(i)) for i in range(len(ctx.conditionBitAndExpression()))]+[self.visit(ctx.conditionClosedBitAndExpression())])
        


    # Visit a parse tree produced by Parser#conditionBitAndExpression.
    def visitConditionBitAndExpression(self, ctx:Parser.ConditionBitAndExpressionContext):
        if len(ctx.conditionShiftExpression())>1:
            return ast_nodes.PrimitiveExpression(op="&",expressions=[self.visit(ctx.conditionShiftExpression(i)) for i in range(len(ctx.conditionShiftExpression()))])
        else:
            return self.visit(ctx.conditionShiftExpression(0))


    # Visit a parse tree produced by Parser#conditionClosedBitAndExpression.
    def visitConditionClosedBitAndExpression(self, ctx:Parser.ConditionClosedBitAndExpressionContext):
        if len(ctx.conditionShiftExpression())==0:
            return self.visit(ctx.conditionClosedShiftExpression())
        return ast_nodes.PrimitiveExpression(op="&",expressions=[self.visit(ctx.conditionShiftExpression(i)) for i in range(len(ctx.conditionShiftExpression()))]+[self.visit(ctx.conditionClosedShiftExpression())])
    


    # Visit a parse tree produced by Parser#conditionShiftExpression.
    def visitConditionShiftExpression(self, ctx:Parser.ConditionShiftExpressionContext):
        if ctx.SHL() or ctx.shiftRight():
            ops=[]
            expressions=[]
            for i in range(0,ctx.getChildCount()-1,2):
                expressions.append(self.visit(ctx.getChild(i)))
                ops.append(ctx.getChild(i+1).getText())
            expressions.append(self.visit(ctx.getChild(ctx.getChildCount()-1)))
            return ast_nodes.ExtraExpression(op='shift',expressions=expressions,ops=ops)
        else:
            return self.visit(ctx.conditionAdditiveExpression(0))


    # Visit a parse tree produced by Parser#conditionClosedShiftExpression.
    def visitConditionClosedShiftExpression(self, ctx:Parser.ConditionClosedShiftExpressionContext):
        if ctx.SHL() or ctx.shiftRight():
            ops=[]
            expressions=[]
            for i in range(0,ctx.getChildCount()-1,2):
                expressions.append(self.visit(ctx.getChild(i)))
                ops.append(ctx.getChild(i+1).getText())
            expressions.append(self.visit(ctx.getChild(ctx.getChildCount()-1)))
            return ast_nodes.ExtraExpression(op='shift',expressions=expressions,ops=ops)
        else:
            return self.visit(ctx.conditionClosedAdditiveExpression(0))


    # Visit a parse tree produced by Parser#conditionAdditiveExpression.
    def visitConditionAdditiveExpression(self, ctx:Parser.ConditionAdditiveExpressionContext):
        if len(ctx.conditionMultiplicativeExpression())>1:
            return ast_nodes.ExtraExpression(op="+",expressions=[self.visit(ctx.conditionMultiplicativeExpression(i)) for i in range(len(ctx.conditionMultiplicativeExpression()))],ops=['+']+[self.visit(ctx.additiveOperator(i)) for i in range(len(ctx.additiveOperator()))])
        else:
            return self.visit(ctx.conditionMultiplicativeExpression(0))


    # Visit a parse tree produced by Parser#conditionClosedAdditiveExpression.
    def visitConditionClosedAdditiveExpression(self, ctx:Parser.ConditionClosedAdditiveExpressionContext):
        if len(ctx.conditionMultiplicativeExpression())==0:
            return self.visit(ctx.conditionClosedMultiplicativeExpression())
        return ast_nodes.ExtraExpression(op="+",expressions=[self.visit(ctx.conditionMultiplicativeExpression(i)) for i in range(len(ctx.conditionMultiplicativeExpression()))]+[self.visit(ctx.conditionClosedMultiplicativeExpression())],ops=['+']+[self.visit(ctx.additiveOperator(i)) for i in range(len(ctx.additiveOperator()))])
               


    # Visit a parse tree produced by Parser#conditionMultiplicativeExpression.
    def visitConditionMultiplicativeExpression(self, ctx:Parser.ConditionMultiplicativeExpressionContext):
        if len(ctx.conditionCastExpression())>1:
            return ast_nodes.ExtraExpression(op="*",expressions=[self.visit(ctx.conditionCastExpression(i)) for i in range(len(ctx.conditionCastExpression()))],ops=['*']+[self.visit(ctx.multiplicativeOperator(i)) for i in range(len(ctx.multiplicativeOperator()))])
        else:
            return self.visit(ctx.conditionCastExpression(0))


    # Visit a parse tree produced by Parser#conditionClosedMultiplicativeExpression.
    def visitConditionClosedMultiplicativeExpression(self, ctx:Parser.ConditionClosedMultiplicativeExpressionContext):
        if len(ctx.conditionCastExpression())==0:
            return self.visit(ctx.conditionClosedCastExpression())
        return ast_nodes.ExtraExpression(op="*",expressions=[self.visit(ctx.conditionCastExpression(i)) for i in range(len(ctx.conditionCastExpression()))]+[self.visit(ctx.conditionClosedCastExpression())],ops=['*']+[self.visit(ctx.multiplicativeOperator(i)) for i in range(len(ctx.multiplicativeOperator()))])
                       
        
    # Visit a parse tree produced by Parser#conditionCastExpression.
    def visitConditionCastExpression(self, ctx:Parser.ConditionCastExpressionContext):
        if len(ctx.typeRef())>0:
            return ast_nodes.CastExpression(unaryExpression=self.visit(ctx.conditionUnaryExpression()),typeRefs=[self.visit(ctx.typeRef(i)) for i in range(len(ctx.typeRef()))])
        else:
            return self.visit(ctx.conditionUnaryExpression())

    # Visit a parse tree produced by Parser#conditionClosedCastExpression.
    def visitConditionClosedCastExpression(self, ctx:Parser.ConditionClosedCastExpressionContext):
        if ctx.conditionUnaryExpression():
            return self.visit(ctx.conditionUnaryExpression())
        castExpression=self.visit(ctx.conditionCastExpression())
        return ast_nodes.CastExpression(unaryExpression=castExpression.unaryExpression,typeRefs=castExpression.typeRefs+[self.visit(ctx.closedCastType())])
                
    # Visit a parse tree produced by Parser#conditionUnaryExpression.
    def visitConditionUnaryExpression(self, ctx:Parser.ConditionUnaryExpressionContext):
        if ctx.unaryOperator():
                unaryExpression=self.visit(ctx.conditionUnaryExpression())
                #quadratic time, may need to optimize!
                return ast_nodes.UnaryExpression(ops=[self.visit(ctx.unaryOperator())]+unaryExpression.ops,postfixExpression=unaryExpression.postfixExpression)
        return ast_nodes.UnaryExpression(ops=[],postfixExpression=self.visit(ctx.conditionPostfixExpression()))

    # Visit a parse tree produced by Parser#conditionPostfixExpression.
    def visitConditionPostfixExpression(self, ctx:Parser.ConditionPostfixExpressionContext):
        return ast_nodes.PostfixExpression(primaryExpression=self.visit(ctx.conditionPrimary()),postfixSuffixes=[self.visit(ctx.postfixSuffix(i)) for i in range(len(ctx.postfixSuffix()))])

    def visitConditionBreakExpression(self, ctx:Parser.ConditionBreakExpressionContext):#same as conditionBreakAssignmentExpression
        return self.visit(ctx.conditionBreakAssignmentExpression())


    # Visit a parse tree produced by Parser#conditionBreakAssignmentExpression.
    def visitConditionBreakAssignmentExpression(self, ctx:Parser.ConditionBreakAssignmentExpressionContext):#treat like normal expression first
        if ctx.assignmentOperator():
            return ast_nodes.PrimitiveExpression(op=self.visit(ctx.assignmentOperator()),expressions=[self.visit(ctx.conditionBreakLogicalOrExpression()),self.visit(ctx.conditionExpression())])
        else:
            return self.visit(ctx.conditionBreakLogicalOrExpression())


    # Visit a parse tree produced by Parser#conditionBreakLogicalOrExpression.
    def visitConditionBreakLogicalOrExpression(self, ctx:Parser.ConditionBreakLogicalOrExpressionContext):
        if len(ctx.conditionLogicalAndExpression())>0:
            return ast_nodes.PrimitiveExpression(op="or",expressions=[self.visit(ctx.conditionBreakLogicalAndExpression())]+[self.visit(ctx.conditionLogicalAndExpression(i)) for i in range(len(ctx.conditionLogicalAndExpression()))])
        else:
            return self.visit(ctx.conditionBreakLogicalAndExpression())


    # Visit a parse tree produced by Parser#conditionBreakLogicalAndExpression.
    def visitConditionBreakLogicalAndExpression(self, ctx:Parser.ConditionBreakLogicalAndExpressionContext):
        if len(ctx.conditionComparisonExpression())>0:
            return ast_nodes.PrimitiveExpression(op="and",expressions=[self.visit(ctx.conditionBreakComparisonExpression())]+[self.visit(ctx.conditionComparisonExpression(i)) for i in range(len(ctx.conditionComparisonExpression()))])
        else:
            return self.visit(ctx.conditionBreakComparisonExpression())


    # Visit a parse tree produced by Parser#conditionBreakComparisonExpression.
    def visitConditionBreakComparisonExpression(self, ctx:Parser.ConditionBreakComparisonExpressionContext):
        if ctx.LT():
            return ast_nodes.PrimitiveExpression(op="<",expressions=[self.visit(ctx.conditionBreakClosedBitOrExpression()),self.visit(ctx.conditionBitOrExpression())])
        elif ctx.comparisonExceptLt():
            return ast_nodes.PrimitiveExpression(op=self.visit(ctx.comparisonExceptLt()),expressions=[self.visit(ctx.conditionBreakBitOrExpression()),self.visit(ctx.conditionBitOrExpression())])
        else:
            return self.visit(ctx.conditionBreakBitOrExpression())


    # Visit a parse tree produced by Parser#conditionBreakBitOrExpression.
    def visitConditionBreakBitOrExpression(self, ctx:Parser.ConditionBreakBitOrExpressionContext):
        if len(ctx.conditionBitXorExpression())>0:
            return ast_nodes.PrimitiveExpression(op="|",expressions=[self.visit(ctx.conditionBreakBitXorExpression())]+[self.visit(ctx.conditionBitXorExpression(i)) for i in range(len(ctx.conditionBitXorExpression()))])
        else:
            return self.visit(ctx.conditionBreakBitXorExpression())


    # Visit a parse tree produced by Parser#conditionBreakClosedBitOrExpression.
    def visitConditionBreakClosedBitOrExpression(self, ctx:Parser.ConditionBreakClosedBitOrExpressionContext):
        if ctx.conditionBreakClosedBitXorExpression():
            return self.visit(ctx.conditionBreakClosedBitXorExpression())
        else:
            return ast_nodes.PrimitiveExpression(op="|",expressions=[self.visit(ctx.conditionBreakBitXorExpression())]+ [self.visit(ctx.conditionBitXorExpression(i)) for i in range(len(ctx.conditionBitXorExpression()))]+[self.visit(ctx.conditionClosedBitXorExpression())])
        


    # Visit a parse tree produced by Parser#conditionBreakBitXorExpression.
    def visitConditionBreakBitXorExpression(self, ctx:Parser.ConditionBreakBitXorExpressionContext):
        if len(ctx.conditionBitAndExpression())>0:
            return ast_nodes.PrimitiveExpression(op="^",expressions=[self.visit(ctx.conditionBreakBitAndExpression())]+[self.visit(ctx.conditionBitAndExpression(i)) for i in range(len(ctx.conditionBitAndExpression()))])
        else:
            return self.visit(ctx.conditionBreakBitAndExpression())


    # Visit a parse tree produced by Parser#conditionBreakClosedBitXorExpression.
    def visitConditionBreakClosedBitXorExpression(self, ctx:Parser.ConditionBreakClosedBitXorExpressionContext):
        if ctx.conditionBreakClosedBitAndExpression():
            return self.visit(ctx.conditionBreakClosedBitAndExpression())
        else:
            return ast_nodes.PrimitiveExpression(op="^",expressions=[self.visit(ctx.conditionBreakBitAndExpression())]+ [self.visit(ctx.conditionBitAndExpression(i)) for i in range(len(ctx.conditionBitAndExpression()))]+[self.visit(ctx.conditionClosedBitAndExpression())])
                
        


    # Visit a parse tree produced by Parser#conditionBreakBitAndExpression.
    def visitConditionBreakBitAndExpression(self, ctx:Parser.ConditionBreakBitAndExpressionContext):
        if len(ctx.conditionShiftExpression())>0:
            return ast_nodes.PrimitiveExpression(op="&",expressions=[self.visit(ctx.conditionBreakShiftExpression())]+[self.visit(ctx.conditionShiftExpression(i)) for i in range(len(ctx.conditionShiftExpression()))])
        else:
            return self.visit(ctx.conditionBreakShiftExpression())


    # Visit a parse tree produced by Parser#conditionBreakClosedBitAndExpression.
    def visitConditionBreakClosedBitAndExpression(self, ctx:Parser.ConditionBreakClosedBitAndExpressionContext):
        if ctx.conditionBreakClosedShiftExpression():
            return self.visit(ctx.conditionBreakClosedShiftExpression())
        else:
            return ast_nodes.PrimitiveExpression(op="&",expressions=[self.visit(ctx.conditionBreakShiftExpression())]+ [self.visit(ctx.conditionShiftExpression(i)) for i in range(len(ctx.conditionShiftExpression()))]+[self.visit(ctx.conditionClosedShiftExpression())])
                    

    # Visit a parse tree produced by Parser#conditionBreakShiftExpression.
    def visitConditionBreakShiftExpression(self, ctx:Parser.ConditionBreakShiftExpressionContext):
        if ctx.SHL() or ctx.shiftRight():
            ops=[]
            expressions=[]
            for i in range(0,ctx.getChildCount()-1,2):
                expressions.append(self.visit(ctx.getChild(i)))
                ops.append(ctx.getChild(i+1).getText())
            expressions.append(self.visit(ctx.getChild(ctx.getChildCount()-1)))
            return ast_nodes.ExtraExpression(op='shift',expressions=expressions,ops=ops)
        else:
            return self.visit(ctx.conditionBreakAdditiveExpression())


    # Visit a parse tree produced by Parser#conditionBreakClosedShiftExpression.
    def visitConditionBreakClosedShiftExpression(self, ctx:Parser.ConditionBreakClosedShiftExpressionContext):
        if ctx.SHL() or ctx.shiftRight():
            ops=[]
            expressions=[]
            for i in range(0,ctx.getChildCount()-1,2):
                expressions.append(self.visit(ctx.getChild(i)))
                ops.append(ctx.getChild(i+1).getText())
            expressions.append(self.visit(ctx.getChild(ctx.getChildCount()-1)))
            return ast_nodes.ExtraExpression(op='shift',expressions=expressions,ops=ops)
        else:
            return self.visit(ctx.conditionBreakClosedAdditiveExpression())


    # Visit a parse tree produced by Parser#conditionBreakAdditiveExpression.
    def visitConditionBreakAdditiveExpression(self, ctx:Parser.ConditionBreakAdditiveExpressionContext):
        if len(ctx.conditionMultiplicativeExpression())>0:
            return ast_nodes.ExtraExpression(op="+",expressions=[self.visit(ctx.conditionBreakMultiplicativeExpression())]+[self.visit(ctx.conditionMultiplicativeExpression(i)) for i in range(len(ctx.conditionMultiplicativeExpression()))],ops=['+']+[self.visit(ctx.additiveOperator(i)) for i in range(len(ctx.additiveOperator()))])
        else:
            return self.visit(ctx.conditionBreakMultiplicativeExpression())
        


    # Visit a parse tree produced by Parser#conditionBreakClosedAdditiveExpression.
    def visitConditionBreakClosedAdditiveExpression(self, ctx:Parser.ConditionBreakClosedAdditiveExpressionContext):
        if ctx.conditionBreakClosedMultiplicativeExpression():
            return self.visit(ctx.conditionBreakClosedMultiplicativeExpression())
        else:
            return ast_nodes.ExtraExpression(op="+",expressions=[self.visit(ctx.conditionBreakMultiplicativeExpression())]+ [self.visit(ctx.conditionMultiplicativeExpression(i)) for i in range(len(ctx.conditionMultiplicativeExpression()))]+[self.visit(ctx.conditionClosedMultiplicativeExpression())],ops=['+']+[self.visit(ctx.additiveOperator(i)) for i in range(len(ctx.additiveOperator()))])
                            
        

    # Visit a parse tree produced by Parser#conditionBreakMultiplicativeExpression.
    def visitConditionBreakMultiplicativeExpression(self, ctx:Parser.ConditionBreakMultiplicativeExpressionContext):
        if len(ctx.conditionCastExpression())>0:
            return ast_nodes.ExtraExpression(op="*",expressions=[self.visit(ctx.conditionBreakCastExpression())]+[self.visit(ctx.conditionCastExpression(i)) for i in range(len(ctx.conditionCastExpression()))],ops=['*']+[self.visit(ctx.multiplicativeOperator(i)) for i in range(len(ctx.multiplicativeOperator()))])
        else:
            return self.visit(ctx.conditionBreakCastExpression())
                
        


    # Visit a parse tree produced by Parser#conditionBreakClosedMultiplicativeExpression.
    def visitConditionBreakClosedMultiplicativeExpression(self, ctx:Parser.ConditionBreakClosedMultiplicativeExpressionContext):
        if ctx.conditionBreakClosedCastExpression():
            return self.visit(ctx.conditionBreakClosedCastExpression())
        else:
            return ast_nodes.ExtraExpression(op="*",expressions=[self.visit(ctx.conditionBreakCastExpression())]+ [self.visit(ctx.conditionCastExpression(i)) for i in range(len(ctx.conditionCastExpression()))]+[self.visit(ctx.conditionClosedCastExpression())],ops=['*']+[self.visit(ctx.multiplicativeOperator(i)) for i in range(len(ctx.multiplicativeOperator()))])
                                      
        
    # Visit a parse tree produced by Parser#conditionBreakCastExpression.
    def visitConditionBreakCastExpression(self, ctx:Parser.ConditionBreakCastExpressionContext):
        if len(ctx.typeRef())>0:
            return ast_nodes.CastExpression(unaryExpression=self.visit(ctx.conditionBreakUnaryExpression()),typeRefs=[self.visit(ctx.typeRef(i)) for i in range(len(ctx.typeRef()))])
        else:
            return self.visit(ctx.conditionBreakUnaryExpression())

        
    # Visit a parse tree produced by Parser#conditionBreakClosedCastExpression.
    def visitConditionBreakClosedCastExpression(self, ctx:Parser.ConditionBreakClosedCastExpressionContext):
        if ctx.conditionBreakUnaryExpression():
            return self.visit(ctx.conditionBreakUnaryExpression())
        else:
            castExpression=self.visit(ctx.conditionBreakCastExpression())
            return ast_nodes.CastExpression(unaryExpression=castExpression.unaryExpression,typeRefs=castExpression.typeRefs+[self.visit(ctx.closedCastType())])
                
    # Visit a parse tree produced by Parser#conditionBreakUnaryExpression.
    def visitConditionBreakUnaryExpression(self, ctx:Parser.ConditionBreakUnaryExpressionContext):
        if ctx.unaryOperator():
                unaryExpression=self.visit(ctx.conditionUnaryExpression())
                #quadratic time, may need to optimize!
                return ast_nodes.UnaryExpression(ops=[self.visit(ctx.unaryOperator())]+unaryExpression.ops,postfixExpression=unaryExpression.postfixExpression)
        else:
            return ast_nodes.UnaryExpression(ops=[],postfixExpression=self.visit(ctx.conditionBreakPostfixExpression()))

    # Visit a parse tree produced by Parser#conditionBreakPostfixExpression.
    def visitConditionBreakPostfixExpression(self, ctx:Parser.ConditionBreakPostfixExpressionContext):
        return ast_nodes.PostfixExpression(primaryExpression=self.visit(ctx.conditionPrimaryWithoutBareBlock()),postfixSuffixes=[self.visit(ctx.postfixSuffix(i)) for i in range(len(ctx.postfixSuffix()))])

    # Visit a parse tree produced by Parser#statementExpression.
    def visitStatementExpression(self, ctx:Parser.StatementExpressionContext):#same as statementAssignmentExpression
        return self.visit(ctx.statementAssignmentExpression())


    # Visit a parse tree produced by Parser#statementAssignmentExpression.
    def visitStatementAssignmentExpression(self, ctx:Parser.StatementAssignmentExpressionContext):#treat like normal expression first
        if ctx.assignmentOperator():
            return ast_nodes.PrimitiveExpression(op=self.visit(ctx.assignmentOperator()),expressions=[self.visit(ctx.statementLogicalOrExpression()),self.visit(ctx.expression())])
        else:
            return self.visit(ctx.statementLogicalOrExpression())


    # Visit a parse tree produced by Parser#statementLogicalOrExpression.
    def visitStatementLogicalOrExpression(self, ctx:Parser.StatementLogicalOrExpressionContext):
        if len(ctx.logicalAndExpression())>0:
            return ast_nodes.PrimitiveExpression(op="or",expressions=[self.visit(ctx.statementLogicalAndExpression())]+[self.visit(ctx.logicalAndExpression(i)) for i in range(len(ctx.logicalAndExpression()))])
        else:
            return self.visit(ctx.statementLogicalAndExpression())


    # Visit a parse tree produced by Parser#statementLogicalAndExpression.
    def visitStatementLogicalAndExpression(self, ctx:Parser.StatementLogicalAndExpressionContext):
        if len(ctx.comparisonExpression())>0:
            return ast_nodes.PrimitiveExpression(op="and",expressions=[self.visit(ctx.statementComparisonExpression())]+[self.visit(ctx.comparisonExpression(i)) for i in range(len(ctx.comparisonExpression()))])
        else:
            return self.visit(ctx.statementComparisonExpression())


    # Visit a parse tree produced by Parser#statementComparisonExpression.
    def visitStatementComparisonExpression(self, ctx:Parser.StatementComparisonExpressionContext):
        if ctx.LT():
            return ast_nodes.PrimitiveExpression(op="<",expressions=[self.visit(ctx.statementClosedBitOrExpression()),self.visit(ctx.bitOrExpression())])
        elif ctx.comparisonExceptLt():
            return ast_nodes.PrimitiveExpression(op=self.visit(ctx.comparisonExceptLt()),expressions=[self.visit(ctx.statementBitOrExpression()),self.visit(ctx.bitOrExpression())])
        else:
            return self.visit(ctx.statementBitOrExpression())


    # Visit a parse tree produced by Parser#statementBitOrExpression.
    def visitStatementBitOrExpression(self, ctx:Parser.StatementBitOrExpressionContext):
        if len(ctx.bitXorExpression())>0:
            return ast_nodes.PrimitiveExpression(op="|",expressions=[self.visit(ctx.statementBitXorExpression())]+[self.visit(ctx.bitXorExpression(i)) for i in range(len(ctx.bitXorExpression()))])
        else:
            return self.visit(ctx.statementBitXorExpression())


    # Visit a parse tree produced by Parser#statementClosedBitOrExpression.
    def visitStatementClosedBitOrExpression(self, ctx:Parser.StatementClosedBitOrExpressionContext):
        if ctx.statementClosedBitXorExpression():
            return self.visit(ctx.statementClosedBitXorExpression())
        return ast_nodes.PrimitiveExpression(op="|",expressions=[self.visit(ctx.statementBitXorExpression())]+[self.visit(ctx.bitXorExpression(i)) for i in range(len(ctx.bitXorExpression()))]+[self.visit(ctx.closedBitXorExpression())])
        


    # Visit a parse tree produced by Parser#statementBitXorExpression.
    def visitStatementBitXorExpression(self, ctx:Parser.StatementBitXorExpressionContext):
        if len(ctx.bitAndExpression())>0:
            return ast_nodes.PrimitiveExpression(op="^",expressions=[self.visit(ctx.statementBitAndExpression())]+[self.visit(ctx.bitAndExpression(i)) for i in range(len(ctx.bitAndExpression()))])
        else:
            return self.visit(ctx.statementBitAndExpression())


    # Visit a parse tree produced by Parser#statementClosedBitXorExpression.
    def visitStatementClosedBitXorExpression(self, ctx:Parser.StatementClosedBitXorExpressionContext):
        if ctx.statementClosedBitAndExpression():
            return self.visit(ctx.statementClosedBitAndExpression())
        return ast_nodes.PrimitiveExpression(op="^",expressions=[self.visit(ctx.statementBitAndExpression())]+[self.visit(ctx.bitAndExpression(i)) for i in range(len(ctx.bitAndExpression()))]+[self.visit(ctx.closedBitAndExpression())])


    # Visit a parse tree produced by Parser#statementBitAndExpression.
    def visitStatementBitAndExpression(self, ctx:Parser.StatementBitAndExpressionContext):
        if len(ctx.shiftExpression())==0:
            return self.visit(ctx.statementShiftExpression())
        return ast_nodes.PrimitiveExpression(op="&",expressions=[self.visit(ctx.statementShiftExpression())]+[self.visit(ctx.shiftExpression(i)) for i in range(len(ctx.shiftExpression()))])
            
        


    # Visit a parse tree produced by Parser#statementClosedBitAndExpression.
    def visitStatementClosedBitAndExpression(self, ctx:Parser.StatementClosedBitAndExpressionContext):
        if ctx.statementClosedShiftExpression():
            return self.visit(ctx.statementClosedShiftExpression())
        return ast_nodes.PrimitiveExpression(op="&",expressions=[self.visit(ctx.statementShiftExpression())]+[self.visit(ctx.shiftExpression(i)) for i in range(len(ctx.shiftExpression()))]+[self.visit(ctx.closedShiftExpression())])
                 
        

    # Visit a parse tree produced by Parser#statementShiftExpression.
    def visitStatementShiftExpression(self, ctx:Parser.StatementShiftExpressionContext):
        if ctx.SHL() or ctx.shiftRight():
            ops=[]
            expressions=[]
            for i in range(0,ctx.getChildCount()-1,2):
                expressions.append(self.visit(ctx.getChild(i)))
                ops.append(ctx.getChild(i+1).getText())
            expressions.append(self.visit(ctx.getChild(ctx.getChildCount()-1)))
            return ast_nodes.ExtraExpression(op='shift',expressions=expressions,ops=ops)
        else:
            return self.visit(ctx.statementAdditiveExpression())


    # Visit a parse tree produced by Parser#statementClosedShiftExpression.
    def visitStatementClosedShiftExpression(self, ctx:Parser.StatementClosedShiftExpressionContext):
        if ctx.SHL() or ctx.shiftRight():
            ops=[]
            expressions=[]
            for i in range(0,ctx.getChildCount()-1,2):
                expressions.append(self.visit(ctx.getChild(i)))
                ops.append(ctx.getChild(i+1).getText())
            expressions.append(self.visit(ctx.getChild(ctx.getChildCount()-1)))
            return ast_nodes.ExtraExpression(op='shift',expressions=expressions,ops=ops)
        else:
            return self.visit(ctx.statementClosedAdditiveExpression())


    # Visit a parse tree produced by Parser#statementAdditiveExpression.
    def visitStatementAdditiveExpression(self, ctx:Parser.StatementAdditiveExpressionContext):
        if len(ctx.multiplicativeExpression())>0:
            return ast_nodes.ExtraExpression(op="+",expressions=[self.visit(ctx.statementMultiplicativeExpression())]+[self.visit(ctx.multiplicativeExpression(i)) for i in range(len(ctx.multiplicativeExpression()))],ops=['+']+[self.visit(ctx.additiveOperator(i)) for i in range(len(ctx.additiveOperator()))])
        else:
            return self.visit(ctx.statementMultiplicativeExpression())


    # Visit a parse tree produced by Parser#statementClosedAdditiveExpression.
    def visitStatementClosedAdditiveExpression(self, ctx:Parser.StatementClosedAdditiveExpressionContext):
        if ctx.statementClosedMultiplicativeExpression():
            return self.visit(ctx.statementClosedMultiplicativeExpression())
        else:
            return ast_nodes.ExtraExpression(op="+",expressions=[self.visit(ctx.statementMultiplicativeExpression())]+[self.visit(ctx.multiplicativeExpression(i)) for i in range(len(ctx.multiplicativeExpression()))]+[self.visit(ctx.closedMultiplicativeExpression())],ops=['+']+[self.visit(ctx.additiveOperator(i)) for i in range(len(ctx.additiveOperator()))])
               


    # Visit a parse tree produced by Parser#statementMultiplicativeExpression.
    def visitStatementMultiplicativeExpression(self, ctx:Parser.StatementMultiplicativeExpressionContext):
        if len(ctx.castExpression())>0:
            return ast_nodes.ExtraExpression(op="*",expressions=[self.visit(ctx.statementCastExpression())]+[self.visit(ctx.castExpression(i)) for i in range(len(ctx.castExpression()))],ops=['*']+[self.visit(ctx.multiplicativeOperator(i)) for i in range(len(ctx.multiplicativeOperator()))])
        else:
            return self.visit(ctx.statementCastExpression())


    # Visit a parse tree produced by Parser#statementClosedMultiplicativeExpression.
    def visitStatementClosedMultiplicativeExpression(self, ctx:Parser.StatementClosedMultiplicativeExpressionContext):
        if ctx.statementClosedCastExpression():
            return self.visit(ctx.statementClosedCastExpression())
        else:
            return ast_nodes.ExtraExpression(op="*",expressions=[self.visit(ctx.statementCastExpression())]+[self.visit(ctx.castExpression(i)) for i in range(len(ctx.castExpression()))]+[self.visit(ctx.closedCastExpression())],ops=['*']+[self.visit(ctx.multiplicativeOperator(i)) for i in range(len(ctx.multiplicativeOperator()))])
                               
        
    # Visit a parse tree produced by Parser#statementCastExpression.
    def visitStatementCastExpression(self, ctx:Parser.StatementCastExpressionContext):
        if len(ctx.typeRef())>0:
            return ast_nodes.CastExpression(unaryExpression=self.visit(ctx.statementUnaryExpression()),typeRefs=[self.visit(ctx.typeRef(i)) for i in range(len(ctx.typeRef()))])
        else:
            return self.visit(ctx.statementUnaryExpression())

        
    # Visit a parse tree produced by Parser#statementClosedCastExpression.
    def visitStatementClosedCastExpression(self, ctx:Parser.StatementClosedCastExpressionContext):
        if ctx.statementUnaryExpression():
            return self.visit(ctx.statementUnaryExpression())
        castExpression=self.visit(ctx.statementCastExpression())
        return ast_nodes.CastExpression(unaryExpression=castExpression.unaryExpression,typeRefs=castExpression.typeRefs+[self.visit(ctx.closedCastType())])
                
    # Visit a parse tree produced by Parser#statementUnaryExpression.
    def visitStatementUnaryExpression(self, ctx:Parser.StatementUnaryExpressionContext):
        if ctx.unaryOperator():
                unaryExpression=self.visit(ctx.unaryExpression())
                #quadratic time, may need to optimize!
                return ast_nodes.UnaryExpression(ops=[self.visit(ctx.unaryOperator())]+unaryExpression.ops,postfixExpression=unaryExpression.postfixExpression)
        return ast_nodes.UnaryExpression(ops=[],postfixExpression=self.visit(ctx.statementPostfixExpression()))

    # Visit a parse tree produced by Parser#statementPostfixExpression.
    def visitStatementPostfixExpression(self, ctx:Parser.StatementPostfixExpressionContext):
        return ast_nodes.StatementPostfixExpression(primaryExpression=self.visit(ctx.nonBlockPrimary() if ctx.nonBlockPrimary() else ctx.expressionWithBlock()),postfixSuffixes=[self.visit(ctx.postfixSuffix(i)) for i in range(len(ctx.postfixSuffix()))],dotSuffix=self.visit(ctx.dotSuffix()) if ctx.dotSuffix() else None)


    # Visit a parse tree produced by Parser#primaryExpression.
    def visitPrimaryExpression(self, ctx:Parser.PrimaryExpressionContext):
        if ctx.nonBlockPrimary():
            return self.visit(ctx.nonBlockPrimary())
        else:
            return self.visit(ctx.expressionWithBlock())


    # Visit a parse tree produced by Parser#nonBlockPrimary.
    def visitNonBlockPrimary(self, ctx:Parser.NonBlockPrimaryContext):
        if ctx.literalExpression():
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.literalExpression()),type="literal",structExprFields=None)
        elif ctx.LPAREN():
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.expression()) if ctx.expression() else None,type="paren",structExprFields=None)
        elif ctx.arrayExpression():
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.arrayExpression()),type="array",structExprFields=None)
        elif ctx.BREAK():
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.expression()) if ctx.expression() else None,type="break",structExprFields=None)
        elif ctx.RETURN():
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.expression()) if ctx.expression() else None,type="return",structExprFields=None)
        elif ctx.CONTINUE():
            return ast_nodes.NonBlockPrimary(expression=None,type="continue",structExprFields=None)
        else:#PATH
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.pathInExpression()),type="path",structExprFields=self.visit(ctx.structExprFields()) if ctx.structExprFields() else None)


    # Visit a parse tree produced by Parser#conditionPrimary.
    def visitConditionPrimary(self, ctx:Parser.ConditionPrimaryContext):
        if ctx.conditionPrimaryWithoutBareBlock():
            return self.visit(ctx.conditionPrimaryWithoutBareBlock())
        else:
            return self.visit(ctx.blockExpression())


    # Visit a parse tree produced by Parser#conditionPrimaryWithoutBareBlock.
    def visitConditionPrimaryWithoutBareBlock(self, ctx:Parser.ConditionPrimaryWithoutBareBlockContext):
        if ctx.literalExpression():
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.literalExpression()),type="literal",structExprFields=None)
        elif ctx.LPAREN():
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.expression()) if ctx.expression() else None,type="paren",structExprFields=None)
        elif ctx.arrayExpression():
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.arrayExpression()),type="array",structExprFields=None)
        elif ctx.BREAK():
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.conditionBreakExpression()) if ctx.conditionBreakExpression() else None,type="break",structExprFields=None)
        elif ctx.RETURN():
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.conditionExpression()) if ctx.conditionExpression() else None,type="return",structExprFields=None)
        elif ctx.CONTINUE():
            return ast_nodes.NonBlockPrimary(expression=None,type="continue",structExprFields=None)
        if ctx.ifExpression():
            return self.visit(ctx.ifExpression())
        elif ctx.LOOP() or ctx.WHILE():
            return ast_nodes.NormalExpressionWithBlock(blockExpression=self.visit(ctx.blockExpression()),loop=ctx.LOOP() or ctx.WHILE(),conditionExpression=self.visit(ctx.conditionExpression()) if ctx.conditionExpression() else None)   
        else:#PATH
            return ast_nodes.NonBlockPrimary(expression=self.visit(ctx.pathInExpression()),type="path",structExprFields=self.visit(ctx.structExprFields()) if ctx.structExprFields() else None)


    # Visit a parse tree produced by Parser#literalExpression.
    def visitLiteralExpression(self, ctx:Parser.LiteralExpressionContext):
        if ctx.INTEGER_LITERAL():
            value,type=ast_nodes.parseIntegerLiteral(ctx.INTEGER_LITERAL().getText())
            return ast_nodes.LiteralExpression(value=value,type=type)
        elif ctx.TRUE():
            return ast_nodes.LiteralExpression(value=True,type="bool")
        else:#false
            return ast_nodes.LiteralExpression(value=False,type="bool")


    # Visit a parse tree produced by Parser#structExprFields.
    def visitStructExprFields(self, ctx:Parser.StructExprFieldsContext):
        return [self.visit(ctx.structExprField(i)) for i in range(len(ctx.structExprField()))]


    # Visit a parse tree produced by Parser#structExprField.
    def visitStructExprField(self, ctx:Parser.StructExprFieldContext):
        return ast_nodes.StructExprField(identifier=self.visit(ctx.identifier()),expression=self.visit(ctx.expression()))


    # Visit a parse tree produced by Parser#arrayExpression.
    def visitArrayExpression(self, ctx:Parser.ArrayExpressionContext):
        if ctx.constValue():
            return ast_nodes.RepeatArrayExpression(expression=self.visit(ctx.expression(0)),length=self.visit(ctx.constValue()))
        else:
            return ast_nodes.NormalArrayExpresssion(expressions=[self.visit(ctx.expression(i)) for i in range(len(ctx.expression()))])


    # Visit a parse tree produced by Parser#postfixSuffix.
    def visitPostfixSuffix(self, ctx:Parser.PostfixSuffixContext):
        if ctx.callArguments():
            return self.visit(ctx.callArguments())
        elif ctx.dotSuffix():
            return self.visit(ctx.dotSuffix())
        else:#bracketSuffix
            return ast_nodes.BracketSuffix(expression=self.visit(ctx.expression()))


    # Visit a parse tree produced by Parser#dotSuffix.
    def visitDotSuffix(self, ctx:Parser.DotSuffixContext):
        if ctx.identifier():
            return ast_nodes.DotSuffixData(identifier=self.visit(ctx.identifier()))
        else:
            return ast_nodes.DotSuffixMethod(pathExprSegment=self.visit(ctx.pathExprSegment()),callarguments=self.visit(ctx.callArguments()))


    # Visit a parse tree produced by Parser#callArguments.
    def visitCallArguments(self, ctx:Parser.CallArgumentsContext):
        return [self.visit(ctx.expression(i)) for i in range(len(ctx.expression()))]


    # Visit a parse tree produced by Parser#unaryOperator.
    def visitUnaryOperator(self, ctx:Parser.UnaryOperatorContext):
        if ctx.AMP() or ctx.ANDAND():
            return ('&' if ctx.AMP() else '&&')+('mut' if ctx.MUT() else '')
        elif ctx.MINUS():
            return "minus"
        elif ctx.NOT():
            return "!"
        elif ctx.STAR():
            return "star"


    # Visit a parse tree produced by Parser#multiplicativeOperator.
    def visitMultiplicativeOperator(self, ctx:Parser.MultiplicativeOperatorContext):
        if ctx.STAR():
            return '*'
        elif ctx.SLASH():
            return '/'
        else:
            return '%'


    # Visit a parse tree produced by Parser#additiveOperator.
    def visitAdditiveOperator(self, ctx:Parser.AdditiveOperatorContext):
        return '+' if ctx.PLUS() else '-'


    # Visit a parse tree produced by Parser#shiftRight.
    def visitShiftRight(self, ctx:Parser.ShiftRightContext):
        return '>>'


    # Visit a parse tree produced by Parser#comparisonExceptLt.
    def visitComparisonExceptLt(self, ctx:Parser.ComparisonExceptLtContext):
        if ctx.genericClose():
            return self.visit(ctx.genericClose())
        else:
            return ctx.getText()


    # Visit a parse tree produced by Parser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:Parser.AssignmentOperatorContext):
        if ctx.equalsSign():
            return self.visit(ctx.equalsSign())
        else:
            return ctx.getText()


    # Visit a parse tree produced by Parser#equalsSign.
    def visitEqualsSign(self, ctx:Parser.EqualsSignContext):
        return '='


    # Visit a parse tree produced by Parser#identifier.
    def visitIdentifier(self, ctx:Parser.IdentifierContext):#return str
        #print("Visited identifier",ctx.getText())
        return ctx.getText()



del Parser