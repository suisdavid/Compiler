	.attribute	4, 16
	.attribute	5, "rv32i2p1_m2p0_zmmul1p0"
	.file	"hello.ll"
	.text
	.globl	CloneInner                      # -- Begin function CloneInner
	.p2align	2
	.type	CloneInner,@function
CloneInner:                             # @CloneInner
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	lw	a0, 0(a0)
	sw	a0, 8(sp)
	lw	a0, 8(sp)
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end0:
	.size	CloneInner, .Lfunc_end0-CloneInner
	.cfi_endproc
                                        # -- End function
	.globl	CloneOuter                      # -- Begin function CloneOuter
	.p2align	2
	.type	CloneOuter,@function
CloneOuter:                             # @CloneOuter
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -48
	.cfi_def_cfa_offset 48
	sw	ra, 44(sp)                      # 4-byte Folded Spill
	.cfi_offset ra, -4
	sw	a1, 8(sp)                       # 4-byte Folded Spill
	mv	a1, a0
	lw	a0, 8(sp)                       # 4-byte Folded Reload
	sw	a1, 4(sp)                       # 4-byte Folded Spill
	call	CloneInner
	lw	a1, 8(sp)                       # 4-byte Folded Reload
	sw	a0, 24(sp)
	addi	a0, a1, 4
	sw	a0, 12(sp)                      # 4-byte Folded Spill
	addi	a0, sp, 28
	sw	a0, 16(sp)                      # 4-byte Folded Spill
	li	a0, 0
	sw	a0, 20(sp)
	j	.LBB1_1
.LBB1_1:                                # %block10
                                        # =>This Inner Loop Header: Depth=1
	lw	a2, 16(sp)                      # 4-byte Folded Reload
	lw	a1, 12(sp)                      # 4-byte Folded Reload
	lw	a0, 20(sp)
	slli	a3, a0, 2
	add	a1, a1, a3
	lw	a1, 0(a1)
	add	a2, a2, a3
	sw	a1, 0(a2)
	addi	a0, a0, 1
	sw	a0, 20(sp)
	li	a1, 3
	bne	a0, a1, .LBB1_1
	j	.LBB1_2
.LBB1_2:                                # %block11
	lw	a1, 4(sp)                       # 4-byte Folded Reload
	lw	a0, 24(sp)
	lw	a2, 28(sp)
	lw	a3, 32(sp)
	lw	a4, 36(sp)
	sw	a4, 12(a1)
	sw	a3, 8(a1)
	sw	a2, 4(a1)
	sw	a0, 0(a1)
	lw	ra, 44(sp)                      # 4-byte Folded Reload
	.cfi_restore ra
	addi	sp, sp, 48
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end1:
	.size	CloneOuter, .Lfunc_end1-CloneOuter
	.cfi_endproc
                                        # -- End function
	.globl	EqualInner                      # -- Begin function EqualInner
	.p2align	2
	.type	EqualInner,@function
EqualInner:                             # @EqualInner
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	li	a2, 1
	sb	a2, 15(sp)
	lw	a0, 0(a0)
	lw	a1, 0(a1)
	beq	a0, a1, .LBB2_2
	j	.LBB2_1
.LBB2_1:                                # %block1
	li	a0, 0
	sb	a0, 15(sp)
	j	.LBB2_2
.LBB2_2:                                # %block2
	lbu	a0, 15(sp)
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end2:
	.size	EqualInner, .Lfunc_end2-EqualInner
	.cfi_endproc
                                        # -- End function
	.globl	EqualOuter                      # -- Begin function EqualOuter
	.p2align	2
	.type	EqualOuter,@function
EqualOuter:                             # @EqualOuter
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -48
	.cfi_def_cfa_offset 48
	sw	ra, 44(sp)                      # 4-byte Folded Spill
	sw	s0, 40(sp)                      # 4-byte Folded Spill
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	addi	s0, sp, 48
	.cfi_def_cfa s0, 0
	sw	a1, -20(s0)                     # 4-byte Folded Spill
	sw	a0, -16(s0)                     # 4-byte Folded Spill
	li	a2, 1
	sb	a2, -9(s0)
	call	EqualInner
	andi	a0, a0, 1
	beqz	a0, .LBB3_6
	j	.LBB3_1
.LBB3_1:                                # %block5
	lw	a0, -20(s0)                     # 4-byte Folded Reload
	lw	a1, -16(s0)                     # 4-byte Folded Reload
	addi	a1, a1, 4
	sw	a1, -36(s0)                     # 4-byte Folded Spill
	addi	a0, a0, 4
	sw	a0, -32(s0)                     # 4-byte Folded Spill
	mv	a1, sp
	addi	a0, a1, -16
	sw	a0, -28(s0)                     # 4-byte Folded Spill
	mv	sp, a0
	li	a0, 0
	sw	a0, -16(a1)
	mv	a1, sp
	addi	a0, a1, -16
	sw	a0, -24(s0)                     # 4-byte Folded Spill
	mv	sp, a0
	li	a0, 1
	sb	a0, -16(a1)
	j	.LBB3_2
