from __future__ import annotations
from dataclasses import dataclass,field
from enum import Enum

class Opcode(Enum):
    ADD = 1
    SUB = 2 
    AND = 3
    OR = 4
    XOR = 5
    SLL = 6
    SRL = 7
    SRA = 8
    SLT = 9
    SLTU = 10
    ADDI = 11
    ANDI = 12
    ORI = 13
    XORI = 14
    SLLI =15
    SRLI = 16
    SRAI = 17
    SLTI = 18
    SLTIU = 19
    LW = 24
    SW = 25
    BNE = 26
    JAL = 27
    JALR = 28
    MUL = 29
    DIV = 30
    DIVU = 31
    REM = 32
    REMU = 33
    LUI = 34
    BLOCK = 35


@dataclass
class FunctionDescriptions:
    identifier: str
    param_types: list[str] #type used in ir
    param_num: int
    ret_size: int
    block: list[str]#split by '\n'
    phiMap: dict[str,str]=field(default_factory=dict)

@dataclass
class Position:
    reg: bool #whether stored in register
    id: int #register id/ stack offset,signed 32
    const: bool=False #whether is constant


@dataclass
class Op:
    opcode: int
    rd: int
    r1: int
    r2: int=0
    label: str=None #reserved for branch op

@dataclass
class Function:
    identifier: str
    ops: list[Op]
