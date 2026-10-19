target triple = "riscv32-unknown-unknown-elf"

declare void @print_i32(i32)
declare void @println_i32(i32)
declare i32 @get_i32()
declare ptr @__rx_alloc(i32, i32)

%Vec = type{ i32, i32, ptr }

%Internal.Unit = type{  }

%Packet = type{ [8 x i32], i1 }

%View = type{ ptr, i32 }

define %Packet @func1(%Packet %param1, i32 %param2){
entry:
    %prm1 = alloca %Packet
    store %Packet %param1, ptr %prm1
    %prm2 = alloca i32
    store i32 %param2, ptr %prm2
    %temp1 = load i32, ptr %prm2
    %temp2 = load %Packet, ptr %prm1
    %temp5 = getelementptr %Packet, ptr %prm1, i32 0, i32 0
    %temp4 = load [8 x i32], ptr %temp5
    %temp8 = getelementptr [8 x i32], ptr %temp5, i32 0, i32 7
    %temp7 = load i32, ptr %temp8
    %temp9 = add i32 %temp7, %temp1
    store i32 %temp9, ptr %temp8
    %temp11 = freeze %Internal.Unit zeroinitializer
    %temp12 = load %Packet, ptr %prm1
    %temp15 = getelementptr %Packet, ptr %prm1, i32 0, i32 1
    %temp14 = load i1, ptr %temp15
    %temp16 = xor i1 %temp14, true
    %temp18 = load %Packet, ptr %prm1
    %temp21 = getelementptr %Packet, ptr %prm1, i32 0, i32 1
    %temp20 = load i1, ptr %temp21
    store i1 %temp16, ptr %temp21
    %temp22 = freeze %Internal.Unit zeroinitializer
    %temp23 = load %Packet, ptr %prm1
    ret %Packet %temp23
    
}

define %Packet @func2(i32 %param1){
entry:
    %prm1 = alloca i32
    store i32 %param1, ptr %prm1
    %temp1 = load i32, ptr %prm1
    %temp2 = alloca [8 x i32]
    %temp4 = alloca i32
    store i32 0, ptr %temp4
    br label %block1
block1:
    %temp5 = load i32, ptr %temp4
    %temp7 = getelementptr [8 x i32], ptr %temp2, i32 0, i32 %temp5
    store i32 %temp1, ptr %temp7
    %temp6 = add i32 %temp5, 1
    store i32 %temp6, ptr %temp4
    %temp8 = icmp eq i32 %temp6, 8
    br i1 %temp8, label %block2, label %block1
block2:
    %temp3 = load [8 x i32], ptr %temp2
    %temp9 = alloca %Packet
    %temp11 = getelementptr %Packet, ptr %temp9, i32 0, i32 0
    store [8 x i32] %temp3, ptr %temp11
    %temp12 = getelementptr %Packet, ptr %temp9, i32 0, i32 1
    store i1 1, ptr %temp12
    %temp10 = load %Packet, ptr %temp9
    ret %Packet %temp10
    
}

define i32 @func3(i32 %param1, i32 %param2){
entry:
    %prm1 = alloca i32
    store i32 %param1, ptr %prm1
    %prm2 = alloca i32
    store i32 %param2, ptr %prm2
    %temp1 = load i32, ptr %prm1
    %temp2 = load i32, ptr %prm2
    %temp3 = add i32 %temp1, %temp2
    ret i32 %temp3
    
}

define %Internal.Unit @rx_source_main(){
entry:
    %temp2 = alloca i32
    %temp1 =  call i32 @func3(i32 1, i32 2)
    store i32 %temp1, ptr %temp2
    call void @println_i32(i32 %temp1)
    %temp3 = freeze %Internal.Unit zeroinitializer
    %temp4 = freeze %Internal.Unit zeroinitializer
    ret %Internal.Unit %temp4
    
}

define i32 @main(){
    call %Internal.Unit @rx_source_main()
    ret i32 0
    
}

