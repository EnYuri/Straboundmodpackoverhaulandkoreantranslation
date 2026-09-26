import struct, sys, io

def rvu(f):
    v=0
    while True:
        b=f.read(1)[0]
        v=(v<<7)|(b&0x7f)
        if not b&0x80: return v

def rvi(f):
    v=rvu(f)
    return -((v>>1)+1) if v&1 else v>>1

def rstr(f):
    n=rvu(f)
    return f.read(n).decode('utf-8','replace')

def rjson(f):
    t=f.read(1)[0]
    if t==1: return None
    if t==2: return struct.unpack('>d',f.read(8))[0]
    if t==3: return f.read(1)[0]!=0
    if t==4: return rvi(f)
    if t==5: return rstr(f)
    if t==6: return [rjson(f) for _ in range(rvu(f))]
    if t==7: return {rstr(f):rjson(f) for _ in range(rvu(f))}
    raise ValueError('bad json type %d'%t)

class Pak:
    def __init__(self,path):
        self.f=open(path,'rb')
        assert self.f.read(8)==b'SBAsset6', path
        off=struct.unpack('>Q',self.f.read(8))[0]
        self.f.seek(off)
        assert self.f.read(5)==b'INDEX'
        self.meta={rstr(self.f):rjson(self.f) for _ in range(rvu(self.f))}
        n=rvu(self.f)
        self.index={}
        for _ in range(n):
            p=rstr(self.f)
            o,l=struct.unpack('>QQ',self.f.read(16))
            self.index[p]=(o,l)
    def read(self,p):
        o,l=self.index[p]
        self.f.seek(o)
        return self.f.read(l)

if __name__=='__main__':
    pk=Pak(sys.argv[1])
    pat=sys.argv[2] if len(sys.argv)>2 else ''
    print('META:', pk.meta.get('name'), pk.meta.get('version'), pk.meta.get('friendlyName'))
    for p in sorted(pk.index):
        if pat.lower() in p.lower(): print(p)
