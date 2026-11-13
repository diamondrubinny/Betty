import json,re,html,urllib.request,urllib.parse,os,time
D='2026-11-13'
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (compatible; research-client)'}),timeout=90) as r: return json.load(r)
reg=json.load(open('dg/reg.json'))
def url(h):
    m=re.search(r'href="([^"]+)"',h or ''); return html.unescape(m.group(1)) if m else ''
KEYS=['פקודת הבטיחות בעבודה [נוסח חדש]','חוק ארגון הפיקוח על העבודה','ציוד מגן אישי','מסירת מידע והדרכת עובדים','עבודה בגובה','עזרה ראשונה במקומות עבודה',
 'במעבדות רפואיות','ממונים על הבטיחות','תכנית לניהול הבטיחות','גיליון בטיחות','(חשמל)','ועדות בטיחות','נאמני בטיחות','ניטור סביבתי','(רעש)','קרינה מייננת','לייזר','נוחות',
 'גיהות תעסוקתית ובריאות העובדים בממסים','אבק מזיק','עגורנאים','בדיקות רפואיות','הודעה על מינוי','תאונות ומחלות משלח יד','אסבסט','בנזן','מתכות מסוימות','כלי הרמה','מלגזות']
cand=[]
for r in reg:
    n=(r['legislation_name'] or '').strip(); u=url(r.get('wikiurl'))
    if not u or 'wikisource' not in u: continue
    if 'עבודה' not in (r['office_name'] or '') and 'בטיחות' not in n: continue
    if any(k in n for k in KEYS) and 'תיקון' not in n and '1946' not in n and 'ביטול' not in n and 'הוראת שעה' not in n: cand.append((n,u))
seen=set();cand=[c for c in cand if not (c[1] in seen or seen.add(c[1]))]
print(len(cand))
def totext(h):
    h=re.sub(r'(?s)<(style|script)[^>]*>.*?</\1>','',h)
    h=re.sub(r'(?s)<span class="printonly">.*?</span></span></span>','',h)
    h=re.sub(r'(?s)<sup[^>]*class="[^"]*reference[^"]*".*?</sup>','',h)
    h=re.sub(r'(?i)<(br|/p|/div|/h\d|/li|/tr|/table|/dd|/dt)[^>]*>','\n',h)
    h=re.sub(r'(?i)</t[dh]>',' ',h)
    t=html.unescape(re.sub(r'<[^>]+>','',h)).replace('\xa0',' ')
    t=re.sub(r'[ \t]+',' ',t); t=re.sub(r' *\n *','\n',t); t=re.sub(r'\n{2,}','\n',t).strip()
    return t
os.makedirs('ws',exist_ok=True)
out=json.load(open('ws/laws.json')) if os.path.exists('ws/laws.json') else []
have={o['name'] for o in out}
for n,u in cand:
    if n in have: continue
    page=urllib.parse.unquote(u.split('/wiki/')[1])
    for attempt in range(4):
        try:
            r=get('https://he.wikisource.org/w/api.php?action=parse&format=json&prop=text|revid&redirects=1&maxlag=5&page='+urllib.parse.quote(page))
            t=totext(r['parse']['text']['*']); title=r['parse']['title']
            out.append({'name':n,'page':title,'url':'https://he.wikisource.org/wiki/'+title.replace(' ','_'),'revid':r['parse'].get('revid'),'text':t})
            print(len(t),'|',n,flush=True); break
        except Exception as e:
            print('retry',attempt,n[:40],str(e)[:60],flush=True); time.sleep(70*(attempt+1))
    json.dump(out,open('ws/laws.json','w'),ensure_ascii=False)
    time.sleep(45)
print('total',len(out),'of',len(cand))
