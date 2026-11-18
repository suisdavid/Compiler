.text
.globl main
main:
    addi sp, sp, -16
    sw ra, 12(sp)
    sw gp, -8(sp)
    addi gp, sp, -8
    call rx_source_main.real_entry
    lw ra, 12(sp)
    addi sp, sp, 16
    li a0, 0
    ret

print_i32.real_entry:
    mv a0, a2
    lw gp, 0(gp)
    tail print_i32

println_i32.real_entry:
    mv a0, a2
    lw gp, 0(gp)
    tail println_i32

get_i32.real_entry:
    lw gp, 0(gp)
    tail get_i32

__rx_alloc.real_entry:
    mv a0, a2
    mv a1, a3
    lw gp, 0(gp)
    tail __rx_alloc
EqualNode.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -96
EqualNode.entry:
    addi x5, x2, 0
    addi x29, x5, 0
    lui x31, 0
    addi x28, x31, 1
    sw x28, 0(x29)
    lui x31, 0
    addi x29, x31, 0
    add x6, x12, x29
    addi x28, x6, 0
    lw x7, 0(x28)
    lui x31, 0
    addi x29, x31, 0
    add x8, x13, x29
    addi x28, x8, 0
    lw x9, 0(x28)
    xor x30, x9, x7
    sltiu x18, x30, 1
    bne x18, x0, EqualNode.block3
    jal x0, EqualNode.block1
EqualNode.block3:
    lui x31, 0
    addi x29, x31, 4
    add x19, x12, x29
    addi x28, x19, 0
    addi x29, x2, 4
    lui x31, 0
    addi x30, x31, 12
    jal x31, internal.memcpy
    lui x31, 0
    addi x29, x31, 4
    add x20, x13, x29
    addi x28, x20, 0
    addi x29, x2, 16
    lui x31, 0
    addi x30, x31, 12
    jal x31, internal.memcpy
    addi x21, x2, 28
    addi x29, x21, 0
    lui x31, 0
    addi x28, x31, 1
    sw x28, 0(x29)
    lw x22, 4(x2)
    lw x23, 16(x2)
    xor x30, x23, x22
    sltiu x24, x30, 1
    bne x24, x0, EqualNode.block4
    jal x0, EqualNode.block7
EqualNode.block4:
    lw x25, 12(x2)
    lw x26, 24(x2)
    addi x27, x2, 32
    addi x29, x27, 0
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    lui x31, 0
    addi x29, x31, 0
    xor x30, x29, x22
    sltiu x28, x30, 1
    sw x28, 36(x2)
    lw x28, 36(x2)
    bne x28, x0, EqualNode.block8
    jal x0, EqualNode.block5
