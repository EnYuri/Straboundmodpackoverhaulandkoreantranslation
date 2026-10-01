import os, sys, time

mods = r"E:\My Games\steamapps\common\Starbound\mods"
tmp = os.path.join(mods, 'zz_translation_female.pak.tmp_write')
dst = os.path.join(mods, 'zz_translation_female.pak')
for i in range(8):
    try:
        os.replace(tmp, dst)
        print('installed')
        sys.exit(0)
    except OSError as e:
        print('try', i, e)
        time.sleep(3)
print('FAILED')
sys.exit(1)
