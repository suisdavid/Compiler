import sys
from antlr4 import FileStream, CommonTokenStream, Token
from frontend.generated.Lexer import Lexer
from frontend.generated.Parser import Parser
from frontend.generated.ParserVisitor import ParserVisitor
from pprint import pprint

def parse_file(file_name):
    file_stream=FileStream(file_name)
    lexer=Lexer(file_stream)
    tokens=CommonTokenStream(lexer)#token stream
    parser=Parser(tokens)
    tree=parser.crate() #CST
    print(tree.toStringTree(recog=parser))
    return tree

def ast_build(file_name):
    tree=parse_file(sys.argv[1])
    visitor=ParserVisitor()
    return visitor.visitCrate(tree)

if __name__=="__main__":
    if len(sys.argv)<2:
        print("no file path provided!")
        sys.exit(0)
    crate=ast_build(sys.argv[1])
    pprint(crate)