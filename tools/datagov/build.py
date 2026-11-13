import json,re,collections,os,html
D='2026-11-13'
reg=json.load(open('dg/reg.json'));std=json.load(open('dg/std.json'));orders=json.load(open('dg/orders.json'))
def url(h):
    m=re.search(r'href="([^"]+)"',h or ''); return html.unescape(m.group(1)).replace(' ','_') if m else ''
def d(s): return (s or '')[:10]
KEY=re.compile('בטיחות|גיהות|פיקוח על העבודה|חומרים מסוכנים|כבאות|חשמל|קרינה|מעבדות|עזרה ראשונה|ציוד מגן|עגורנ|רעש|אבק|אסבסט')
sel=[r for r in reg if 'משרד העבודה' in (r['office_name'] or '') or KEY.search(r['legislation_name'] or '')]
sel.sort(key=lambda r:(r['legislation_type']!='חקיקה ראשית', r['legislation_name'] or ''))
def regline(r):
    p=[r['legislation_name'].strip(), r['legislation_type'], 'משרד אחראי: '+(r['office_name'] or '').strip()]
    if r.get('primary_authorizing_legislation'): p.append('מכוח: '+r['primary_authorizing_legislation'].strip())
    if d(r.get('publication_date')): p.append('פורסם: '+d(r['publication_date']))
    if d(r.get('last_update')): p.append('עדכון אחרון: '+d(r['last_update']))
    u=url(r.get('wikiurl'))
    if u: p.append('נוסח מלא: '+u)
    return ' | '.join(p)
docs=[]
def add(id,title,source,intro,lines,maxc=95000):
    part=1;buf=[];n=len(intro)
    def flush():
        nonlocal part,buf,n
        if not buf: return
        t=title+(' (חלק %d)'%part if part>1 or more else '')
        docs.append({'id':id+('-%d'%part if part>1 or more else ''),'title':t,'source':source,'text':intro+'\n\n'+'\n\n'.join(buf)})
        part+=1;buf=[];n=len(intro)
    more=sum(len(l)+2 for l in lines)+len(intro)>maxc
    for l in lines:
        if n+len(l)+2>maxc: flush()
        buf.append(l);n+=len(l)+2
    flush()
add('gov-legislation-index','מפתח חקיקת בטיחות וגיהות (מאגר האסדרה)','data.gov.il, מאגר האסדרה של רשות האסדרה, עדכון המאגר 30.06.2025, נמשך '+D,
    'מפתח של חוקים, פקודות, תקנות וצווים בתחומי הבטיחות, הגיהות והפיקוח על העבודה. זהו מפתח בלבד: שם החיקוק, סוגו, החוק המסמיך, תאריכים וקישור לנוסח המלא. הוא אינו כולל את לשון הסעיפים.',
    [regline(r) for r in sel])
def stdline(s):
    p=[s['standard_number_and_name'].strip(),'מהדורה: '+(s['standard_edition'] or ''),'תוקף: '+(s['validity_from'] or '')]
    if s.get('mandatory_sections'): p.append('סעיפים רשמיים (מחייבים): '+re.sub(r'\s+',' ',s['mandatory_sections'])[:160])
    if s.get('amendments') and s['amendments']!='אין': p.append('גיליונות תיקון: '+re.sub(r'\s+',' ',s['amendments'])[:120])
    if s.get('standard_name_en'): p.append((s.get('standard_number_en') or '')+' '+s['standard_name_en'])
    return ' | '.join(p)
add('gov-official-standards','מאגר התקנים הרשמיים (תקנים ישראליים מחייבים)','data.gov.il, מאגר תקנים רשמיים, משרד הכלכלה והתעשייה, נמשך '+D,
    'רשימת התקנים הישראליים שהוכרזו רשמיים (מחייבים). זו רשימה בלבד: מספר התקן, שמו, מהדורה, תוקף והסעיפים המחייבים. לשון התקנים עצמם אינה כלולה; היא מוגנת בזכויות יוצרים של מכון התקנים הישראלי.',
    [stdline(s) for s in std])
c=collections.Counter()
for o in orders:
    if o['law_name'] or o['clause_name'] or o['felony_name']:
        c[(o['law_name'].strip(),re.sub(r'\s+',' ',o['clause_name'] or '').strip(),re.sub(r'\s+',' ',o['felony_name'] or '').strip())]+=1
cats=collections.Counter(o['category_name'] for o in orders)
lines=['%s | סעיף: %s | הליקוי: %s | מספר צווים: %d'%(a or 'לא צוין חיקוק',b or 'לא צוין',f or 'לא צוין',n) for (a,b,f),n in c.most_common(350)]
add('gov-safety-orders-summary','ליקויי בטיחות נפוצים בצווי בטיחות (סיכום)','data.gov.il, רשימת צווי בטיחות, משרד העבודה, נמשך '+D,
    'סיכום סטטיסטי של %d צווי בטיחות שהטילו מפקחי מינהל הבטיחות: אילו חיקוקים וסעיפים הופרו ומה היה הליקוי, לפי שכיחות. הסיכום אינו כולל שמות של אתרים, מבצעים או חברות. פילוח לפי ענף: %s.'%(len(orders),', '.join('%s %d'%(k or 'לא צוין',v) for k,v in cats.most_common(8))),
    lines)
os.makedirs('kbout',exist_ok=True)
for x in docs:
    x['createdAt']=D+'T00:00:00.000Z'
    json.dump({k:x[k] for k in ['title','source','text','createdAt']},open('kbout/%s.json'%x['id'],'w'),ensure_ascii=False)
    open('kbout/%s.md'%x['id'],'w').write('# '+x['title']+'\n\nמקור: '+x['source']+'\n\n'+x['text']+'\n')
    print(x['id'],'|',x['title'],'|',len(x['text']),'chars |',len(json.dumps(x,ensure_ascii=False).encode()),'bytes')
print('selected legislation rows',len(sel)); print(sel and regline([r for r in sel if 'ציוד מגן' in r['legislation_name']][0])); print(lines[0]); print(stdline(std[5]))
