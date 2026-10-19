target triple = "riscv32-unknown-unknown-elf"

declare void @print_i32(i32)
declare void @println_i32(i32)
declare i32 @get_i32()
declare ptr @__rx_alloc(i32, i32)

%Vec = type{ i32, i32, ptr }

%Internal.Unit = type{  }

%Counter = type{ i32 }

define %Internal.Unit @rx_source_main(){
entry:
    %temp2 = alloca %Counter
    %temp1 =  call %Counter @func2()
    store %Counter %temp1, ptr %temp2
    %var1 = alloca %Counter
    store %Counter %temp1, ptr %var1
    %temp3 = load %Counter, ptr %var1
    call void @func4(ptr %var1, i32 4)
    %temp4 = freeze %Internal.Unit zeroinitializer
    %temp5 = load %Counter, ptr %var1
    %temp7 = alloca i32
    %temp6 =  call i32 @func3(ptr %var1)
    store i32 %temp6, ptr %temp7
    call void @println_i32(i32 %temp6)
    %temp8 = freeze %Internal.Unit zeroinitializer
    %temp9 = load %Counter, ptr %var1
    %temp11 = alloca %Counter
    %temp10 =  call %Counter @func6(%Counter %temp9)
    store %Counter %temp10, ptr %temp11
    %var2 = alloca %Counter
    store %Counter %temp10, ptr %var2
    %temp12 = load %Counter, ptr %var1
    %temp15 = getelementptr %Counter, ptr %var1, i32 0, i32 0
    %temp14 = load i32, ptr %temp15
    call void @println_i32(i32 %temp14)
    %temp16 = freeze %Internal.Unit zeroinitializer
    %temp17 = load %Counter, ptr %var2
    %temp19 = alloca i32
    %temp18 =  call i32 @func5(%Counter %temp17)
    store i32 %temp18, ptr %temp19
    call void @println_i32(i32 %temp18)
    %temp20 = freeze %Internal.Unit zeroinitializer
    %temp21 = load %Counter, ptr %var1
    call void @func4(ptr %var1, i32 2)
    %temp22 = freeze %Internal.Unit zeroinitializer
    %temp23 = load %Counter, ptr %var1
    %temp25 = alloca i32
    %temp24 =  call i32 @func3(ptr %var1)
    store i32 %temp24, ptr %temp25
    call void @println_i32(i32 %temp24)
    %temp26 = freeze %Internal.Unit zeroinitializer
    %temp27 = load %Counter, ptr %var1
    %temp28 = alloca ptr
    %temp29 = call ptr @__rx_alloc(i32 4, i32 4)
    store %Counter %temp27, ptr %temp29
    store ptr %temp29, ptr %temp28
    %var3 = alloca ptr
    store ptr %temp29, ptr %var3
    %temp30 = load ptr, ptr %var3
    %temp31 = load %Counter, ptr %temp30
    call void @func4(%Counter %temp31, i32 1)
    %temp33 = freeze %Internal.Unit zeroinitializer
    %temp34 = load ptr, ptr %var3
    %temp35 = load %Counter, ptr %temp34
    %temp38 = alloca i32
    %temp37 =  call i32 @func3(%Counter %temp35)
    store i32 %temp37, ptr %temp38
    call void @println_i32(i32 %temp37)
    %temp39 = freeze %Internal.Unit zeroinitializer
    %temp40 = load ptr, ptr %var3
    %var4 = alloca ptr
    store ptr %var3, ptr %var4
    %temp41 = load ptr, ptr %var4
    %temp42 = load ptr, ptr %temp41
    %temp43 = load %Counter, ptr %temp42
    call void @func4(%Counter %temp43, i32 2)
    %temp45 = freeze %Internal.Unit zeroinitializer
    %temp46 = load ptr, ptr %var4
    %temp47 = load ptr, ptr %temp46
    %temp48 = load %Counter, ptr %temp47
    %temp51 = alloca i32
    %temp50 =  call i32 @func3(%Counter %temp48)
    store i32 %temp50, ptr %temp51
    call void @println_i32(i32 %temp50)
    %temp52 = freeze %Internal.Unit zeroinitializer
    %temp54 = alloca %Counter
    %temp53 =  call %Counter @func2()
    store %Counter %temp53, ptr %temp54
    %temp56 = alloca %Counter
    %temp55 =  call %Counter @func6(%Counter %temp53)
    store %Counter %temp55, ptr %temp56
    %temp58 = alloca i32
    %temp57 =  call i32 @func3(ptr %temp56)
    store i32 %temp57, ptr %temp58
    call void @println_i32(i32 %temp57)
    %temp59 = freeze %Internal.Unit zeroinitializer
    %temp60 = freeze %Internal.Unit zeroinitializer
    ret %Internal.Unit %temp60
    
}

define %Counter @func2(){
entry:
    %temp1 = alloca %Counter
    %temp3 = getelementptr %Counter, ptr %temp1, i32 0, i32 0
    store i32 3, ptr %temp3
    %temp2 = load %Counter, ptr %temp1
    ret %Counter %temp2
    
}

define i32 @func3(ptr %param1){
entry:
    %prm1 = alloca ptr
    store ptr %param1, ptr %prm1
    %temp1 = load ptr, ptr %prm1
    %temp2 = load %Counter, ptr %temp1
    %temp5 = getelementptr %Counter, ptr %temp1, i32 0, i32 0
    %temp4 = load i32, ptr %temp5
    ret i32 %temp4
    
}

define %Internal.Unit @func4(ptr %param1, i32 %param2){
entry:
    %prm1 = alloca ptr
    store ptr %param1, ptr %prm1
    %prm2 = alloca i32
    store i32 %param2, ptr %prm2
    %temp1 = load i32, ptr %prm2
    %temp2 = load ptr, ptr %prm1
    %temp3 = load %Counter, ptr %temp2
    %temp6 = getelementptr %Counter, ptr %temp2, i32 0, i32 0
    %temp5 = load i32, ptr %temp6
    %temp7 = add i32 %temp5, %temp1
    store i32 %temp7, ptr %temp6
    %temp9 = freeze %Internal.Unit zeroinitializer
    %temp10 = freeze %Internal.Unit zeroinitializer
    ret %Internal.Unit %temp10
    
}

define i32 @func5(%Counter %param1){
entry:
    %prm1 = alloca %Counter
    store %Counter %param1, ptr %prm1
    %temp1 = load %Counter, ptr %prm1
    %temp4 = getelementptr %Counter, ptr %prm1, i32 0, i32 0
    %temp3 = load i32, ptr %temp4
    ret i32 %temp3
    
}

define %Counter @func6(%Counter %param1){
entry:
    %prm1 = alloca %Counter
    store %Counter %param1, ptr %prm1
    %temp1 = load %Counter, ptr %prm1
    %temp4 = getelementptr %Counter, ptr %prm1, i32 0, i32 0
    %temp3 = load i32, ptr %temp4
    %temp5 = add i32 %temp3, 10
    store i32 %temp5, ptr %temp4
    %temp7 = freeze %Internal.Unit zeroinitializer
    %temp8 = load %Counter, ptr %prm1
    ret %Counter %temp8
    
}

define i32 @main(){
    call %Internal.Unit @rx_source_main()
    ret i32 0
    
}

