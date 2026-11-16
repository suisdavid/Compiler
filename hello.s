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
EqualS.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -80
EqualS.entry:
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
    bne x18, x0, EqualS.block3
    jal x0, EqualS.block1
EqualS.block3:
    lui x31, 0
    addi x29, x31, 4
    add x19, x12, x29
    addi x28, x19, 0
    lw x20, 0(x28)
    lui x31, 0
    addi x29, x31, 4
    add x21, x13, x29
    addi x28, x21, 0
    lw x22, 0(x28)
    xor x30, x22, x20
    sltiu x23, x30, 1
    bne x23, x0, EqualS.block4
    jal x0, EqualS.block1
EqualS.block4:
    lui x31, 0
    addi x29, x31, 8
    add x24, x12, x29
    addi x28, x24, 0
    lw x25, 0(x28)
    lui x31, 0
    addi x29, x31, 8
    add x26, x13, x29
    addi x28, x26, 0
    lw x27, 0(x28)
    xor x30, x27, x25
    sltiu x28, x30, 1
    sw x28, 4(x2)
    lw x28, 4(x2)
    bne x28, x0, EqualS.block5
    jal x0, EqualS.block1
EqualS.block5:
    lui x31, 0
    addi x29, x31, 12
    add x28, x12, x29
    sw x28, 8(x2)
    lui x31, 0
    addi x29, x31, 12
    add x28, x13, x29
    sw x28, 12(x2)
    addi x28, x2, 16
    sw x28, 20(x2)
    lw x29, 20(x2)
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    addi x28, x2, 24
    sw x28, 28(x2)
    lw x29, 28(x2)
    lui x31, 0
    addi x28, x31, 1
    sw x28, 0(x29)
    jal x0, EqualS.block6
