import json,re,os,sys,hashlib
D='2026-11-13'
laws=json.load(open('ws/laws.json'))
skip=set(sys.argv[1:])
os.makedirs('kblaws',exist_ok=True);made=[]
def slug(i): return 'law-%02d'%i
names=sorted(l['name'] for l in laws)
for l in laws:
    t=re.sub(r'\n\[?תיקון: [^\n]*\]?','',l['text'])
    intro='נוסח לא רשמי מתוך ספר החוקים הפתוח (ויקיטקסט), גרסת עמוד %s. יש לאמת מול הנוסח הרשמי ברשומות לפני הסתמכות. קישור: %s'%(l.get('revid'),l['url'])
    parts=[t[k:k+90000] for k in range(0,len(t),90000)]
    for n,part in enumerate(parts,1):
        id='law-'+hashlib.md5(l['name'].encode()).hexdigest()[:8]+('-%d'%n if len(parts)>1 else '')
        title=l['name']+(' (חלק %d)'%n if len(parts)>1 else '')
        doc={'title':title[:150],'source':'נוסח לא רשמי, ויקיטקסט, נמשך '+D,'text':intro+'\n\n'+part,'createdAt':D+'T00:00:01.000Z'}
        json.dump(doc,open('kblaws/%s.json'%id,'w'),ensure_ascii=False)
        open('kblaws/%s.md'%id,'w').write('# '+title+'\n\n'+doc['text']+'\n')
        made.append(id)
print(json.dumps([{'op':'set','collection':'kb','doc_id':m,'file_path':os.path.abspath('kblaws/%s.json'%m)} for m in made if m not in skip]))
