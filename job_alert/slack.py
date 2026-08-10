import json
from urllib.request import Request, urlopen

def payload(jobs,errors=None):
    blocks=[{"type":"header","text":{"type":"plain_text","text":f"🔎 {len(jobs)} new DV job{'s' if len(jobs)!=1 else ''}"}},{"type":"context","elements":[{"type":"mrkdwn","text":"Fresh Design Verification openings matched by your daily search."}]},{"type":"divider"}]
    for job in jobs:
        date=job.published_at.strftime("%b %d") if job.published_at else "Date unavailable"
        blocks += [{"type":"section","text":{"type":"mrkdwn","text":f"*<{job.url}|{job.title}>*\n{job.company} · {job.location}"}},{"type":"context","elements":[{"type":"mrkdwn","text":f"{job.source} · {date}"}]}]
    if errors: blocks.append({"type":"context","elements":[{"type":"mrkdwn","text":"⚠️ Some sources failed: "+", ".join(errors)}]})
    return {"text":f"{len(jobs)} new Design Verification jobs","blocks":blocks}

def send(webhook,jobs,errors=None):
    req=Request(webhook,data=json.dumps(payload(jobs,errors)).encode(),headers={"Content-Type":"application/json"},method="POST")
    with urlopen(req,timeout=20) as response:
        if response.status>=300: raise RuntimeError(f"Slack returned HTTP {response.status}")