EqualS.block6:
    lw x28, 20(x2)
    lw x30, 0(x28)
    sw x30, 32(x2)
    lw x28, 8(x2)
    lw x29, 32(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 36(x2)
    lw x28, 36(x2)
    lw x30, 0(x28)
    sw x30, 40(x2)
    lw x28, 12(x2)
    lw x29, 32(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 44(x2)
    lw x28, 44(x2)
    lw x30, 0(x28)
    sw x30, 48(x2)
    lw x28, 40(x2)
    lw x29, 48(x2)
    xor x30, x29, x28
    sltiu x28, x30, 1
    sw x28, 52(x2)
    lw x28, 32(x2)
    addi x28, x28, 1
    sw x28, 56(x2)
    lw x29, 20(x2)
    lw x30, 56(x2)
    sw x30, 0(x29)
    lw x28, 52(x2)
    bne x28, x0, EqualS.block7
    jal x0, EqualS.block8
EqualS.block7:
    lw x28, 56(x2)
    lui x31, 0
    addi x29, x31, 2
    xor x30, x29, x28
    sltiu x30, x30, 1
    xori x28, x30, 1
    sw x28, 60(x2)
    lw x28, 60(x2)
    bne x28, x0, EqualS.block6
    jal x0, EqualS.block9
EqualS.block8:
    lw x29, 28(x2)
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    jal x0, EqualS.block9
EqualS.block9:
    lw x28, 28(x2)
    lw x30, 0(x28)
    sw x30, 64(x2)
    lw x28, 64(x2)
    bne x28, x0, EqualS.block2
    jal x0, EqualS.block1
EqualS.block1:
    addi x29, x5, 0
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    jal x0, EqualS.block2
EqualS.block2:
    addi x28, x5, 0
    lw x30, 0(x28)
    sw x30, 68(x2)
    lw x28, 68(x2)
    addi x10, x28, 0
    jal x0, EqualS.return
EqualS.return:
    addi x2, x2, 80
    lw x3, -8(x2)
    lw x1, -4(x2)
    jalr x0, 0(x1)
CloneS.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -80
CloneS.entry:
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
    lw x18, 0(x28)
    lui x31, 0
    addi x29, x31, 4
    add x19, x5, x29
    addi x29, x19, 0
    sw x18, 0(x29)
    lui x31, 0
    addi x29, x31, 8
    add x20, x12, x29
    addi x28, x20, 0
    lw x21, 0(x28)
    lui x31, 0
    addi x29, x31, 8
    add x22, x5, x29
    addi x29, x22, 0
    sw x21, 0(x29)
    lui x31, 0
    addi x29, x31, 12
    add x23, x12, x29
    lui x31, 0
    addi x29, x31, 12
    add x24, x5, x29
    addi x25, x2, 20
    addi x29, x25, 0
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    jal x0, CloneS.block1
CloneS.block1:
    addi x28, x25, 0
    lw x26, 0(x28)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x26, x30
    add x27, x23, x31
    addi x28, x27, 0
    lw x30, 0(x28)
    sw x30, 24(x2)
    lui x31, 0
    addi x30, x31, 4
    mul x31, x26, x30
    add x28, x24, x31
    sw x28, 28(x2)
    lw x29, 28(x2)
    lw x30, 24(x2)
    sw x30, 0(x29)
    addi x28, x26, 1
    sw x28, 32(x2)
    addi x29, x25, 0
    lw x30, 32(x2)
    sw x30, 0(x29)
    lw x28, 32(x2)
    lui x31, 0
    addi x29, x31, 2
    xor x30, x29, x28
    sltiu x30, x30, 1
    xori x28, x30, 1
    sw x28, 36(x2)
    lw x28, 36(x2)
    bne x28, x0, CloneS.block1
    jal x0, CloneS.block2
CloneS.block2:
    addi x28, x5, 0
    addi x29, x2, 40
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    addi x28, x2, 40
    addi x29, x3, 8
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    jal x0, CloneS.return
CloneS.return:
    addi x2, x2, 80
    lw x3, -8(x2)
    lw x1, -4(x2)
    jalr x0, 0(x1)
func1.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -16
func1.entry:
    addi x5, x2, 0
    addi x29, x5, 0
    sw x12, 0(x29)
    addi x28, x5, 0
    lw x6, 0(x28)
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x12, -12(x2)
    addi x2, x2, -20
    sw x3, -8(x2)
    lw x28, 12(x2)
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, println_i32.real_entry
    addi x2, x2, 20
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x12, -12(x2)
    addi x28, x5, 0
    lw x7, 0(x28)
    addi x10, x7, 0
    jal x0, func1.return
func1.return:
    addi x2, x2, 16
    lw x3, -8(x2)
    lw x1, -4(x2)
    jalr x0, 0(x1)
func2.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -48
func2.entry:
    addi x5, x2, 0
    addi x29, x5, 0
    addi x28, x3, 28
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    lui x31, 0
    addi x29, x31, 4
    add x6, x5, x29
    addi x29, x6, 0
    lui x31, 0
    addi x28, x31, 99
    sw x28, 0(x29)
    lui x31, 0
    addi x29, x31, 12
    add x7, x5, x29
    lui x31, 0
    addi x29, x31, 1
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x8, x7, x31
    addi x29, x8, 0
    lui x31, 0
    addi x28, x31, 77
    sw x28, 0(x29)
    addi x28, x5, 0
    addi x29, x2, 20
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    addi x28, x2, 20
    addi x29, x3, 8
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    jal x0, func2.return
func2.return:
    addi x2, x2, 48
    lw x3, -8(x2)
    lw x1, -4(x2)
    jalr x0, 0(x1)
rx_source_main.real_entry:
    sw x1, -4(x2)
    addi x2, x2, -272
rx_source_main.entry:
    addi x5, x2, 0
    addi x6, x2, 8
    sw x5, -4(x2)
    sw x6, -8(x2)
    addi x2, x2, -16
    sw x3, -8(x2)
    lui x31, 0
    addi x28, x31, 1
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, func1.real_entry
    addi x2, x2, 16
    lw x5, -4(x2)
    lw x6, -8(x2)
    addi x7, x10, 0
    addi x29, x6, 0
    sw x7, 0(x29)
    addi x8, x2, 12
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    addi x2, x2, -24
    sw x3, -8(x2)
    lui x31, 0
    addi x28, x31, 2
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, func1.real_entry
    addi x2, x2, 24
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    addi x9, x10, 0
    addi x29, x8, 0
    sw x9, 0(x29)
    lui x31, 0
    addi x29, x31, 0
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x18, x5, x31
    addi x29, x18, 0
    sw x7, 0(x29)
    lui x31, 0
    addi x29, x31, 1
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x19, x5, x31
    addi x29, x19, 0
    sw x9, 0(x29)
    addi x28, x5, 0
    addi x29, x2, 16
    lui x31, 0
    addi x30, x31, 8
    jal x31, internal.memcpy
    addi x20, x2, 24
    sw x5, -4(x2)
    sw x6, -8(x2)
    sw x7, -12(x2)
    sw x8, -16(x2)
    sw x9, -20(x2)
    sw x18, -24(x2)
    sw x19, -28(x2)
    sw x20, -32(x2)
    addi x2, x2, -40
    sw x3, -8(x2)
    lui x31, 0
    addi x28, x31, 3
    addi x12, x28, 0
    addi x3, x2, -8
    jal x1, func1.real_entry
    addi x2, x2, 40
    lw x5, -4(x2)
    lw x6, -8(x2)
    lw x7, -12(x2)
    lw x8, -16(x2)
    lw x9, -20(x2)
    lw x18, -24(x2)
    lw x19, -28(x2)
    lw x20, -32(x2)
    addi x21, x10, 0
    addi x29, x20, 0
    sw x21, 0(x29)
    addi x22, x2, 28
    lui x31, 0
    addi x29, x31, 0
    add x23, x22, x29
    addi x29, x23, 0
    lui x31, 0
    addi x28, x31, 0
    sw x28, 0(x29)
    lui x31, 0
    addi x29, x31, 4
    add x24, x22, x29
    addi x29, x24, 0
    sw x21, 0(x29)
    lui x31, 0
    addi x29, x31, 8
    add x25, x22, x29
    addi x29, x25, 0
    lui x31, 0
    addi x28, x31, 1
    sw x28, 0(x29)
    lui x31, 0
    addi x29, x31, 12
    add x26, x22, x29
    addi x29, x26, 0
    addi x28, x2, 16
    lui x31, 0
    addi x30, x31, 8
    jal x31, internal.memcpy
    addi x28, x22, 0
    addi x29, x2, 48
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    addi x27, x2, 68
    addi x29, x27, 0
    addi x28, x2, 48
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    addi x28, x27, 0
    addi x29, x2, 88
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    addi x28, x2, 108
    sw x28, 128(x2)
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
    addi x2, x2, -108
    sw x3, -8(x2)
    addi x28, x2, 196
    addi x29, x2, 20
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    addi x3, x2, -8
    jal x1, func2.real_entry
    addi x2, x2, 108
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
    addi x29, x2, 132
    addi x28, x2, -108
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    lw x29, 128(x2)
    addi x28, x2, 132
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    addi x28, x2, 152
    sw x28, 172(x2)
    lw x29, 172(x2)
    addi x28, x2, 132
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    lui x31, 0
    addi x29, x31, 4
    add x28, x27, x29
    sw x28, 176(x2)
    lw x28, 176(x2)
    lw x30, 0(x28)
    sw x30, 180(x2)
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
    lw x28, 248(x2)
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
    addi x29, x31, 12
    add x28, x27, x29
    sw x28, 184(x2)
    lw x28, 184(x2)
    lui x31, 0
    addi x29, x31, 1
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 188(x2)
    lw x28, 188(x2)
    lw x30, 0(x28)
    sw x30, 192(x2)
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
    lw x28, 260(x2)
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
    lw x28, 172(x2)
    lui x31, 0
    addi x29, x31, 4
    add x28, x28, x29
    sw x28, 196(x2)
    lw x28, 196(x2)
    lw x30, 0(x28)
    sw x30, 200(x2)
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
    lw x28, 268(x2)
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
    lw x28, 172(x2)
    lui x31, 0
    addi x29, x31, 12
    add x28, x28, x29
    sw x28, 204(x2)
    lw x28, 204(x2)
    lui x31, 0
    addi x29, x31, 1
    lui x31, 0
    addi x30, x31, 4
    mul x31, x29, x30
    add x28, x28, x31
    sw x28, 208(x2)
    lw x28, 208(x2)
    lw x30, 0(x28)
    sw x30, 212(x2)
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
    lw x28, 280(x2)
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
    addi x28, x27, 0
    addi x29, x2, 216
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    lw x29, 172(x2)
    addi x28, x2, 216
    lui x31, 0
    addi x30, x31, 20
    jal x31, internal.memcpy
    lw x28, 172(x2)
    lui x31, 0
    addi x29, x31, 4
    add x28, x28, x29
    sw x28, 236(x2)
    lw x28, 236(x2)
    lw x30, 0(x28)
    sw x30, 240(x2)
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
    lw x28, 308(x2)
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
    lw x28, 172(x2)
    lui x31, 0
    addi x29, x31, 8
    add x28, x28, x29
    sw x28, 244(x2)
    lw x28, 244(x2)
    lw x30, 0(x28)
    sw x30, 248(x2)
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
    lw x28, 316(x2)
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
    lw x28, 172(x2)
    lui x31, 0
    addi x29, x31, 0
    add x28, x28, x29
    sw x28, 252(x2)
    lw x28, 252(x2)
    lw x30, 0(x28)
    sw x30, 256(x2)
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
    lw x28, 324(x2)
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
    jal x0, rx_source_main.return
rx_source_main.return:
    addi x2, x2, 272
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