EqualNode.block5:
    addi x28, x27, 0
    lw x30, 0(x28)
    sw x30, 40(x2)
    lw x29, 40(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x25, x31
    sw x28, 44(x2)
    lw x28, 44(x2)
    lw x30, 0(x28)
    sw x30, 48(x2)
    lw x29, 40(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x26, x31
    sw x28, 52(x2)
    lw x28, 52(x2)
    lw x30, 0(x28)
    sw x30, 56(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x13, -28(x2)
    sw x18, -32(x2)
    sw x19, -36(x2)
    sw x20, -40(x2)
    sw x21, -44(x2)
    sw x22, -48(x2)
    sw x23, -52(x2)
    sw x24, -56(x2)
    sw x25, -60(x2)
    sw x26, -64(x2)
    sw x27, -68(x2)
    addi x2, x2, -76
    sw x3, -8(x2)
    lw x28, 124(x2)
    addi x12, x28, 0
    lw x28, 132(x2)
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, EqualNode.real_entry
    addi x2, x2, 76
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x13, -28(x2)
    lw x18, -32(x2)
    lw x19, -36(x2)
    lw x20, -40(x2)
    lw x21, -44(x2)
    lw x22, -48(x2)
    lw x23, -52(x2)
    lw x24, -56(x2)
    lw x25, -60(x2)
    lw x26, -64(x2)
    lw x27, -68(x2)
    addi x28, x10, 0
    sw x28, 60(x2)
    lw x28, 40(x2)
    addi x28, x28, 1
    sw x28, 64(x2)
    addi x29, x27, 0
    lw x30, 64(x2)
    sw x30, 0(x29)
    lw x28, 60(x2)
    bne x28, x0, EqualNode.block6
    jal x0, EqualNode.block7
EqualNode.block6:
    lw x28, 64(x2)
    xor x30, x22, x28
    sltiu x30, x30, 1
    xori x28, x30, 1
    sw x28, 68(x2)
    lw x28, 68(x2)
    bne x28, x0, EqualNode.block5
    jal x0, EqualNode.block8
EqualNode.block7:
    addi x29, x21, 0
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    jal x0, EqualNode.block8
EqualNode.block8:
    addi x28, x21, 0
    lw x30, 0(x28)
    sw x30, 72(x2)
    lw x28, 72(x2)
    bne x28, x0, EqualNode.block2
    jal x0, EqualNode.block1
EqualNode.block1:
    addi x29, x5, 0
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    jal x0, EqualNode.block2
EqualNode.block2:
    addi x28, x5, 0
    lw x30, 0(x28)
    sw x30, 76(x2)
    lw x28, 76(x2)
    addi x10, x28, 0
    jal x0, EqualNode.return
EqualNode.return:
    addi x2, x2, 96
    lw x3, -8(x2)
    lw x1, -4(x2)
    jalr x0, 0(x1)
CloneNode.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -112
CloneNode.entry:
    addi x5, x2, 0
    lui x31, 0
    addi x29, x31, 0
    add x6, x12, x29
    addi x28, x6, 0
    lw x7, 0(x28)
    lui x31, 0
    addi x29, x31, 0
    add x8, x5, x29
    addi x29, x8, 0
    sw x7, 0(x29)
    lui x31, 0
    addi x29, x31, 4
    add x9, x12, x29
    addi x28, x9, 0
    addi x29, x2, 16
    lui x31, 0
    addi x30, x31, 12
    jal x31, internal.memcpy
    lui x31, 0
    addi x29, x31, 4
    add x18, x5, x29
    lw x19, 16(x2)
    lw x20, 20(x2)
    lw x21, 24(x2)
    lui x31, 0
    addi x29, x31, 0
    add x22, x18, x29
    lui x31, 0
    addi x29, x31, 4
    add x23, x18, x29
    addi x29, x22, 0
    sw x19, 0(x29)
    addi x29, x23, 0
    sw x20, 0(x29)
    lui x31, 0
    addi x29, x31, 8
    add x24, x18, x29
    lui x31, 0
    addi x29, x31, 4
    mul x25, x20, x29
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x18, -28(x2)
    sw x19, -32(x2)
    sw x20, -36(x2)
    sw x21, -40(x2)
    sw x22, -44(x2)
    sw x23, -48(x2)
    sw x24, -52(x2)
    sw x25, -56(x2)
    addi x2, x2, -64
    sw x3, -8(x2)
    lw x28, 8(x2)
    addi x12, x28, 0
    lui x31, 0
    addi x28, x31, 4
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, __rx_alloc.real_entry
    addi x2, x2, 64
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x18, -28(x2)
    lw x19, -32(x2)
    lw x20, -36(x2)
    lw x21, -40(x2)
    lw x22, -44(x2)
    lw x23, -48(x2)
    lw x24, -52(x2)
    lw x25, -56(x2)
    addi x26, x10, 0
    addi x29, x24, 0
    sw x26, 0(x29)
    addi x27, x2, 28
    addi x29, x27, 0
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    lui x31, 0
    addi x29, x31, 0
    xor x30, x29, x19
    sltiu x28, x30, 1
    sw x28, 32(x2)
    lw x28, 32(x2)
    bne x28, x0, CloneNode.block2
    jal x0, CloneNode.block1
CloneNode.block1:
    addi x28, x27, 0
    lw x30, 0(x28)
    sw x30, 36(x2)
    lw x29, 36(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x21, x31
    sw x28, 40(x2)
    lw x28, 40(x2)
    lw x30, 0(x28)
    sw x30, 44(x2)
    lw x29, 36(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x26, x31
    sw x28, 48(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x18, -28(x2)
    sw x19, -32(x2)
    sw x20, -36(x2)
    sw x21, -40(x2)
    sw x22, -44(x2)
    sw x23, -48(x2)
    sw x24, -52(x2)
    sw x25, -56(x2)
    sw x26, -60(x2)
    sw x27, -64(x2)
    addi x2, x2, -72
    sw x3, -8(x2)
    lui x31, 0
    addi x28, x31, 16
    addi x12, x28, 0
    lui x31, 0
    addi x28, x31, 4
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, __rx_alloc.real_entry
    addi x2, x2, 72
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x18, -28(x2)
    lw x19, -32(x2)
    lw x20, -36(x2)
    lw x21, -40(x2)
    lw x22, -44(x2)
    lw x23, -48(x2)
    lw x24, -52(x2)
    lw x25, -56(x2)
    lw x26, -60(x2)
    lw x27, -64(x2)
    addi x28, x10, 0
    sw x28, 52(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x18, -28(x2)
    sw x19, -32(x2)
    sw x20, -36(x2)
    sw x21, -40(x2)
    sw x22, -44(x2)
    sw x23, -48(x2)
    sw x24, -52(x2)
    sw x25, -56(x2)
    sw x26, -60(x2)
    sw x27, -64(x2)
    addi x2, x2, -88
    sw x3, -8(x2)
    lw x28, 132(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, CloneNode.real_entry
    addi x2, x2, 88
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x18, -28(x2)
    lw x19, -32(x2)
    lw x20, -36(x2)
    lw x21, -40(x2)
    lw x22, -44(x2)
    lw x23, -48(x2)
    lw x24, -52(x2)
    lw x25, -56(x2)
    lw x26, -60(x2)
    lw x27, -64(x2)
    addi x29, x2, 56
    addi x28, x2, -88
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    lw x29, 52(x2)
    addi x28, x2, 56
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    lw x29, 48(x2)
    lw x30, 52(x2)
    sw x30, 0(x29)
    lw x28, 36(x2)
    addi x28, x28, 1
    sw x28, 72(x2)
    addi x29, x27, 0
    lw x30, 72(x2)
    sw x30, 0(x29)
    lw x28, 72(x2)
    xor x30, x19, x28
    sltiu x30, x30, 1
    xori x28, x30, 1
    sw x28, 76(x2)
    lw x28, 76(x2)
    bne x28, x0, CloneNode.block1
    jal x0, CloneNode.block2
CloneNode.block2:
    addi x28, x5, 0
    addi x29, x2, 80
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x28, x2, 80
    addi x29, x3, 8
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    jal x0, CloneNode.return
CloneNode.return:
    addi x2, x2, 112
    lw x3, -8(x2)
    lw x1, -4(x2)
    jalr x0, 0(x1)
func1.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -368
func1.entry:
    addi x5, x2, 0
    addi x29, x5, 0
    sw x12, 0(x29)
    addi x6, x2, 4
    addi x29, x6, 0
    sw x13, 0(x29)
    addi x28, x6, 0
    lw x7, 0(x28)
    addi x8, x2, 8
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x12, -20(x2)
    sw x13, -24(x2)
    addi x2, x2, -48
    sw x3, -8(x2)
    lw x28, 36(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, func3.real_entry
    addi x2, x2, 48
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x12, -20(x2)
    lw x13, -24(x2)
    addi x29, x2, 24
    addi x28, x2, -48
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x29, x8, 0
    addi x28, x2, 24
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x9, x2, 40
    addi x29, x9, 0
    addi x28, x2, 24
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x28, x5, 0
    lw x18, 0(x28)
    lui x31, 0
    addi x29, x31, 0
    slt x19, x29, x18
    bne x19, x0, func1.block1
    jal x0, func1.block2
func1.block1:
    lui x31, 0
    addi x29, x31, 4
    add x20, x9, x29
    addi x28, x5, 0
    lw x21, 0(x28)
    addi x22, x21, -1
    addi x28, x6, 0
    lw x23, 0(x28)
    lui x31, 0
    addi x29, x31, 2
    mul x24, x23, x29
    addi x25, x2, 56
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x13, -28(x2)
    sw x18, -32(x2)
    sw x19, -36(x2)
    sw x20, -40(x2)
    sw x21, -44(x2)
    sw x22, -48(x2)
    sw x23, -52(x2)
    sw x24, -56(x2)
    sw x25, -60(x2)
    addi x2, x2, -84
    sw x3, -8(x2)
    lw x28, 36(x2)
    addi x12, x28, 0
    lw x28, 28(x2)
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, func1.real_entry
    addi x2, x2, 84
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x13, -28(x2)
    lw x18, -32(x2)
    lw x19, -36(x2)
    lw x20, -40(x2)
    lw x21, -44(x2)
    lw x22, -48(x2)
    lw x23, -52(x2)
    lw x24, -56(x2)
    lw x25, -60(x2)
    addi x29, x2, 72
    addi x28, x2, -84
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x29, x25, 0
    addi x28, x2, 72
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x26, x2, 88
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x13, -28(x2)
    sw x18, -32(x2)
    sw x19, -36(x2)
    sw x20, -40(x2)
    sw x21, -44(x2)
    sw x22, -48(x2)
    sw x23, -52(x2)
    sw x24, -56(x2)
    sw x25, -60(x2)
    sw x26, -64(x2)
    addi x2, x2, -72
    sw x3, -8(x2)
    lui x31, 0
    addi x28, x31, 16
    addi x12, x28, 0
    lui x31, 0
    addi x28, x31, 4
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, __rx_alloc.real_entry
    addi x2, x2, 72
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x13, -28(x2)
    lw x18, -32(x2)
    lw x19, -36(x2)
    lw x20, -40(x2)
    lw x21, -44(x2)
    lw x22, -48(x2)
    lw x23, -52(x2)
    lw x24, -56(x2)
    lw x25, -60(x2)
    lw x26, -64(x2)
    addi x27, x10, 0
    addi x29, x27, 0
    addi x28, x2, 72
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x29, x26, 0
    sw x27, 0(x29)
    lui x31, 0
    addi x29, x31, 0
    add x28, x20, x29
    sw x28, 92(x2)
    lw x28, 92(x2)
    lw x30, 0(x28)
    sw x30, 96(x2)
    lw x28, 96(x2)
    addi x28, x28, 1
    sw x28, 100(x2)
    lw x29, 92(x2)
    lw x30, 100(x2)
    sw x30, 0(x29)
    lui x31, 0
    addi x29, x31, 4
    add x28, x20, x29
    sw x28, 104(x2)
    lw x28, 104(x2)
    lw x30, 0(x28)
    sw x30, 108(x2)
    lui x31, 0
    addi x29, x31, 8
    add x28, x20, x29
    sw x28, 112(x2)
    lw x28, 112(x2)
    lw x30, 0(x28)
    sw x30, 116(x2)
    lw x28, 96(x2)
    lw x29, 108(x2)
    xor x30, x29, x28
    sltiu x28, x30, 1
    sw x28, 120(x2)
    lw x28, 120(x2)
    bne x28, x0, func1.block3
    jal x0, func1.block4
func1.block3:
    lw x28, 108(x2)
    lw x29, 108(x2)
    add x28, x28, x29
    sw x28, 124(x2)
    lw x28, 124(x2)
    lui x31, 0
    addi x29, x31, 4
    mul x28, x28, x29
    sw x28, 128(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x13, -28(x2)
    sw x18, -32(x2)
    sw x19, -36(x2)
    sw x20, -40(x2)
    sw x21, -44(x2)
    sw x22, -48(x2)
    sw x23, -52(x2)
    sw x24, -56(x2)
    sw x25, -60(x2)
    sw x26, -64(x2)
    sw x27, -68(x2)
    addi x2, x2, -76
    sw x3, -8(x2)
    lw x28, 204(x2)
    addi x12, x28, 0
    lui x31, 0
    addi x28, x31, 4
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, __rx_alloc.real_entry
    addi x2, x2, 76
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x13, -28(x2)
    lw x18, -32(x2)
    lw x19, -36(x2)
    lw x20, -40(x2)
    lw x21, -44(x2)
    lw x22, -48(x2)
    lw x23, -52(x2)
    lw x24, -56(x2)
    lw x25, -60(x2)
    lw x26, -64(x2)
    lw x27, -68(x2)
    addi x28, x10, 0
    sw x28, 132(x2)
    lw x29, 112(x2)
    lw x30, 132(x2)
    sw x30, 0(x29)
    lw x29, 104(x2)
    lw x30, 124(x2)
    sw x30, 0(x29)
    addi x28, x2, 136
    sw x28, 140(x2)
    lw x29, 140(x2)
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    jal x0, func1.block5
func1.block5:
    lw x28, 140(x2)
    lw x30, 0(x28)
    sw x30, 144(x2)
    lw x28, 116(x2)
    lw x29, 144(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 148(x2)
    lw x28, 148(x2)
    lw x30, 0(x28)
    sw x30, 152(x2)
    lw x28, 132(x2)
    lw x29, 144(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 156(x2)
    lw x29, 156(x2)
    lw x30, 152(x2)
    sw x30, 0(x29)
    lw x28, 144(x2)
    addi x28, x28, 1
    sw x28, 160(x2)
    lw x29, 140(x2)
    lw x30, 160(x2)
    sw x30, 0(x29)
    lw x28, 160(x2)
    lw x29, 96(x2)
    xor x30, x29, x28
    sltiu x30, x30, 1
    xori x28, x30, 1
    sw x28, 164(x2)
    lw x28, 164(x2)
    bne x28, x0, func1.block5
    jal x0, func1.block4
func1.block4:
    lw x28, 112(x2)
    lw x30, 0(x28)
    sw x30, 168(x2)
    lw x28, 168(x2)
    lw x29, 96(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 172(x2)
    lw x29, 172(x2)
    sw x27, 0(x29)
    lui x31, 0
    addi x29, x31, 4
    add x28, x9, x29
    sw x28, 176(x2)
    addi x28, x5, 0
    lw x30, 0(x28)
    sw x30, 180(x2)
    lw x28, 180(x2)
    addi x28, x28, -1
    sw x28, 184(x2)
    addi x28, x6, 0
    lw x30, 0(x28)
    sw x30, 188(x2)
    lw x28, 188(x2)
    lui x31, 0
    addi x29, x31, 2
    mul x28, x28, x29
    sw x28, 192(x2)
    lw x28, 192(x2)
    addi x28, x28, 1
    sw x28, 196(x2)
    addi x28, x2, 200
    sw x28, 216(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x13, -28(x2)
    sw x18, -32(x2)
    sw x19, -36(x2)
    sw x20, -40(x2)
    sw x21, -44(x2)
    sw x22, -48(x2)
    sw x23, -52(x2)
    sw x24, -56(x2)
    sw x25, -60(x2)
    sw x26, -64(x2)
    sw x27, -68(x2)
    addi x2, x2, -92
    sw x3, -8(x2)
    lw x28, 276(x2)
    addi x12, x28, 0
    lw x28, 288(x2)
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, func1.real_entry
    addi x2, x2, 92
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x13, -28(x2)
    lw x18, -32(x2)
    lw x19, -36(x2)
    lw x20, -40(x2)
    lw x21, -44(x2)
    lw x22, -48(x2)
    lw x23, -52(x2)
    lw x24, -56(x2)
    lw x25, -60(x2)
    lw x26, -64(x2)
    lw x27, -68(x2)
    addi x29, x2, 220
    addi x28, x2, -92
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    lw x29, 216(x2)
    addi x28, x2, 220
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x28, x2, 236
    sw x28, 240(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x13, -28(x2)
    sw x18, -32(x2)
    sw x19, -36(x2)
    sw x20, -40(x2)
    sw x21, -44(x2)
    sw x22, -48(x2)
    sw x23, -52(x2)
    sw x24, -56(x2)
    sw x25, -60(x2)
    sw x26, -64(x2)
    sw x27, -68(x2)
    addi x2, x2, -76
    sw x3, -8(x2)
    lui x31, 0
    addi x28, x31, 16
    addi x12, x28, 0
    lui x31, 0
    addi x28, x31, 4
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, __rx_alloc.real_entry
    addi x2, x2, 76
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x13, -28(x2)
    lw x18, -32(x2)
    lw x19, -36(x2)
    lw x20, -40(x2)
    lw x21, -44(x2)
    lw x22, -48(x2)
    lw x23, -52(x2)
    lw x24, -56(x2)
    lw x25, -60(x2)
    lw x26, -64(x2)
    lw x27, -68(x2)
    addi x28, x10, 0
    sw x28, 244(x2)
    lw x29, 244(x2)
    addi x28, x2, 220
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    lw x29, 240(x2)
    lw x30, 244(x2)
    sw x30, 0(x29)
    lw x28, 176(x2)
    lui x31, 0
    addi x29, x31, 0
    add x28, x28, x29
    sw x28, 248(x2)
    lw x28, 248(x2)
    lw x30, 0(x28)
    sw x30, 252(x2)
    lw x28, 252(x2)
    addi x28, x28, 1
    sw x28, 256(x2)
    lw x29, 248(x2)
    lw x30, 256(x2)
    sw x30, 0(x29)
    lw x28, 176(x2)
    lui x31, 0
    addi x29, x31, 4
    add x28, x28, x29
    sw x28, 260(x2)
    lw x28, 260(x2)
    lw x30, 0(x28)
    sw x30, 264(x2)
    lw x28, 176(x2)
    lui x31, 0
    addi x29, x31, 8
    add x28, x28, x29
    sw x28, 268(x2)
    lw x28, 268(x2)
    lw x30, 0(x28)
    sw x30, 272(x2)
    lw x28, 252(x2)
    lw x29, 264(x2)
    xor x30, x29, x28
    sltiu x28, x30, 1
    sw x28, 276(x2)
    lw x28, 276(x2)
    bne x28, x0, func1.block6
    jal x0, func1.block7
func1.block6:
    lw x28, 264(x2)
    lw x29, 264(x2)
    add x28, x28, x29
    sw x28, 280(x2)
    lw x28, 280(x2)
    lui x31, 0
    addi x29, x31, 4
    mul x28, x28, x29
    sw x28, 284(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x13, -28(x2)
    sw x18, -32(x2)
    sw x19, -36(x2)
    sw x20, -40(x2)
    sw x21, -44(x2)
    sw x22, -48(x2)
    sw x23, -52(x2)
    sw x24, -56(x2)
    sw x25, -60(x2)
    sw x26, -64(x2)
    sw x27, -68(x2)
    addi x2, x2, -76
    sw x3, -8(x2)
    lw x28, 360(x2)
    addi x12, x28, 0
    lui x31, 0
    addi x28, x31, 4
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, __rx_alloc.real_entry
    addi x2, x2, 76
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x13, -28(x2)
    lw x18, -32(x2)
    lw x19, -36(x2)
    lw x20, -40(x2)
    lw x21, -44(x2)
    lw x22, -48(x2)
    lw x23, -52(x2)
    lw x24, -56(x2)
    lw x25, -60(x2)
    lw x26, -64(x2)
    lw x27, -68(x2)
    addi x28, x10, 0
    sw x28, 288(x2)
    lw x29, 268(x2)
    lw x30, 288(x2)
    sw x30, 0(x29)
    lw x29, 260(x2)
    lw x30, 280(x2)
    sw x30, 0(x29)
    addi x28, x2, 292
    sw x28, 296(x2)
    lw x29, 296(x2)
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    jal x0, func1.block8
func1.block8:
    lw x28, 296(x2)
    lw x30, 0(x28)
    sw x30, 300(x2)
    lw x28, 272(x2)
    lw x29, 300(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 304(x2)
    lw x28, 304(x2)
    lw x30, 0(x28)
    sw x30, 308(x2)
    lw x28, 288(x2)
    lw x29, 300(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 312(x2)
    lw x29, 312(x2)
    lw x30, 308(x2)
    sw x30, 0(x29)
    lw x28, 300(x2)
    addi x28, x28, 1
    sw x28, 316(x2)
    lw x29, 296(x2)
    lw x30, 316(x2)
    sw x30, 0(x29)
    lw x28, 316(x2)
    lw x29, 252(x2)
    xor x30, x29, x28
    sltiu x30, x30, 1
    xori x28, x30, 1
    sw x28, 320(x2)
    lw x28, 320(x2)
    bne x28, x0, func1.block8
    jal x0, func1.block7
func1.block7:
    lw x28, 268(x2)
    lw x30, 0(x28)
    sw x30, 324(x2)
    lw x28, 324(x2)
    lw x29, 252(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 328(x2)
    lw x29, 328(x2)
    lw x30, 244(x2)
    sw x30, 0(x29)
    jal x0, func1.block2
func1.block2:
    addi x28, x9, 0
    addi x29, x2, 332
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x28, x2, 332
    addi x29, x3, 8
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    jal x0, func1.return
func1.return:
    addi x2, x2, 368
    lw x3, -8(x2)
    lw x1, -4(x2)
    jalr x0, 0(x1)
rx_source_main.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -288
rx_source_main.entry:
    addi x5, x2, 0
    sw x5, -4(x2)
    addi x2, x2, -12
    sw x3, -8(x2)
    addi x3, x2, -8
    jal x1, get_i32.real_entry
    addi x2, x2, 12
    lw x5, -4(x2)
    addi x6, x10, 0
    addi x29, x5, 0
    sw x6, 0(x29)
    addi x7, x2, 4
    addi x29, x7, 0
    sw x6, 0(x29)
    addi x8, x2, 8
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    addi x2, x2, -24
    sw x3, -8(x2)
    addi x3, x2, -8
    jal x1, get_i32.real_entry
    addi x2, x2, 24
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    addi x9, x10, 0
    addi x29, x8, 0
    sw x9, 0(x29)
    addi x18, x2, 12
    addi x29, x18, 0
    sw x9, 0(x29)
    addi x28, x7, 0
    lw x19, 0(x28)
    addi x28, x18, 0
    lw x20, 0(x28)
    addi x21, x2, 16
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    addi x2, x2, -60
    sw x3, -8(x2)
    lw x28, 32(x2)
    addi x12, x28, 0
    lw x28, 28(x2)
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, func1.real_entry
    addi x2, x2, 60
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    addi x29, x2, 32
    addi x28, x2, -60
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x29, x21, 0
    addi x28, x2, 32
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x22, x2, 48
    addi x29, x22, 0
    addi x28, x2, 32
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x23, x2, 64
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    addi x2, x2, -68
    sw x3, -8(x2)
    lw x28, 28(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, CloneNode.real_entry
    addi x2, x2, 68
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    addi x29, x2, 80
    addi x28, x2, -68
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x29, x23, 0
    addi x28, x2, 80
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x28, x23, 0
    addi x29, x2, 96
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x24, x2, 112
    addi x29, x24, 0
    addi x28, x2, 96
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    addi x2, x2, -56
    sw x3, -8(x2)
    lw x28, 16(x2)
    addi x12, x28, 0
    lw x28, 8(x2)
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, EqualNode.real_entry
    addi x2, x2, 56
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    addi x25, x10, 0
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    addi x2, x2, -60
    sw x3, -8(x2)
    lw x28, 8(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, println_i32.real_entry
    addi x2, x2, 60
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    addi x2, x2, -60
    sw x3, -8(x2)
    lw x28, 12(x2)
    addi x12, x28, 0
    lui x31, 0
    addi x28, x31, 1
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, func5.real_entry
    addi x2, x2, 60
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    addi x26, x2, 128
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    sw x26, -56(x2)
    addi x2, x2, -64
    sw x3, -8(x2)
    lw x28, 24(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, func4.real_entry
    addi x2, x2, 64
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    lw x26, -56(x2)
    addi x27, x10, 0
    addi x29, x26, 0
    sw x27, 0(x29)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    sw x26, -56(x2)
    sw x27, -60(x2)
    addi x2, x2, -68
    sw x3, -8(x2)
    lw x28, 8(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, println_i32.real_entry
    addi x2, x2, 68
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    lw x26, -56(x2)
    lw x27, -60(x2)
    addi x28, x2, 132
    sw x28, 136(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    sw x26, -56(x2)
    sw x27, -60(x2)
    addi x2, x2, -68
    sw x3, -8(x2)
    lw x28, 20(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, func4.real_entry
    addi x2, x2, 68
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    lw x26, -56(x2)
    lw x27, -60(x2)
    addi x28, x10, 0
    sw x28, 140(x2)
    lw x29, 136(x2)
    lw x30, 140(x2)
    sw x30, 0(x29)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    sw x26, -56(x2)
    sw x27, -60(x2)
    addi x2, x2, -68
    sw x3, -8(x2)
    lw x28, 208(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, println_i32.real_entry
    addi x2, x2, 68
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    lw x26, -56(x2)
    lw x27, -60(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    sw x26, -56(x2)
    sw x27, -60(x2)
    addi x2, x2, -68
    sw x3, -8(x2)
    lw x28, 28(x2)
    addi x12, x28, 0
    lw x28, 20(x2)
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, EqualNode.real_entry
    addi x2, x2, 68
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    lw x26, -56(x2)
    lw x27, -60(x2)
    addi x28, x10, 0
    sw x28, 144(x2)
    lw x28, 144(x2)
    xori x28, x28, 1
    sw x28, 148(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    sw x26, -56(x2)
    sw x27, -60(x2)
    addi x2, x2, -68
    sw x3, -8(x2)
    lw x28, 216(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, println_i32.real_entry
    addi x2, x2, 68
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    lw x26, -56(x2)
    lw x27, -60(x2)
    lui x31, 0
    addi x29, x31, 4
    add x28, x24, x29
    sw x28, 152(x2)
    lw x28, 152(x2)
    lui x31, 0
    addi x29, x31, 0
    add x28, x28, x29
    sw x28, 156(x2)
    lw x28, 156(x2)
    lw x30, 0(x28)
    sw x30, 160(x2)
    lw x28, 160(x2)
    lui x31, 0
    addi x29, x31, 0
    sltu x28, x29, x28
    sw x28, 164(x2)
    lw x28, 164(x2)
    bne x28, x0, rx_source_main.block1
    jal x0, rx_source_main.block2
rx_source_main.block1:
    lui x31, 0
    addi x29, x31, 4
    add x28, x24, x29
    sw x28, 168(x2)
    lw x28, 168(x2)
    lui x31, 0
    addi x29, x31, 0
    add x28, x28, x29
    sw x28, 172(x2)
    lw x28, 172(x2)
    lw x30, 0(x28)
    sw x30, 176(x2)
    lw x28, 176(x2)
    addi x28, x28, -1
    sw x28, 180(x2)
    lw x29, 172(x2)
    lw x30, 180(x2)
    sw x30, 0(x29)
    lw x28, 168(x2)
    lui x31, 0
    addi x29, x31, 8
    add x28, x28, x29
    sw x28, 184(x2)
    lw x28, 184(x2)
    lw x30, 0(x28)
    sw x30, 188(x2)
    lw x28, 188(x2)
    lui x31, 0
    addi x29, x31, 0
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 192(x2)
    lw x28, 192(x2)
    lw x30, 0(x28)
    sw x30, 196(x2)
    lw x28, 180(x2)
    lui x31, 0
    addi x29, x31, 0
    xor x30, x29, x28
    sltiu x28, x30, 1
    sw x28, 200(x2)
    lw x28, 200(x2)
    bne x28, x0, rx_source_main.block6
    jal x0, rx_source_main.block3
rx_source_main.block3:
    addi x28, x2, 204
    sw x28, 208(x2)
    lw x29, 208(x2)
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    jal x0, rx_source_main.block4
rx_source_main.block4:
    lw x28, 208(x2)
    lw x30, 0(x28)
    sw x30, 212(x2)
    lw x28, 212(x2)
    addi x28, x28, 1
    sw x28, 216(x2)
    lw x29, 208(x2)
    lw x30, 216(x2)
    sw x30, 0(x29)
    lw x28, 188(x2)
    lw x29, 216(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 220(x2)
    lw x28, 220(x2)
    lw x30, 0(x28)
    sw x30, 224(x2)
    lw x28, 188(x2)
    lw x29, 212(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 228(x2)
    lw x29, 228(x2)
    lw x30, 224(x2)
    sw x30, 0(x29)
    lw x28, 216(x2)
    lw x29, 180(x2)
    xor x30, x29, x28
    sltiu x28, x30, 1
    sw x28, 232(x2)
    lw x28, 232(x2)
    bne x28, x0, rx_source_main.block6
    jal x0, rx_source_main.block4
rx_source_main.block6:
    addi x28, x2, 236
    sw x28, 240(x2)
    lw x29, 240(x2)
    lw x30, 196(x2)
    sw x30, 0(x29)
    addi x28, x2, 244
    sw x28, 248(x2)
    lw x29, 248(x2)
    lw x30, 196(x2)
    sw x30, 0(x29)
    lw x28, 248(x2)
    lw x30, 0(x28)
    sw x30, 252(x2)
    addi x28, x2, 256
    sw x28, 260(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    sw x26, -56(x2)
    sw x27, -60(x2)
    addi x2, x2, -68
    sw x3, -8(x2)
    lw x28, 320(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, func4.real_entry
    addi x2, x2, 68
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    lw x26, -56(x2)
    lw x27, -60(x2)
    addi x28, x10, 0
    sw x28, 264(x2)
    lw x29, 260(x2)
    lw x30, 264(x2)
    sw x30, 0(x29)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    sw x26, -56(x2)
    sw x27, -60(x2)
    addi x2, x2, -68
    sw x3, -8(x2)
    lw x28, 332(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, println_i32.real_entry
    addi x2, x2, 68
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    lw x26, -56(x2)
    lw x27, -60(x2)
    addi x28, x2, 268
    sw x28, 272(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    sw x26, -56(x2)
    sw x27, -60(x2)
    addi x2, x2, -68
    sw x3, -8(x2)
    lw x28, 20(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, func4.real_entry
    addi x2, x2, 68
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    lw x26, -56(x2)
    lw x27, -60(x2)
    addi x28, x10, 0
    sw x28, 276(x2)
    lw x29, 272(x2)
    lw x30, 276(x2)
    sw x30, 0(x29)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    sw x21, -36(x2)
    sw x22, -40(x2)
    sw x23, -44(x2)
    sw x24, -48(x2)
    sw x25, -52(x2)
    sw x26, -56(x2)
    sw x27, -60(x2)
    addi x2, x2, -68
    sw x3, -8(x2)
    lw x28, 344(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, println_i32.real_entry
    addi x2, x2, 68
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    lw x21, -36(x2)
    lw x22, -40(x2)
    lw x23, -44(x2)
    lw x24, -48(x2)
    lw x25, -52(x2)
    lw x26, -56(x2)
    lw x27, -60(x2)
    jal x0, rx_source_main.block2
rx_source_main.block2:
    jal x0, rx_source_main.return
rx_source_main.return:
    addi x2, x2, 288
    lw x3, -8(x2)
    lw x1, -4(x2)
    jalr x0, 0(x1)
func3.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -80
func3.entry:
    addi x5, x2, 0
    addi x29, x5, 0
    sw x12, 0(x29)
    addi x28, x5, 0
    lw x6, 0(x28)
    addi x7, x2, 4
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x12, -16(x2)
    addi x2, x2, -24
    sw x3, -8(x2)
    lui x31, 0
    addi x28, x31, 8
    addi x12, x28, 0
    lui x31, 0
    addi x28, x31, 4
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, __rx_alloc.real_entry
    addi x2, x2, 24
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x12, -16(x2)
    addi x8, x10, 0
    lui x31, 0
    addi x29, x31, 0
    add x9, x7, x29
    addi x29, x9, 0
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    lui x31, 0
    addi x29, x31, 4
    add x18, x7, x29
    addi x29, x18, 0
    lui x31, 0
    addi x28, x31, 2
    sw x28, 0(x29)
    lui x31, 0
    addi x29, x31, 8
    add x19, x7, x29
    addi x29, x19, 0
    sw x8, 0(x29)
    addi x28, x7, 0
    addi x29, x2, 16
    lui x31, 0
    addi x30, x31, 12
    jal x31, internal.memcpy
    addi x20, x2, 28
    lui x31, 0
    addi x29, x31, 0
    add x21, x20, x29
    addi x29, x21, 0
    sw x6, 0(x29)
    lui x31, 0
    addi x29, x31, 4
    add x22, x20, x29
    addi x29, x22, 0
    addi x28, x2, 16
    lui x31, 0
    addi x30, x31, 12
    jal x31, internal.memcpy
    addi x28, x20, 0
    addi x29, x2, 44
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    addi x28, x2, 44
    addi x29, x3, 8
    lui x31, 0
    addi x30, x31, 16
    jal x31, internal.memcpy
    jal x0, func3.return
func3.return:
    addi x2, x2, 80
    lw x3, -8(x2)
    lw x1, -4(x2)
    jalr x0, 0(x1)
func4.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -80
func4.entry:
    addi x5, x2, 0
    addi x29, x5, 0
    sw x12, 0(x29)
    addi x28, x5, 0
    lw x6, 0(x28)
    lui x31, 0
    addi x29, x31, 0
    add x7, x6, x29
    addi x28, x7, 0
    lw x8, 0(x28)
    addi x9, x2, 4
    addi x29, x9, 0
    sw x8, 0(x29)
    addi x18, x2, 8
    addi x29, x18, 0
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    addi x19, x2, 12
    jal x0, func4.block1
func4.block1:
    addi x28, x5, 0
    lw x20, 0(x28)
    lui x31, 0
    addi x29, x31, 4
    add x21, x20, x29
    lui x31, 0
    addi x29, x31, 0
    add x22, x21, x29
    addi x28, x22, 0
    lw x23, 0(x28)
    addi x28, x18, 0
    lw x24, 0(x28)
    sltu x25, x24, x23
    bne x25, x0, func4.block2
    jal x0, func4.block3
func4.block2:
    addi x28, x5, 0
    lw x26, 0(x28)
    lui x31, 0
    addi x29, x31, 4
    add x27, x26, x29
    addi x28, x27, 0
    addi x29, x2, 12
    lui x31, 0
    addi x30, x31, 12
    jal x31, internal.memcpy
    addi x28, x18, 0
    lw x30, 0(x28)
    sw x30, 24(x2)
    addi x28, x2, 20
    lw x30, 0(x28)
    sw x30, 28(x2)
    lw x28, 28(x2)
    lw x29, 24(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 32(x2)
    lw x28, 32(x2)
    lw x30, 0(x28)
    sw x30, 36(x2)
    addi x28, x2, 40
    sw x28, 44(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x18, -28(x2)
    sw x19, -32(x2)
    sw x20, -36(x2)
    sw x21, -40(x2)
    sw x22, -44(x2)
    sw x23, -48(x2)
    sw x24, -52(x2)
    sw x25, -56(x2)
    sw x26, -60(x2)
    sw x27, -64(x2)
    addi x2, x2, -72
    sw x3, -8(x2)
    lw x28, 108(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, func4.real_entry
    addi x2, x2, 72
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x18, -28(x2)
    lw x19, -32(x2)
    lw x20, -36(x2)
    lw x21, -40(x2)
    lw x22, -44(x2)
    lw x23, -48(x2)
    lw x24, -52(x2)
    lw x25, -56(x2)
    lw x26, -60(x2)
    lw x27, -64(x2)
    addi x28, x10, 0
    sw x28, 48(x2)
    lw x29, 44(x2)
    lw x30, 48(x2)
    sw x30, 0(x29)
    addi x28, x9, 0
    lw x30, 0(x28)
    sw x30, 52(x2)
    lw x28, 52(x2)
    lw x29, 48(x2)
    add x28, x28, x29
    sw x28, 56(x2)
    addi x29, x9, 0
    lw x30, 56(x2)
    sw x30, 0(x29)
    addi x28, x18, 0
    lw x30, 0(x28)
    sw x30, 60(x2)
    lw x28, 60(x2)
    addi x28, x28, 1
    sw x28, 64(x2)
    addi x29, x18, 0
    lw x30, 64(x2)
    sw x30, 0(x29)
    jal x0, func4.block1
func4.block3:
    addi x28, x9, 0
    lw x30, 0(x28)
    sw x30, 68(x2)
    lw x28, 68(x2)
    addi x10, x28, 0
    jal x0, func4.return
func4.return:
    addi x2, x2, 80
    lw x3, -8(x2)
    lw x1, -4(x2)
    jalr x0, 0(x1)
func5.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -80
func5.entry:
    addi x5, x2, 0
    addi x29, x5, 0
    sw x12, 0(x29)
    addi x6, x2, 4
    addi x29, x6, 0
    sw x13, 0(x29)
    addi x28, x6, 0
    lw x7, 0(x28)
    addi x28, x5, 0
    lw x8, 0(x28)
    lui x31, 0
    addi x29, x31, 0
    add x9, x8, x29
    addi x28, x9, 0
    lw x18, 0(x28)
    add x19, x18, x7
    addi x29, x9, 0
    sw x19, 0(x29)
    addi x20, x2, 8
    addi x29, x20, 0
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    addi x21, x2, 12
    jal x0, func5.block1
func5.block1:
    addi x28, x5, 0
    lw x22, 0(x28)
    lui x31, 0
    addi x29, x31, 4
    add x23, x22, x29
    lui x31, 0
    addi x29, x31, 0
    add x24, x23, x29
    addi x28, x24, 0
    lw x25, 0(x28)
    addi x28, x20, 0
    lw x26, 0(x28)
    sltu x27, x26, x25
    bne x27, x0, func5.block2
    jal x0, func5.block3
func5.block2:
    addi x28, x5, 0
    lw x30, 0(x28)
    sw x30, 12(x2)
    lw x28, 12(x2)
    lui x31, 0
    addi x29, x31, 4
    add x28, x28, x29
    sw x28, 16(x2)
    lw x28, 16(x2)
    addi x29, x2, 20
    lui x31, 0
    addi x30, x31, 12
    jal x31, internal.memcpy
    addi x28, x20, 0
    lw x30, 0(x28)
    sw x30, 32(x2)
    addi x28, x2, 28
    lw x30, 0(x28)
    sw x30, 36(x2)
    lw x28, 36(x2)
    lw x29, 32(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 40(x2)
    lw x28, 40(x2)
    lw x30, 0(x28)
    sw x30, 44(x2)
    addi x28, x6, 0
    lw x30, 0(x28)
    sw x30, 48(x2)
    lw x28, 48(x2)
    addi x28, x28, 1
    sw x28, 52(x2)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x12, -24(x2)
    sw x13, -28(x2)
    sw x18, -32(x2)
    sw x19, -36(x2)
    sw x20, -40(x2)
    sw x21, -44(x2)
    sw x22, -48(x2)
    sw x23, -52(x2)
    sw x24, -56(x2)
    sw x25, -60(x2)
    sw x26, -64(x2)
    sw x27, -68(x2)
    addi x2, x2, -76
    sw x3, -8(x2)
    lw x28, 120(x2)
    addi x12, x28, 0
    lw x28, 128(x2)
    addi x13, x28, 0
    addi x3, x2, -8
    jal x1, func5.real_entry
    addi x2, x2, 76
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x12, -24(x2)
    lw x13, -28(x2)
    lw x18, -32(x2)
    lw x19, -36(x2)
    lw x20, -40(x2)
    lw x21, -44(x2)
    lw x22, -48(x2)
    lw x23, -52(x2)
    lw x24, -56(x2)
    lw x25, -60(x2)
    lw x26, -64(x2)
    lw x27, -68(x2)
    addi x28, x20, 0
    lw x30, 0(x28)
    sw x30, 56(x2)
    lw x28, 56(x2)
    addi x28, x28, 1
    sw x28, 60(x2)
    addi x29, x20, 0
    lw x30, 60(x2)
    sw x30, 0(x29)
    jal x0, func5.block1
func5.block3:
    jal x0, func5.return
func5.return:
    addi x2, x2, 80
    lw x3, -8(x2)
    lw x1, -4(x2)
    jalr x0, 0(x1)
internal.memcpy:
    lw a1, 0(t3)
    sw a1, 0(t4)
    addi t3, t3, 4
    addi t4, t4, 4
    addi t5, t5, -4
    beq t5, x0, internal.memcpy.ret
    jal x0, internal.memcpy
internal.memcpy.ret:
    jalr x0, 0(t6)
