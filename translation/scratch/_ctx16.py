import sys,io,csv
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
want=['inhibitordrone','v-toxicbubblespawner','v-corelightningspawner','toptophathead','samplesample','relicseekerdisplay2','deploywhistle','mooshiunripeAF','luftbrenner_endless','weather/longdescription','scanner/items.config']
for r in csv.DictReader(open('data/pak_pairs.tsv',encoding='utf-8-sig'),delimiter='\t'):
    for w in want:
        if w in r['asset'] or w in r['pointer']:
            print('===',r['asset'][-50:],'|',r['pointer'][-35:])
            print('  EN:',repr(r['english'])[:160])
            print('  KO:',repr(r['korean'])[:160])
            want.remove(w);break
