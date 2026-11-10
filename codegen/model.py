from __future__ import annotations
from dataclasses import dataclass,field
from enum import Enum

class Opcode(Enum):
    ADD: 1
    SUB: 2 
    AND: 3
    OR: 4
    XOR: 5
    SLL: 6
    SRL: 7
    SRA: 8
    SLT: 9
    SLTU: 10
    ADDI: 11
    ANDI: 12
    ORI: 13
    XORI: 14
    SLLI: 15
    SRLI: 16
    SRAI: 17
    SLTI: 18
    SLTIU: 19
    LB: 20
    LBU: 21
    LH: 22
    LHU: 23
    LW: 24
    SB: 25
    SH: 26
    SW: 27
    BEQ: 28
    BGE: 29
    BGEU: 30
    BLT: 31
    BLTU: 32
    BNE: 33
    JAL: 34
    JALR: 35
    MUL: 36
    DIV: 37
    DIVU: 38
    REM: 39
    REMU: 40

@dataclass
class FunctionDescriptions:
    identifier: str
    param_types: list[str] #type used in ir
    param_num: int
    block: list[str]#split by '\n'

@dataclass
class Position:
    reg: bool #whether stored in register
    id: int #register id/ stack offset


@dataclass
class Op:
    opcode: Opcode
    rd: int
    r1: int
    r2: int