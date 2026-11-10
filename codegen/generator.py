from __future__ import annotations
from dataclasses import dataclass,field
from codegen.model import *
from utils.util import util

class Generator:
    class Allocator: #for register allocating
        def __init__(self):
            self.regNum=19
            self.regIds=['t0','t1','t2','t3','t4','t5','t6','s0','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11']   
            self.in_use=[0]*self.regNum
            self.stk_offset=0
            self.varpos={}#varName to position(Position)
            
        def allocate(self,varName:str,varSize:int)->Position:
            pos=self.varpos.get(varName)
            if pos:
                return pos
            else:
                if 0 in self.in_use and varSize<=4:
                    idx=self.in_use.index(0)
                    self.in_use[idx]=1
                    self.varpos[varName]=Position(reg=True,id=idx)
                else:
                    self.stk_offset+=varSize
                    self.varpos[varName]=Position(reg=False,id=self.stk_offset-varSize)
                return self.varpos[varName]
            
        def free(self,varName:str):
            pos=self.varpos.get(varName)
            if pos and pos.reg:
                self.in_use[pos.id]=0

    def __init__(self,functions:list[FunctionDescriptions],output_path:str):
        self.functions=functions
        self.output=output_path
        self.varSize={}#varname to Size
        self.varType={}#varname to Type(IR-based)

    def Generate(self):
        for function in self.functions:
            self.allocator=self.Allocator()
            self.Parse(allocator)
