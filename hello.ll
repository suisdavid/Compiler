@fmt = private constant [4 x i8] c"%d\0A\00"

declare i32 @printf(ptr, ...)

define i32 @main() {
entry:
    %answer = add i32 40, 2
    %ignored = call i32 (ptr, ...) @printf(ptr @fmt, i32 %answer)
    ret i32 0
}