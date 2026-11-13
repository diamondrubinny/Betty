import json,urllib.request,collections
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (compatible; research-client)'}),timeout=120) as r: return json.load(r)
def allrows(rid):
    out=[];off=0
    while True:
        d=get('https://data.gov.il/api/3/action/datastore_search?limit=5000&offset=%d&resource_id=%s'%(off,rid))['result']
        out+=d['records']; off+=5000
        if off>=d['total'] or not d['records']: break
    return out
R={'reg':'929b4c60-ce43-4f5b-9960-f6146ba33eed','std':'1a4d94e2-369a-488d-a223-eb1020612fbd','orders':'264cec97-c8f8-496f-84e5-052a63fdea3f'}
for k,rid in R.items():
    rows=allrows(rid); json.dump(rows,open('dg/%s.json'%k,'w'),ensure_ascii=False); print(k,len(rows))
reg=json.load(open('dg/reg.json'))
print(collections.Counter(r['office_name'] for r in reg).most_common(40))
print(collections.Counter(r['legislation_type'] for r in reg).most_common(10))
print(json.dumps([r for r in reg if 'בטיחות בעבודה' in (r['legislation_name'] or '')][:3],ensure_ascii=False)[:1500])
std=json.load(open('dg/std.json')); print(json.dumps(std[0],ensure_ascii=False)[:1200])
o=json.load(open('dg/orders.json')); print(json.dumps(o[0],ensure_ascii=False)[:600])
print(collections.Counter(r['law_name'] for r in o).most_common(15))
