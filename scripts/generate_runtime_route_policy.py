#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path


def normalize(p:str)->str:
    return p if p.startswith("Release/") else f"Release/{p}"


def item_text(item:dict)->str:
    file_path = item.get("file","")
    path = Path(file_path)
    text = " ".join([file_path, item.get("display_name",""), item.get("description","")])
    try:
        text += " " + " ".join(path.read_text(encoding="utf-8").splitlines()[:20])
    except Exception:
        pass
    return text.lower()


def best_owner(issue_type:str, roles:list[dict])->str:
    candidates=[]
    for item in roles:
        caps=set(item.get("capability_tags",[]))
        primary=set(item.get("primary_issue_types",[]))
        if issue_type not in caps and issue_type not in primary:
            continue
        kind=item.get("role_kind","owner")
        score=0
        if issue_type in primary:
            score += 100
        if issue_type in caps:
            score += 40
        score += 30 if kind=='owner' else 5
        text=item_text(item)
        if issue_type.lower() in text:
            score += 3
        candidates.append((score, normalize(item['file'])))
    return sorted(candidates, reverse=True)[0][1] if candidates else ""


def best_tools(issue_type:str, tools:list[dict], configured_count:int)->list[str]:
    scored=[]
    for item in tools:
        caps=set(item.get("capability_tags",[]))
        primary=set(item.get("primary_issue_types",[]))
        if issue_type not in caps and issue_type not in primary:
            continue
        score=0
        if issue_type in primary:
            score += 100
        if issue_type in caps:
            score += 40
        text=item_text(item)
        if issue_type.lower() in text:
            score += 2
        scored.append((score, normalize(item['file'])))
    scored=sorted(scored, reverse=True)
    configured_count=max(1, configured_count or 3)
    return [p for _,p in scored[:configured_count]]


def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',default='.'); ap.add_argument('--manifest',default='Release/MANIFEST.json'); ap.add_argument('--output',default='.hgs/generated_runtime_route_policy.json'); args=ap.parse_args()
    root=Path(args.repo_root).resolve(); manifest=json.loads((root/args.manifest).read_text(encoding='utf-8'))
    roles=[{**x,'file':normalize(x['file'])} for x in manifest.get('roles',[]) if isinstance(x,dict) and 'file' in x]
    tools=[{**x,'file':normalize(x['file'])} for x in manifest.get('tools',[]) if isinstance(x,dict) and 'file' in x]
    configured_route=manifest.get('automation_policy',{}).get('runtime_route_policy',{})
    supported=configured_route.get('supported_issue_types',[])
    owner_by={t:best_owner(t,roles) for t in supported}
    tools_by={t:best_tools(t,tools,len(configured_route.get('tools_by_issue_type',{}).get(t,[]))) for t in supported}
    data={'owner_by_issue_type':owner_by,'tools_by_issue_type':tools_by}
    out=root/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(data,ensure_ascii=False,indent=2)); return 0

if __name__=='__main__':
    raise SystemExit(main())
