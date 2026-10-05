import sys
from antlr4 import FileStream, CommonTokenStream, Token
from frontend.generated.Lexer import Lexer
from frontend.generated.Parser import Parser
from frontend.generated.ParserVisitor import ParserVisitor
from semantic.checker import Checker
from semantic.errors import SemanticError
from pprint import pprint
from antlr4.error.ErrorListener import ErrorListener

class Listener(ErrorListener):
   def syntaxError(self):
    raise Exception()

    
def parse_file(file_name):
    file_stream=FileStream(file_name)
    listener = Listener()
    lexer=Lexer(file_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(listener)

    tokens=CommonTokenStream(lexer)#token stream
    parser=Parser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    tree=parser.crate() #CST
    return tree

def ast_build(file_name):
    tree=parse_file(sys.argv[1])
    visitor=ParserVisitor()
    return visitor.visitCrate(tree)

if __name__=="__main__":
    if len(sys.argv)<2:
        print("no file path provided!")
        sys.exit(0)
    try:
        crate=ast_build(sys.argv[1])
    except Exception as e:
        print("Parse Error!")
        sys.exit(1)
    checker=Checker(crate)
    try:
        checker.SymbolCollection()
    except SemanticError as e:
        print(e.errormessage)
        sys.exit(1)
    pprint(checker.ConstValues)
    #pprint(checker.FunctionDefinitions)