#!/usr/bin/env python3
"""Mark ids as reviewed in style_worklist.tsv.
usage: python style_done.py DONE id1 id2 ... | python style_done.py OK id1 ..."""
import csv,io,sys
status=sys.argv[1]; ids=set(sys.argv[2:])
rows=list(csv.reader(open('style_worklist.tsv',encoding='utf-8-sig',newline=''),delimiter='\t'))
head,body=rows[0],rows[1:]
n=0
for r in body:
    if r[0] in ids: r[-1]=status; n+=1
out=io.StringIO(); w=csv.writer(out,delimiter='\t',lineterminator='\n')
w.writerow(head); w.writerows(body)
open('style_worklist.tsv','w',encoding='utf-8-sig',newline='').write(out.getvalue())
left=sum(1 for r in body if r[-1]=='TODO')
print(f'marked {n} as {status}; TODO left {left}')
