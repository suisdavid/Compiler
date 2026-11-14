#useful functions
from __future__ import annotations

class Util:
    def __init__(self):
        self.regNum=15
        self.paramNum=6
        self.SIZE={"%Vec":12,"%Internal.Unit":0}
        self.OFFSETS={"%Vec":[0,4,8],"%Internal.Unit":[]}#structName(str) to list[int](field offsets)
        self.useregs=['t0','t1','t2','s0','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','a2','a3','a4','a5','a6','a7']#a2-a7 are reserved for function params
        self.stack_offset_register='a0'
        self.memcpy_reserved='a1'
        self.tempregs=['t3','t4','t5','t6']
        self.regMap={"zero":0,"ra":1,"sp":2,"gp":3,"tp":4,"t0":5,"t1":6,"t2":7,"s0":8,"s1":9,"a0":10,"a1":11,"a2":12,"a3":13,"a4":14,"a5":15,"a6":16,"a7":17,"s2":18,"s3":19,"s4":20,"s5":21,"s6":22,"s7":23,"s8":24,"s9":25,"s10":26,"s11":27,"t3":28,"t4":29,"t5":30,"t6":31}
        
    def u32(self,x:int)->int:
        return x%(1<<32)
    
    def s32(self,x:int)->int:
        x%=(1<<32)
        return x if x<(1<<31) else (x-(1<<32))

    def prune1(self,s:str)->str:#one line
        return '    '+s.strip()+'\n'
    
    def prune(self,s:str)->str:
            lines=s.split('\n')
            t=''
            flag=0
            for i in range(len(lines)):
                lines[i]=lines[i].strip()
                if lines[i].endswith(":"):
                    t+=(f'    br label %{lines[i][:-1]}\n' if (not flag and not lines[i].startswith('entry') and not lines[i-1].startswith('br') and not lines[i-1]=='unreachable') else '')+lines[i]+'\n'
                    flag=0
                elif lines[i].startswith("define") or lines[i].startswith("{") or lines[i].startswith("}"):
                    t+=lines[i]+'\n'
                else:
                    if flag==0:
                        t+='    '+lines[i]+'\n'
                    if lines[i].startswith('ret'):
                        flag=1
            return t

    def GetIRType(self,type:str)->str:#replace all &mut with &
        return type.replace('&mut','&')

    def GetArrayInfo(self,type:str)->tuple[str,int]:#array innerType and length
        if ';' in type:
            idx=len(type)-1
            while type[idx]!=';':
                idx-=1
            return self.GetIRType(type[1:idx]),int(type[idx+1:-1])
        else:
            idx=type.index('x')
            return self.GetIRType(type[idx+1:-1]),int(type[1:idx])

    def GetAllocSize(self,type:str)->int:#everything is multiple of 4, easy to store in RISC_V
        if type.startswith("&") or type.startswith("Box<"):
            return 4
        elif type.startswith("Vec<"):
            return 12
        elif type in ["i32","u32","isize","usize","bool","()"]:
            return 4
        elif type=='^':
            return 0
        elif type.startswith("["):
            innerType,length=self.GetArrayInfo(type)
            return length*self.GetAllocSize(innerType)
        else:
            return self.SIZE[type]
        
    def GetFieldOffset(self,type:str,field_idx:int)->int:
        return self.OFFSETS[type][field_idx]
    
    def GetAllocType(self,type:str)->str:
        if type.startswith("&") or type.startswith("Box<"):
            return "ptr"
        elif type.startswith("Vec<"):
            return "%Vec"
        elif type=="()":
            return "%Internal.Unit"
        elif type in ["i32","u32","isize","usize"]:
            return "i32"
        elif type=="bool":
            return "i1"
        elif type=='^':
            return type
        elif type.startswith("["):
            innerType,length=self.GetArrayInfo(type)
            return f"[{length} x {self.GetAllocType(innerType)}]"
        else:
            return "%"+type
util=Util()