"""Apply tracked existing-patch corrections without changing other pak assets.

Run after rebuilding the translation paks. Original metadata, asset names,
and unmodified bytes are preserved. Starbound and test servers must be closed.
"""
from pathlib import Path
import json, os, struct, subprocess, sys
from pak import Pak

REPO = Path(__file__).resolve().parents[1]

def vlq(value):
    parts = [value & 127]
    while value >> 7:
        value >>= 7
        parts.append(value & 127)
    return bytes(p | (128 if i else 0) for i,p in reversed(list(enumerate(parts))))

def string(value):
    data=value.encode('utf8')
    return vlq(len(data))+data

def value(data):
    if data is None:return b'\x01'
    if isinstance(data,bool):return b'\x03'+bytes([int(data)])
    if isinstance(data,float):return b'\x02'+struct.pack('>d',data)
    if isinstance(data,int):return b'\x04'+vlq(data<<1 if data>=0 else ((-data-1)<<1)|1)
    if isinstance(data,str):return b'\x05'+string(data)
    if isinstance(data,list):return b'\x06'+vlq(len(data))+b''.join(value(x) for x in data)
    if isinstance(data,dict):return b'\x07'+vlq(len(data))+b''.join(string(k)+value(v) for k,v in data.items())
    raise TypeError(type(data))

def main():
    star=Path(sys.argv[1]) if len(sys.argv)>1 else Path('E:/My Games/steamapps/common/Starbound')
    if os.name=='nt':
        running=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-Process -Name starbound,starbound_server -ErrorAction SilentlyContinue).Count"],capture_output=True,text=True,check=True)
        if int(running.stdout.strip()):raise RuntimeError('Close Starbound and its server before replacing active paks.')
    overrides=REPO/'compat_patch_overrides'
    for folder in sorted(p for p in overrides.iterdir() if p.is_dir()):
        target=star/'mods'/folder.name
        pak=Pak(target)
        replacements={'/'+str(f.relative_to(folder)).replace('\\','/'):f.read_bytes() for f in folder.rglob('*') if f.is_file()}
        if not replacements.keys() <= pak.index.keys():raise ValueError('Override is not an existing asset: '+folder.name)
        temporary=target.with_suffix('.pak.new')
        with temporary.open('wb') as out:
            out.write(b'SBAsset6'+bytes(8))
            index=[]
            for name in sorted(pak.index):
                data=replacements[name] if name in replacements else pak.read(name)
                index.append((name,out.tell(),len(data)))
                out.write(data)
            offset=out.tell()
            out.write(b'INDEX'+vlq(len(pak.meta))+b''.join(string(k)+value(v) for k,v in pak.meta.items()))
            out.write(vlq(len(index)))
            for name,pos,size in index:out.write(string(name)+struct.pack('>QQ',pos,size))
            out.seek(8);out.write(struct.pack('>Q',offset))
        result=Pak(temporary)
        assert result.meta==pak.meta and result.index.keys()==pak.index.keys()
        for name in pak.index:
            assert result.read(name)==(replacements[name] if name in replacements else pak.read(name)),name
        result.f.close();pak.f.close()
        os.replace(temporary,target)
        print(f'{folder.name}: {len(replacements)} patch corrections; other assets and metadata unchanged')

if __name__=='__main__':main()
