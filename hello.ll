target triple = "riscv32-unknown-unknown-elf"

declare void @print_i32(i32)
declare void @println_i32(i32)
declare i32 @get_i32()
declare ptr @__rx_alloc(i32, i32)

%Vec = type{ i32, i32, ptr }

%Internal.Unit = type{  }

%Inner = type{ i32 }

%Outer = type{ %Inner, [3 x i32] }

define %Inner @CloneInner(ptr %temp10)
{
entry:
    %temp11 = alloca %Inner
    %temp13 = getelementptr %Inner, ptr %temp10, i32 0, i32 0
    %temp14 = load i32, ptr %temp13
    %temp15 = getelementptr %Inner, ptr %temp11, i32 0, i32 0
    store i32 %temp14, ptr %temp15
    %temp12 = load %Inner, ptr %temp11
    ret %Inner %temp12
}

define %Outer @CloneOuter(ptr %temp40)
{
entry:
    %temp41 = alloca %Outer
    %temp43 = getelementptr %Outer, ptr %temp40, i32 0, i32 0
    %temp44 = load %Inner, ptr %temp43
    %temp45 = getelementptr %Outer, ptr %temp41, i32 0, i32 0
    %temp46 = call %Inner @CloneInner(ptr %temp43)
    store %Inner %temp46, ptr %temp45
    %temp47 = getelementptr %Outer, ptr %temp40, i32 0, i32 1
    %temp48 = load [3 x i32], ptr %temp47
    %temp49 = getelementptr %Outer, ptr %temp41, i32 0, i32 1
    %temp50 = alloca i32
    store i32 0, ptr %temp50
    br label %block10
block10:
    %temp54 = load i32, ptr %temp50
    %temp51 = getelementptr [3 x i32], ptr %temp47, i32 0, i32 %temp54
    %temp52 = load i32, ptr %temp51
    %temp53 = getelementptr [3 x i32], ptr %temp49, i32 0, i32 %temp54
    store i32 %temp52, ptr %temp53
    %temp55 = add i32 %temp54, 1
    store i32 %temp55, ptr %temp50
    %temp56 = icmp ne i32 %temp55, 3
    br i1 %temp56, label %block10,label %block11
block11:
    %temp42 = load %Outer, ptr %temp41
    ret %Outer %temp42
}

define i1 @EqualInner(ptr %temp2, ptr %temp3){
entry:
    %temp1 = alloca i1
    store i1 true, ptr %temp1    %temp5 = getelementptr %Inner, ptr %temp2, i32 0, i32 0
    %temp7 = load i32, ptr %temp5
    %temp6 = getelementptr %Inner, ptr %temp3, i32 0, i32 0
    %temp8 = load i32, ptr %temp6
    %temp9 = icmp eq i32 %temp7, %temp8
    br i1 %temp9, label %block2, label %block1
block1:
    store i1 false, ptr %temp1
    br label %block2
block2:
    %temp4 = load i1, ptr %temp1
    ret i1 %temp4
}

define i1 @EqualOuter(ptr %temp17, ptr %temp18){
entry:
    %temp16 = alloca i1
    store i1 true, ptr %temp16    %temp20 = getelementptr %Outer, ptr %temp17, i32 0, i32 0
    %temp22 = load %Inner, ptr %temp20
    %temp21 = getelementptr %Outer, ptr %temp18, i32 0, i32 0
    %temp23 = load %Inner, ptr %temp21
    %temp24 = call i1 @EqualInner(ptr %temp20, ptr %temp21)
    br i1 %temp24, label %block5, label %block3
block5:
    %temp25 = getelementptr %Outer, ptr %temp17, i32 0, i32 1
    %temp27 = load [3 x i32], ptr %temp25
    %temp26 = getelementptr %Outer, ptr %temp18, i32 0, i32 1
    %temp28 = load [3 x i32], ptr %temp26
    %temp30 = alloca i32
    store i32 0, ptr %temp30
    %temp35 = alloca i1
    store i1 true, ptr %temp35
    br label %block6
block6:
    %temp36 = load i32, ptr %temp30
    %temp31 = getelementptr [3 x i32], ptr %temp25, i32 0, i32 %temp36
    %temp33 = load i32, ptr %temp31
    %temp32 = getelementptr [3 x i32], ptr %temp26, i32 0, i32 %temp36
    %temp34 = load i32, ptr %temp32
    %temp39 = icmp eq i32 %temp33, %temp34
    %temp37 = add i32 %temp36, 1
    store i32 %temp37, ptr %temp30
    br i1 %temp39, label %block7, label %block8
block7:
    %temp38 = icmp ne i32 %temp37, 3
    br i1 %temp38, label %block6,label %block9
block8:
    store i1 false, ptr %temp35
    br label %block9
block9:
    %temp29 = load i1, ptr %temp35
    br i1 %temp29, label %block4, label %block3
block3:
    store i1 false, ptr %temp16
    br label %block4
block4:
    %temp19 = load i1, ptr %temp16
    ret i1 %temp19
}

