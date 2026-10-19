#!/usr/bin/env bash
set -euo pipefail

# 固定在脚本所在目录运行。
cd "$(dirname "$0")"

LLVM_BIN="$(brew --prefix llvm@22)/bin"

# RX → LLVM IR
python3 main.py sample.rx hello.ll
"$LLVM_BIN/opt" -passes=verify -disable-output hello.ll

# LLVM IR → RV32IM 汇编
"$LLVM_BIN/clang" \
    --target=riscv32-unknown-elf -march=rv32im -mabi=ilp32 \
    -S -O0 -g0 -fno-addrsig -Wno-override-module \
    hello.ll -o hello.s

# C 运行时 → RV32IM 汇编
"$LLVM_BIN/clang" \
    --target=riscv32-unknown-elf -march=rv32im -mabi=ilp32 \
    -S -O2 -g0 -ffreestanding -fno-addrsig -Wno-override-module  \
    runtime-example.c -o runtime.s

python3 scripts/strip_asm_debug.py hello.s
python3 scripts/strip_asm_debug.py runtime.s

xmake run -P vendor/REIMU -w "$PWD" reimu \
    --memory=256M --stack=1M  --silent\
    -f hello.s,runtime.s \
    -o hello.out -p hello.profile

cat hello.out