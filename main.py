import sys
from antlr4 import FileStream, CommonTokenStream, Token
from frontend.generated.Lexer import Lexer
from frontend.generated.Parser import Parser
from frontend.generated.ParserVisitor import ParserVisitor
from semantic.checker import Checker
from semantic.errors import SemanticError
from pprint import pprint
from antlr4.error.ErrorListener import ErrorListener
from ir.builder import Builder
from codegen.generator import Generator
from codegen.model import *

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
    tree=parse_file(file_name)
    visitor=ParserVisitor()
    return visitor.visitCrate(tree)

if __name__=="__main__":#python3 main.py --stage <stage> <input_file> <output_file>
    if len(sys.argv)<4:
        print("no file path provided!")
        sys.exit(1)
    if sys.argv[1]!='--stage':
        print("unrecognized format")
        sys.exit(1)
    stage=sys.argv[2]
    try:
        crate=ast_build(sys.argv[3])
    except Exception as e:
        print("Parse Error!")
        sys.exit(1)
    checker=Checker(crate)
    try:
        checker.SemanticCheck()
    except SemanticError as e:
        print(e.errormessage)
        sys.exit(1)
    if stage=="semantic":
        sys.exit(0)
    if len(sys.argv)<5:
        print("no output file path provided!")
        sys.exit(1)
    builder=Builder(checker,sys.argv[4])
    functionDescriptions=builder.Build()
    if stage=="ir":
        sys.exit(0)
    generator=Generator(functionDescriptions,sys.argv[4])
    generator.Generate()
    if stage=="codegen":
        sys.exit(0)


    