define %Internal.Unit @rx_source_main(){
entry:
    %temp1 = alloca %Inner
    %temp3 = getelementptr %Inner, ptr %temp1, i32 0, i32 0
    store i32 7, ptr %temp3
    %temp2 = load %Inner, ptr %temp1
    %temp4 = alloca [3 x i32]
    %temp6 = getelementptr [3 x i32], ptr %temp4, i32 0, i32 0
    store i32 1, ptr %temp6
    %temp7 = getelementptr [3 x i32], ptr %temp4, i32 0, i32 1
    store i32 2, ptr %temp7
    %temp8 = getelementptr [3 x i32], ptr %temp4, i32 0, i32 2
    store i32 3, ptr %temp8
    %temp5 = load [3 x i32], ptr %temp4
    %temp9 = alloca %Outer
    %temp11 = getelementptr %Outer, ptr %temp9, i32 0, i32 0
    store %Inner %temp2, ptr %temp11
    %temp12 = getelementptr %Outer, ptr %temp9, i32 0, i32 1
    store [3 x i32] %temp5, ptr %temp12
    %temp10 = load %Outer, ptr %temp9
    %var1 = alloca %Outer
    store %Outer %temp10, ptr %var1
    %temp13 = load %Outer, ptr %var1
    %temp14 = alloca %Outer
    %temp16 = load %Outer, ptr %var1
    %temp17 = call %Outer @CloneOuter(ptr %var1)
    store %Outer %temp17, ptr %temp14
    %temp15 = load %Outer, ptr %temp14
    %var2 = alloca %Outer
    store %Outer %temp15, ptr %var2
    %temp18 = load %Outer, ptr %var2
    %temp19 = load %Outer, ptr %var1
    %temp20 = call i1 @EqualOuter(ptr %var1, ptr %var2)
    %temp21 = zext i1 %temp20 to i32
    call void @println_i32(i32 %temp21)
    %temp22 = freeze %Internal.Unit zeroinitializer
    %temp23 = load %Outer, ptr %var1
    %temp26 = getelementptr %Outer, ptr %var1, i32 0, i32 0
    %temp25 = load %Inner, ptr %temp26
    %temp28 = alloca i32
    %temp27 =  call i32 @func2(ptr %temp26)
    store i32 %temp27, ptr %temp28
    call void @println_i32(i32 %temp27)
    %temp29 = freeze %Internal.Unit zeroinitializer
    %temp30 = load %Outer, ptr %var2
    %temp33 = getelementptr %Outer, ptr %var2, i32 0, i32 0
    %temp32 = load %Inner, ptr %temp33
    %temp36 = getelementptr %Inner, ptr %temp33, i32 0, i32 0
    %temp35 = load i32, ptr %temp36
    call void @println_i32(i32 %temp35)
    %temp37 = freeze %Internal.Unit zeroinitializer
    %var3 = alloca i32
    store i32 9, ptr %var3
    %var4 = alloca i32
    store i32 9, ptr %var4
    %temp38 = load i32, ptr %var3
    %var5 = alloca ptr
    store ptr %var3, ptr %var5
    %temp39 = load i32, ptr %var4
    %var6 = alloca ptr
    store ptr %var4, ptr %var6
    %temp40 = load ptr, ptr %var6
    %temp41 = load ptr, ptr %var5
    %temp43 = load i32, ptr %temp41
    %temp44 = load i32, ptr %temp40
    %temp42 = icmp eq i32 %temp43, %temp44
    %temp45 = zext i1 %temp42 to i32
    call void @println_i32(i32 %temp45)
    %temp46 = freeze %Internal.Unit zeroinitializer
    %temp47 = load ptr, ptr %var5
    %temp48 = load i32, ptr %temp47
    store i32 11, ptr %temp47
    %temp49 = freeze %Internal.Unit zeroinitializer
    %temp50 = load ptr, ptr %var6
    %temp51 = load ptr, ptr %var5
    %temp53 = load i32, ptr %temp51
    %temp54 = load i32, ptr %temp50
    %temp52 = icmp eq i32 %temp53, %temp54
    %temp55 = xor i1 %temp52, true
    %temp56 = zext i1 %temp55 to i32
    call void @println_i32(i32 %temp56)
    %temp57 = freeze %Internal.Unit zeroinitializer
    %temp58 = load ptr, ptr %var6
    %temp59 = load i32, ptr %temp58
    call void @println_i32(i32 %temp59)
    %temp60 = freeze %Internal.Unit zeroinitializer
    %temp61 = freeze %Internal.Unit zeroinitializer
    ret %Internal.Unit %temp61
}

define i32 @func2(ptr %param1){
entry:
    %prm1 = alloca ptr
    store ptr %param1, ptr %prm1
    %temp1 = load ptr, ptr %prm1
    %temp2 = load %Inner, ptr %temp1
    %temp5 = getelementptr %Inner, ptr %temp1, i32 0, i32 0
    %temp4 = load i32, ptr %temp5
    %temp6 = add i32 %temp4, 100
    ret i32 %temp6
}

define i32 @main(){
    call %Internal.Unit @rx_source_main()
    ret i32 0
}

