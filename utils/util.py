#useful functions
from __future__ import annotations

class Util:
    def __init__(self):
        self.SIZE={"%Vec":12,"%Internal.Unit":0}
        self.OFFSETS={"%Vec":[0,4,8],"%Internal.Unit":[]}#structName(str) to list[int](field offsets)
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
        idx=len(type)-1
        while type[idx]!=';':
            idx-=1
        return self.GetIRType(type[1:idx]),int(type[idx+1:-1])

    def GetAllocSize(self,type:str)->int:
        if type.startswith("&") or type.startswith("Box<"):
            return 4
        elif type.startswith("Vec<"):
            return 12
        elif type=="()":
            return 0
        elif type in ["i32","u32","isize","usize"]:
            return 4
        elif type=="bool":
            return 1
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