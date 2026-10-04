def visitStatementExpression(self, ctx:Parser.StatementExpressionContext):#same as statementAssignmentExpression
        return self.visit(ctx.statementAssignmentExpression())


    # Visit a parse tree produced by Parser#statementAssignmentExpression.
    def visitStatementAssignmentExpression(self, ctx:Parser.StatementAssignmentExpressionContext):#treat like normal expression first
        if ctx.assignmentOperator():
            return ast_nodes.PrimitiveExpression(op=self.visit(ctx.assignmentOperator()),expressions=[self.visit(ctx.statementLogicalOrExpression()),self.visit(ctx.statementExpression())])
        else:
            return self.visit(ctx.statementLogicalOrExpression())


    # Visit a parse tree produced by Parser#statementLogicalOrExpression.
    def visitStatementLogicalOrExpression(self, ctx:Parser.StatementLogicalOrExpressionContext):
        if len(ctx.statementLogicalAndExpression())>1:
            return ast_nodes.PrimitiveExpression(op="or",expressions=[self.visit(ctx.statementLogicalAndExpression(i)) for i in range(len(ctx.statementLogicalAndExpression()))])
        else:
            return self.visit(ctx.statementLogicalAndExpression(0))


    # Visit a parse tree produced by Parser#statementLogicalAndExpression.
    def visitStatementLogicalAndExpression(self, ctx:Parser.StatementLogicalAndExpressionContext):
        if len(ctx.statementComparisonExpression())>1:
            return ast_nodes.PrimitiveExpression(op="and",expressions=[self.visit(ctx.statementComparisonExpression(i)) for i in range(len(ctx.statementComparisonExpression()))])
        else:
            return self.visit(ctx.statementComparisonExpression(0))


    # Visit a parse tree produced by Parser#statementComparisonExpression.
    def visitStatementComparisonExpression(self, ctx:Parser.StatementComparisonExpressionContext):
        if ctx.LT():
            return ast_nodes.PrimitiveExpression(op="<",expressions=[self.visit(ctx.statementClosedBitOrExpression()),self.visit(ctx.statementBitOrExpression(0))])
        elif ctx.comparisonExceptLt():
            return ast_nodes.PrimitiveExpression(op=self.visit(ctx.comparisonExceptLt()),expressions=[self.visit(ctx.statementBitOrExpression(0)),self.visit(ctx.statementBitOrExpression(1))])
        else:
            return self.visit(ctx.statementBitOrExpression(0))


    # Visit a parse tree produced by Parser#statementBitOrExpression.
    def visitStatementBitOrExpression(self, ctx:Parser.StatementBitOrExpressionContext):
        if len(ctx.statementBitXorExpression())>1:
            return ast_nodes.PrimitiveExpression(op="|",expressions=[self.visit(ctx.statementBitXorExpression(i)) for i in range(len(ctx.statementBitXorExpression()))])
        else:
            return self.visit(ctx.statementBitXorExpression(0))


    # Visit a parse tree produced by Parser#statementClosedBitOrExpression.
    def visitStatementClosedBitOrExpression(self, ctx:Parser.StatementClosedBitOrExpressionContext):
        if len(ctx.statementBitXorExpression())==0:
                return self.visit(ctx.statementClosedBitXorExpression())
        return ast_nodes.PrimitiveExpression(op="|",expressions=[self.visit(ctx.statementBitXorExpression(i)) for i in range(len(ctx.statementBitXorExpression()))]+[self.visit(ctx.statementClosedBitXorExpression())])
        


    # Visit a parse tree produced by Parser#statementBitXorExpression.
    def visitStatementBitXorExpression(self, ctx:Parser.StatementBitXorExpressionContext):
        if len(ctx.statementBitAndExpression())>1:
            return ast_nodes.PrimitiveExpression(op="^",expressions=[self.visit(ctx.statementBitAndExpression(i)) for i in range(len(ctx.statementBitAndExpression()))])
        else:
            return self.visit(ctx.statementBitAndExpression(0))


    # Visit a parse tree produced by Parser#statementClosedBitXorExpression.
    def visitStatementClosedBitXorExpression(self, ctx:Parser.StatementClosedBitXorExpressionContext):
        if len(ctx.statementBitAndExpression())==0:
                return self.visit(ctx.statementClosedBitAndExpression())
        return ast_nodes.PrimitiveExpression(op="^",expressions=[self.visit(ctx.statementBitAndExpression(i)) for i in range(len(ctx.statementBitAndExpression()))]+[self.visit(ctx.statementClosedBitAndExpression())])
        


    # Visit a parse tree produced by Parser#statementBitAndExpression.
    def visitStatementBitAndExpression(self, ctx:Parser.StatementBitAndExpressionContext):
        if len(ctx.statementShiftExpression())>1:
            return ast_nodes.PrimitiveExpression(op="&",expressions=[self.visit(ctx.statementShiftExpression(i)) for i in range(len(ctx.statementShiftExpression()))])
        else:
            return self.visit(ctx.statementShiftExpression(0))


    # Visit a parse tree produced by Parser#statementClosedBitAndExpression.
    def visitStatementClosedBitAndExpression(self, ctx:Parser.StatementClosedBitAndExpressionContext):
        if len(ctx.statementShiftExpression())==0:
            return self.visit(ctx.statementClosedShiftExpression())
        return ast_nodes.PrimitiveExpression(op="&",expressions=[self.visit(ctx.statementShiftExpression(i)) for i in range(len(ctx.statementShiftExpression()))]+[self.visit(ctx.statementClosedShiftExpression())])
    


    # Visit a parse tree produced by Parser#statementShiftExpression.
    def visitStatementShiftExpression(self, ctx:Parser.StatementShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Parser#statementClosedShiftExpression.
    def visitStatementClosedShiftExpression(self, ctx:Parser.StatementClosedShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Parser#statementAdditiveExpression.
    def visitStatementAdditiveExpression(self, ctx:Parser.StatementAdditiveExpressionContext):
        if len(ctx.statementMultiplicativeExpression())>1:
            return ast_nodes.ExtraExpression(op="+",expressions=[self.visit(ctx.statementMultiplicativeExpression(i)) for i in range(len(ctx.statementMultiplicativeExpression()))],ops=['+']+[self.visit(ctx.additiveOperator(i)) for i in range(len(ctx.statementMultiplicativeExpression()))])
        else:
            return self.visit(ctx.statementMultiplicativeExpression(0))


    # Visit a parse tree produced by Parser#statementClosedAdditiveExpression.
    def visitStatementClosedAdditiveExpression(self, ctx:Parser.StatementClosedAdditiveExpressionContext):
        if len(ctx.statementMultiplicativeExpression())==0:
            return self.visit(ctx.statementClosedMultiplicativeExpression())
        return ast_nodes.ExtraExpression(op="+",expressions=[self.visit(ctx.statementMultiplicativeExpression(i)) for i in range(len(ctx.statementMultiplicativeExpression()))]+[self.visit(ctx.statementClosedMultiplicativeExpression())],ops=['+']+[self.visit(ctx.additiveOperator(i)) for i in range(len(ctx.additiveOperator()))])
               


    # Visit a parse tree produced by Parser#statementMultiplicativeExpression.
    def visitStatementMultiplicativeExpression(self, ctx:Parser.StatementMultiplicativeExpressionContext):
        if len(ctx.statementCastExpression())>1:
            return ast_nodes.ExtraExpression(op="*",expressions=[self.visit(ctx.statementCastExpression(i)) for i in range(len(ctx.statementCastExpression()))],ops=['*']+[self.visit(ctx.multiplicativeOperator(i)) for i in range(len(ctx.multiplicativeOperator()))])
        else:
            return self.visit(ctx.statementCastExpression(0))


    # Visit a parse tree produced by Parser#statementClosedMultiplicativeExpression.
    def visitStatementClosedMultiplicativeExpression(self, ctx:Parser.StatementClosedMultiplicativeExpressionContext):
        if len(ctx.statementCastExpression())==0:
            return self.visit(ctx.statementClosedCastExpression())
        return ast_nodes.ExtraExpression(op="*",expressions=[self.visit(ctx.statementClosedCastExpression(i)) for i in range(len(ctx.statementCastExpression()))]+[self.visit(ctx.statementClosedCastExpression())],ops=['*']+[self.visit(ctx.multiplicativeOperator(i)) for i in range(len(ctx.multiplicativeOperator()))])
                       
        
    # Visit a parse tree produced by Parser#statementCastExpression.
    def visitStatementCastExpression(self, ctx:Parser.StatementCastExpressionContext):
        return ast_nodes.CastExpression(unaryExpression=self.visit(ctx.statementUnaryExpression()),typeRefs=[self.visit(ctx.typeRef(i)) for i in range(len(ctx.typeRef()))])

    # Visit a parse tree produced by Parser#statementClosedCastExpression.
    def visitStatementClosedCastExpression(self, ctx:Parser.StatementClosedCastExpressionContext):
        if ctx.statementUnaryExpression():
            return self.visit(ctx.statementUnaryExpression())
        castExpression=self.visit(ctx.statementCastExpression())
        return ast_nodes.CastExpression(unaryExpression=castExpression.unaryExpression,typeRefs=castExpression.typeRefs+[self.visit(ctx.closedCastType())])
                
    # Visit a parse tree produced by Parser#statementUnaryExpression.
    def visitStatementUnaryExpression(self, ctx:Parser.StatementUnaryExpressionContext):
        if ctx.unaryOperator():
                unaryExpression=self.visit(ctx.statementUnaryExpression())
                #quadratic time, may need to optimize!
                return ast_nodes.UnaryExpression(ops=[self.visit(ctx.unaryOperator())]+unaryExpression.ops,postfixExpression=unaryExpression.postfixExpression)
        return ast_nodes.UnaryExpression(ops=[],postfixExpression=self.visit(ctx.statementPostfixExpression()))

    # Visit a parse tree produced by Parser#statementPostfixExpression.
    def visitStatementPostfixExpression(self, ctx:Parser.StatementPostfixExpressionContext):
        return ast_nodes.PostfixExpression(primaryExpression=self.visit(ctx.statementPrimary()),postfixSuffixes=[self.visit(ctx.postfixSuffix(i)) for i in range(len(ctx.postfixSuffix()))])