.LBB3_2:                                # %block6
                                        # =>This Inner Loop Header: Depth=1
	lw	a3, -28(s0)                     # 4-byte Folded Reload
	lw	a1, -32(s0)                     # 4-byte Folded Reload
	lw	a0, -36(s0)                     # 4-byte Folded Reload
	lw	a2, 0(a3)
	slli	a4, a2, 2
	add	a0, a0, a4
	lw	a0, 0(a0)
	add	a1, a1, a4
	lw	a1, 0(a1)
	addi	a2, a2, 1
	sw	a2, -40(s0)                     # 4-byte Folded Spill
	sw	a2, 0(a3)
	bne	a0, a1, .LBB3_4
	j	.LBB3_3
.LBB3_3:                                # %block7
                                        #   in Loop: Header=BB3_2 Depth=1
	lw	a0, -40(s0)                     # 4-byte Folded Reload
	li	a1, 3
	bne	a0, a1, .LBB3_2
	j	.LBB3_5
.LBB3_4:                                # %block8
	lw	a1, -24(s0)                     # 4-byte Folded Reload
	li	a0, 0
	sb	a0, 0(a1)
	j	.LBB3_5
.LBB3_5:                                # %block9
	lw	a0, -24(s0)                     # 4-byte Folded Reload
	lbu	a0, 0(a0)
	bnez	a0, .LBB3_7
	j	.LBB3_6
.LBB3_6:                                # %block3
	li	a0, 0
	sb	a0, -9(s0)
	j	.LBB3_7
.LBB3_7:                                # %block4
	lbu	a0, -9(s0)
	addi	sp, s0, -48
	.cfi_def_cfa sp, 48
	lw	ra, 44(sp)                      # 4-byte Folded Reload
	lw	s0, 40(sp)                      # 4-byte Folded Reload
	.cfi_restore ra
	.cfi_restore s0
	addi	sp, sp, 48
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end3:
	.size	EqualOuter, .Lfunc_end3-EqualOuter
	.cfi_endproc
                                        # -- End function
	.globl	rx_source_main                  # -- Begin function rx_source_main
	.p2align	2
	.type	rx_source_main,@function
rx_source_main:                         # @rx_source_main
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -144
	.cfi_def_cfa_offset 144
	sw	ra, 140(sp)                     # 4-byte Folded Spill
	.cfi_offset ra, -4
	li	a0, 7
	sw	a0, 136(sp)
	lw	a3, 136(sp)
	li	a0, 1
	sw	a0, 124(sp)
	li	a0, 2
	sw	a0, 128(sp)
	li	a0, 3
	sw	a0, 132(sp)
	lw	a0, 124(sp)
	lw	a1, 128(sp)
	lw	a2, 132(sp)
	sw	a3, 104(sp)
	sw	a2, 116(sp)
	sw	a1, 112(sp)
	sw	a0, 108(sp)
	lw	a0, 104(sp)
	lw	a1, 108(sp)
	lw	a2, 112(sp)
	lw	a3, 116(sp)
	sw	a3, 100(sp)
	sw	a2, 96(sp)
	sw	a1, 92(sp)
	sw	a0, 88(sp)
	addi	a0, sp, 16
	addi	a1, sp, 88
	sw	a1, 12(sp)                      # 4-byte Folded Spill
	call	CloneOuter
	lw	a0, 12(sp)                      # 4-byte Folded Reload
	lw	a1, 16(sp)
	lw	a2, 20(sp)
	lw	a3, 24(sp)
	lw	a4, 28(sp)
	sw	a4, 84(sp)
	sw	a3, 80(sp)
	sw	a2, 76(sp)
	sw	a1, 72(sp)
	lw	a1, 72(sp)
	lw	a2, 76(sp)
	lw	a3, 80(sp)
	lw	a4, 84(sp)
	sw	a4, 68(sp)
	sw	a3, 64(sp)
	sw	a2, 60(sp)
	sw	a1, 56(sp)
	addi	a1, sp, 56
	call	EqualOuter
	andi	a0, a0, 1
	call	println_i32
	lw	a0, 12(sp)                      # 4-byte Folded Reload
	call	func2
	sw	a0, 52(sp)
	call	println_i32
	lw	a0, 56(sp)
	call	println_i32
	li	a0, 9
	sw	a0, 48(sp)
	sw	a0, 44(sp)
	addi	a0, sp, 48
	sw	a0, 40(sp)
	addi	a0, sp, 44
	sw	a0, 32(sp)
	lw	a1, 32(sp)
	lw	a0, 40(sp)
	lw	a0, 0(a0)
	lw	a1, 0(a1)
	xor	a0, a0, a1
	seqz	a0, a0
	call	println_i32
	lw	a1, 40(sp)
	li	a0, 11
	sw	a0, 0(a1)
	lw	a1, 32(sp)
	lw	a0, 40(sp)
	lw	a0, 0(a0)
	lw	a1, 0(a1)
	xor	a0, a0, a1
	snez	a0, a0
	call	println_i32
	lw	a0, 32(sp)
	lw	a0, 0(a0)
	call	println_i32
	lw	ra, 140(sp)                     # 4-byte Folded Reload
	.cfi_restore ra
	addi	sp, sp, 144
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end4:
	.size	rx_source_main, .Lfunc_end4-rx_source_main
	.cfi_endproc
                                        # -- End function
	.globl	func2                           # -- Begin function func2
	.p2align	2
	.type	func2,@function
func2:                                  # @func2
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	a0, 8(sp)
	lw	a0, 8(sp)
	lw	a0, 0(a0)
	addi	a0, a0, 100
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end5:
	.size	func2, .Lfunc_end5-func2
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
.Lfunc_end6:
	.size	main, .Lfunc_end6-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
