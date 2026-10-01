import sys,io,csv
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
want=[('naked.npctype','hylotl/default/62'),('naked.npctype','hylotl/default/63'),
('lawenforcementheadquarters01c','/shortdescription'),
('mfgstation','/description'),
('ffs_radiomessages_hc','ffs0_1_4_hc'),
('gic_scope_charm.statuseffect','/label'),
('neb-damagetypekills','/title'),
('gic_sawdustbread','/description'),
('plebiancap','/text'),
('10industrialcentrifuge','/text'),
('shoggoth_wagner','/text'),
('1boozekit','turnInDescription'),
('create_protocite','turnInDescription'),
('NNCSU','/description'),
('gic_plantfibresalad','/description'),
]
for r in csv.DictReader(open('data/pak_pairs.tsv',encoding='utf-8-sig'),delimiter='\t'):
    for a,p in want:
        if a in r['asset'] and p in r['pointer']:
            print('===',r['asset'][-48:],'|',r['pointer'][-45:])
            print('  EN:',repr(r['english'])[:300])
            print('  KO:',repr(r['korean'])[:300])
            want.remove((a,p));break
