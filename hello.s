	.attribute	4, 16
	.attribute	5, "rv32i2p1_m2p0_zmmul1p0"
	.file	"hello.ll"
	.text
	.globl	func1                           # -- Begin function func1
	.p2align	2
	.type	func1,@function
func1:                                  # @func1
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -48
	.cfi_def_cfa_offset 48
	sw	a1, 4(sp)                       # 4-byte Folded Spill
	mv	a1, a0
	lw	a0, 4(sp)                       # 4-byte Folded Reload
	lw	t1, 52(sp)
	lw	t0, 48(sp)
                                        # kill: def $x7 killed $x17
                                        # kill: def $x7 killed $x16
                                        # kill: def $x7 killed $x15
                                        # kill: def $x7 killed $x14
                                        # kill: def $x7 killed $x13
                                        # kill: def $x7 killed $x12
                                        # kill: def $x7 killed $x10
	lw	t2, 56(sp)
	andi	t1, t1, 1
	sb	t1, 40(sp)
	sw	t0, 36(sp)
	sw	a7, 32(sp)
	sw	a6, 28(sp)
	sw	a5, 24(sp)
	sw	a4, 20(sp)
	sw	a3, 16(sp)
	sw	a2, 12(sp)
	sw	a0, 8(sp)
	lw	a2, 56(sp)
	lw	a0, 36(sp)
	add	a0, a0, a2
	sw	a0, 36(sp)
	lbu	a0, 40(sp)
	not	a0, a0
	andi	a0, a0, 1
	sb	a0, 40(sp)
	lbu	a0, 40(sp)
	lw	a2, 8(sp)
	lw	a3, 12(sp)
	lw	a4, 16(sp)
	lw	a5, 20(sp)
	lw	a6, 24(sp)
	lw	a7, 28(sp)
	lw	t0, 32(sp)
	lw	t1, 36(sp)
	sw	t1, 28(a1)
	sw	t0, 24(a1)
	sw	a7, 20(a1)
	sw	a6, 16(a1)
	sw	a5, 12(a1)
	sw	a4, 8(a1)
	sw	a3, 4(a1)
	sw	a2, 0(a1)
	andi	a0, a0, 1
	sb	a0, 32(a1)
	addi	sp, sp, 48
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end0:
	.size	func1, .Lfunc_end0-func1
	.cfi_endproc
                                        # -- End function
	.globl	func2                           # -- Begin function func2
	.p2align	2
	.type	func2,@function
func2:                                  # @func2
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -64
	.cfi_def_cfa_offset 64
	sw	ra, 60(sp)                      # 4-byte Folded Spill
	sw	s0, 56(sp)                      # 4-byte Folded Spill
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	addi	s0, sp, 64
	.cfi_def_cfa s0, 0
	sw	a0, -56(s0)                     # 4-byte Folded Spill
	sw	a1, -12(s0)
	lw	a0, -12(s0)
	sw	a0, -52(s0)                     # 4-byte Folded Spill
	li	a0, 0
	sw	a0, -48(s0)
	j	.LBB1_1
.LBB1_1:                                # %block1
                                        # =>This Inner Loop Header: Depth=1
	lw	a1, -52(s0)                     # 4-byte Folded Reload
	lw	a0, -48(s0)
	slli	a3, a0, 2
	addi	a2, s0, -44
	add	a2, a2, a3
	sw	a1, 0(a2)
	addi	a0, a0, 1
	sw	a0, -48(s0)
	li	a1, 8
	bne	a0, a1, .LBB1_1
	j	.LBB1_2
.LBB1_2:                                # %block2
	lw	a1, -56(s0)                     # 4-byte Folded Reload
	lw	a0, -44(s0)
	lw	a2, -40(s0)
	lw	a3, -36(s0)
	lw	a4, -32(s0)
	lw	a5, -28(s0)
	lw	a6, -24(s0)
	lw	a7, -20(s0)
	lw	t0, -16(s0)
	mv	t1, sp
	addi	t2, t1, -48
	mv	sp, t2
	sw	t0, -20(t1)
	sw	a7, -24(t1)
	sw	a6, -28(t1)
	sw	a5, -32(t1)
	sw	a4, -36(t1)
	sw	a3, -40(t1)
	sw	a2, -44(t1)
	sw	a0, -48(t1)
	li	a0, 1
	sb	a0, -16(t1)
	lbu	a0, -16(t1)
	lw	a2, -48(t1)
	lw	a3, -44(t1)
	lw	a4, -40(t1)
	lw	a5, -36(t1)
	lw	a6, -32(t1)
	lw	a7, -28(t1)
	lw	t0, -24(t1)
	lw	t1, -20(t1)
	sw	t1, 28(a1)
	sw	t0, 24(a1)
	sw	a7, 20(a1)
	sw	a6, 16(a1)
	sw	a5, 12(a1)
	sw	a4, 8(a1)
	sw	a3, 4(a1)
	sw	a2, 0(a1)
	andi	a0, a0, 1
	sb	a0, 32(a1)
	addi	sp, s0, -64
	.cfi_def_cfa sp, 64
	lw	ra, 60(sp)                      # 4-byte Folded Reload
	lw	s0, 56(sp)                      # 4-byte Folded Reload
	.cfi_restore ra
	.cfi_restore s0
	addi	sp, sp, 64
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end1:
	.size	func2, .Lfunc_end1-func2
	.cfi_endproc
                                        # -- End function
	.globl	func3                           # -- Begin function func3
	.p2align	2
	.type	func3,@function
func3:                                  # @func3
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	a0, 12(sp)
	sw	a1, 8(sp)
	lw	a0, 12(sp)
	lw	a1, 8(sp)
	add	a0, a0, a1
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end2:
	.size	func3, .Lfunc_end2-func3
	.cfi_endproc
                                        # -- End function
	.globl	rx_source_main                  # -- Begin function rx_source_main
	.p2align	2
	.type	rx_source_main,@function
rx_source_main:                         # @rx_source_main
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	ra, 12(sp)                      # 4-byte Folded Spill
	.cfi_offset ra, -4
	li	a0, 1
	li	a1, 2
	call	func3
	sw	a0, 8(sp)
	call	println_i32
	lw	ra, 12(sp)                      # 4-byte Folded Reload
	.cfi_restore ra
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end3:
	.size	rx_source_main, .Lfunc_end3-rx_source_main
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	2
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	ra, 12(sp)                      # 4-byte Folded Spill
	.cfi_offset ra, -4
	call	rx_source_main
	li	a0, 0
	lw	ra, 12(sp)                      # 4-byte Folded Reload
	.cfi_restore ra
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end4:
	.size	main, .Lfunc_end4-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
