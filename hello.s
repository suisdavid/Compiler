	.attribute	4, 16
	.attribute	5, "rv32i2p1_m2p0_zmmul1p0"
	.file	"hello.ll"
	.text
	.globl	CloneCounter                    # -- Begin function CloneCounter
	.p2align	2
	.type	CloneCounter,@function
CloneCounter:                           # @CloneCounter
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
	.size	CloneCounter, .Lfunc_end0-CloneCounter
	.cfi_endproc
                                        # -- End function
	.globl	EqualCounter                    # -- Begin function EqualCounter
	.p2align	2
	.type	EqualCounter,@function
EqualCounter:                           # @EqualCounter
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	li	a2, 1
	sb	a2, 15(sp)
	lw	a0, 0(a0)
	lw	a1, 0(a1)
	beq	a0, a1, .LBB1_2
	j	.LBB1_1
.LBB1_1:                                # %block1
	li	a0, 0
	sb	a0, 15(sp)
	j	.LBB1_2
.LBB1_2:                                # %block2
	lbu	a0, 15(sp)
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end1:
	.size	EqualCounter, .Lfunc_end1-EqualCounter
	.cfi_endproc
                                        # -- End function
	.globl	func1                           # -- Begin function func1
	.p2align	2
	.type	func1,@function
func1:                                  # @func1
	.cfi_startproc
# %bb.0:                                # %entry
	li	a0, 7
	ret
.Lfunc_end2:
	.size	func1, .Lfunc_end2-func1
	.cfi_endproc
                                        # -- End function
	.globl	rx_source_main                  # -- Begin function rx_source_main
	.p2align	2
	.type	rx_source_main,@function
rx_source_main:                         # @rx_source_main
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -112
	.cfi_def_cfa_offset 112
	sw	ra, 108(sp)                     # 4-byte Folded Spill
	.cfi_offset ra, -4
	call	func3
	sw	a0, 104(sp)
	sw	a0, 96(sp)
	addi	a0, sp, 96
	sw	a0, 12(sp)                      # 4-byte Folded Spill
	li	a1, 4
	sw	a1, 16(sp)                      # 4-byte Folded Spill
	call	func5
	lw	a0, 12(sp)                      # 4-byte Folded Reload
	call	func4
	sw	a0, 92(sp)
	call	println_i32
	lw	a0, 96(sp)
	call	func7
	sw	a0, 88(sp)
	sw	a0, 80(sp)
	lw	a0, 96(sp)
	call	println_i32
	lw	a0, 80(sp)
	call	func6
	sw	a0, 76(sp)
	call	println_i32
	lw	a0, 12(sp)                      # 4-byte Folded Reload
	li	a1, 2
	sw	a1, 24(sp)                      # 4-byte Folded Spill
	call	func5
	lw	a0, 12(sp)                      # 4-byte Folded Reload
	call	func4
	sw	a0, 72(sp)
	call	println_i32
	lw	a1, 16(sp)                      # 4-byte Folded Reload
	lw	a0, 96(sp)
	sw	a0, 20(sp)                      # 4-byte Folded Spill
	mv	a0, a1
	call	__rx_alloc
	lw	a1, 20(sp)                      # 4-byte Folded Reload
	sw	a1, 0(a0)
	sw	a0, 64(sp)
	sw	a0, 56(sp)
	lw	a0, 56(sp)
	li	a1, 1
	call	func5
	lw	a0, 56(sp)
	call	func4
	sw	a0, 52(sp)
	call	println_i32
	lw	a1, 24(sp)                      # 4-byte Folded Reload
	addi	a0, sp, 56
	sw	a0, 48(sp)
	lw	a0, 48(sp)
	lw	a0, 0(a0)
	call	func5
	lw	a0, 48(sp)
	lw	a0, 0(a0)
	call	func4
	sw	a0, 44(sp)
	call	println_i32
	call	func3
	sw	a0, 40(sp)
	call	func7
	sw	a0, 32(sp)
	addi	a0, sp, 32
	call	func4
	sw	a0, 28(sp)
	call	println_i32
	lw	ra, 108(sp)                     # 4-byte Folded Reload
	.cfi_restore ra
	addi	sp, sp, 112
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end3:
	.size	rx_source_main, .Lfunc_end3-rx_source_main
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
	li	a0, 3
	sw	a0, 8(sp)
	lw	a0, 8(sp)
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end4:
	.size	func3, .Lfunc_end4-func3
	.cfi_endproc
                                        # -- End function
	.globl	func4                           # -- Begin function func4
	.p2align	2
	.type	func4,@function
func4:                                  # @func4
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	a0, 8(sp)
	lw	a0, 8(sp)
	lw	a0, 0(a0)
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end5:
	.size	func4, .Lfunc_end5-func4
	.cfi_endproc
                                        # -- End function
	.globl	func5                           # -- Begin function func5
	.p2align	2
	.type	func5,@function
func5:                                  # @func5
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	a0, 8(sp)
	sw	a1, 4(sp)
	lw	a2, 4(sp)
	lw	a1, 8(sp)
	lw	a0, 0(a1)
	add	a0, a0, a2
	sw	a0, 0(a1)
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end6:
	.size	func5, .Lfunc_end6-func5
	.cfi_endproc
                                        # -- End function
	.globl	func6                           # -- Begin function func6
	.p2align	2
	.type	func6,@function
func6:                                  # @func6
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	a0, 8(sp)
	lw	a0, 8(sp)
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end7:
	.size	func6, .Lfunc_end7-func6
	.cfi_endproc
                                        # -- End function
	.globl	func7                           # -- Begin function func7
	.p2align	2
	.type	func7,@function
func7:                                  # @func7
	.cfi_startproc
# %bb.0:                                # %entry
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	a0, 8(sp)
	lw	a0, 8(sp)
	addi	a0, a0, 10
	sw	a0, 8(sp)
	lw	a0, 8(sp)
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end8:
	.size	func7, .Lfunc_end8-func7
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
.Lfunc_end9:
	.size	main, .Lfunc_end9-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
