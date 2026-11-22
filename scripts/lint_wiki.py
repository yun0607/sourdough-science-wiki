#!/usr/bin/env python3
"""Offline structural and citation validation; does not validate scientific truth."""
import argparse, json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CATEGORIES=['酸種麵包的基本原理','酸種酵母的培養與餵養','麵粉與發酵條件','酸種麵包的完整製作','常見問題與失敗原因','營養、健康與食品安全']
EXPECTED={f'SRC-{i:03}' for i in range(1,8)}
ALLOWED={'pending','ingested','approved','blocked','needs_human_review'}

def check(min_approved=0,strict=False):
 errors=[];warnings=[]
 try: sources=json.loads((ROOT/'sources.json').read_text(encoding='utf-8'))
 except (OSError,ValueError) as exc:
  print('FAIL: cannot load sources.json:',exc); return 1
 if not isinstance(sources,list):
  print('FAIL: sources.json must be an array');return 1
 source_by_id={}; urls=set();raws=set()
 for s in sources:
  if not isinstance(s,dict): errors.append('source record not object');continue
  sid=s.get('source_id');url=s.get('url');status=s.get('status')
  if not re.fullmatch(r'SRC-\d{3}',str(sid)):errors.append(f'invalid source ID: {sid}')
  if sid in source_by_id: errors.append(f'duplicate source ID: {sid}')
  source_by_id[sid]=s
  if not isinstance(url,str) or not url.startswith('https://'):errors.append(f'{sid}: invalid url')
  if url in urls:errors.append(f'{sid}: duplicate URL')
  urls.add(url)
  if status not in ALLOWED:errors.append(f'{sid}: invalid status')
  if not s.get('title'):errors.append(f'{sid}: missing title')
  if not isinstance(s.get('topics'),list) or not set(s.get('topics',[])).issubset(set(CATEGORIES)):
   errors.append(f'{sid}: invalid topics')
  if status in ('ingested','approved'):
   if not isinstance(s.get('authors'),list) or not s['authors']:errors.append(f'{sid}: no verified authors')
   if not s.get('accessed_on'): errors.append(f'{sid}: no accessed_on')
   if not s.get('license') or s.get('license')=='待檢查原文授權':errors.append(f'{sid}: license not checked')
   rp=s.get('raw_path')
   if not isinstance(rp,str) or not rp.startswith('raw/') or '..' in Path(rp).parts:errors.append(f'{sid}: invalid raw_path')
   elif not (ROOT/rp).is_file():errors.append(f'{sid}: raw file missing: {rp}')
   if rp in raws:errors.append(f'{sid}: duplicate raw_path')
   raws.add(rp)
 if set(source_by_id)!=EXPECTED:errors.append('expected exactly SRC-001..SRC-007')
 articles=list((ROOT/'wiki/articles').glob('W*.md'))
 approved_articles=[];seen_articles=set();cited=set();covered=set()
 for path in articles:
  content=path.read_text(encoding='utf-8')
  m=re.match(r'\A---\s*\n(.*?)\n---\s*\n',content,re.S)
  if not m:errors.append(f'{path.name}: missing frontmatter');continue
  fields={}
  for ln in m.group(1).splitlines():
   if ':' in ln:
    k,v=ln.split(':',1);fields[k.strip()]=v.strip()
  aid=fields.get('article_id');category=fields.get('category');state=fields.get('status')
  if not re.fullmatch(r'W\d{3}',str(aid)) or not path.name.startswith(str(aid)+'-'):errors.append(f'{path.name}: invalid article id/filename')
  if aid in seen_articles:errors.append(f'duplicate article ID: {aid}')
  seen_articles.add(aid)
  if category not in CATEGORIES:errors.append(f'{path.name}: invalid category')
  if state not in ('draft','approved','blocked','needs_human_review'):errors.append(f'{path.name}: invalid status')
  sm=re.fullmatch(r'\[(.*?)\]',fields.get('source_ids',''))
  sids=[x.strip() for x in sm.group(1).split(',') if x.strip()] if sm else []
  if not sids: errors.append(f'{path.name}: no source IDs')
  if len(sids)!=len(set(sids)):errors.append(f'{path.name}: duplicate source reference')
  for sid in sids:
   if sid not in source_by_id:errors.append(f'{path.name}: unknown source {sid}')
  body=content[m.end():]
  for pattern,label in [(r'^# .+', 'title'),(r'^\*\*摘要：\*\* .+','summary'),(r'^\*\*關鍵字：\*\* .+','keywords'),(r'^## 正文\s*$','body'),(r'^## 研究限制與不確定性\s*$','limitations'),(r'^## 來源\s*$','references')]:
   if not re.search(pattern,body,re.M): errors.append(f'{path.name}: missing {label}')
  if state=='approved':
   approved_articles.append((path,aid,category))
   covered.add(category);cited.update(sids)
   for sid in sids:
    if source_by_id.get(sid,{}).get('status')!='approved':errors.append(f'{path.name}: cites nonapproved {sid}')
   refs=set(re.findall(r'\[(SRC-\d{3})\]',body))
   if not set(sids).issubset(refs):errors.append(f'{path.name}: source not cited in body')
   main=body.split('## 來源')[0]
   for paragraph in re.split(r'\n\s*\n',main):
    para=paragraph.strip()
    if para and not para.startswith(('#','**關鍵字：**')) and not re.search(r'\[SRC-\d{3}\]',para):
     errors.append(f'{path.name}: paragraph missing citation: {para[:45]}')
 index=(ROOT/'wiki/index.md').read_text(encoding='utf-8')
 links=re.findall(r'^- (W\d{3}) \[[^\]]+\]\((articles/[^)]+)\)',index,re.M)
 linked_ids=[a for a,_ in links]
 if len(linked_ids)!=len(set(linked_ids)):errors.append('index: duplicate article ID')
 if set(linked_ids)!={a for _,a,_ in approved_articles}:errors.append('index does not match approved articles')
 for aid,path in links:
  if not (ROOT/'wiki'/path).exists():errors.append(f'index broken article path: {path}')
 approved_sources={k for k,v in source_by_id.items() if v.get('status')=='approved'}
 if min_approved and len(approved_sources)<min_approved:errors.append(f'approved sources {len(approved_sources)}/{min_approved}')
 if min_approved and len(approved_sources&cited)<min_approved:errors.append(f'cited approved sources {len(approved_sources&cited)}/{min_approved}')
 if min_approved==2 and not {'SRC-001','SRC-004'}.issubset(approved_sources&cited):errors.append('first batch SRC-001 and SRC-004 must both be approved and cited')
 if strict:
  if approved_sources!=EXPECTED:errors.append('strict requires all 7 sources approved')
  if covered!=set(CATEGORIES):errors.append('strict requires all 6 Wiki topics covered')
  if cited!=EXPECTED:errors.append('strict requires every source cited by approved articles')
 if not articles: warnings.append('no Wiki articles yet (project scaffold)')
 if not approved_sources:warnings.append('0 sources approved; no ingest has been performed')
 print('Sourdough Wiki Lint | '+('strict' if strict else f'min_sources={min_approved}'))
 print(f'Sources: {len(source_by_id)} | Approved sources: {len(approved_sources)} | Articles: {len(articles)} | Approved articles: {len(approved_articles)} | Topics: {len(covered)}/{len(CATEGORIES)}')
 for w in warnings:print('WARNING:',w)
 for e in errors:print('ERROR:',e)
 print('RESULT:', 'FAIL' if errors else 'PASS',f'({len(errors)} errors, {len(warnings)} warnings)')
 return 1 if errors else 0
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');p.add_argument('--min-approved-sources',type=int,default=0)
 a=p.parse_args()
 if a.min_approved_sources<0:p.error('min approved sources must be >= 0')
 sys.exit(check(min_approved=max(7 if a.strict else 0,a.min_approved_sources),strict=a.strict))
