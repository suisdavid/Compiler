PYTHON := $(CURDIR)/.venv/bin/python3

CLANG ?= clang-22
# 测试开始前，将公共运行时编译为汇编。
BUILD = "$(CLANG)" \
    --target=riscv32-unknown-none-elf -march=rv32im -mabi=ilp32 \
    -S -O2 -g0 -ffreestanding -fno-addrsig \
    "$(CURDIR)/runtime-example.c" -o {runtime} && \
    "$(PYTHON)" scripts/strip_asm_debug.py {runtime}

# 只进行语义检查。
SEMANTIC = "$(PYTHON)" main.py {source}

# 生成测试器指定位置的 LLVM IR。
IR = "$(PYTHON)" main.py {source} {output}

# 尚未实现直接输出汇编，可以暂时留空。
CODEGEN =

# 测试器传给 RUN 的 {output} 已经是汇编文件。
RUN = xmake run -P "$(CURDIR)/vendor/REIMU" -w "$(CURDIR)" reimu \
    --memory=256M --stack=1M \
    -f {output},{runtime} \
    -o {stdout} -p {profile} 1>&2