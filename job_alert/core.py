from datetime import datetime, timedelta, timezone
import json
import logging
from .sources import SOURCES

LOG=logging.getLogger(__name__)
def load_json(path, default):
    if not path.exists(): return default
    with path.open(encoding="utf-8") as handle: return json.load(handle)

def matches(job, config, now=None):
    now=now or datetime.now(timezone.utc)
    text=f"{job.title} {job.description}".lower()
    if not any(x.lower() in text for x in config["keywords"]): return False
    if any(x.lower() in text for x in config.get("exclude_keywords",[])): return False
    places=config.get("locations",[])
    if places and not any(x.lower() in job.location.lower() for x in places): return False
    return not job.published_at or job.published_at >= now-timedelta(days=config.get("max_age_days",14))

def collect(config):
    jobs=[]; errors=[]
    for name, enabled in config.get("sources",{}).items():
        if not enabled: continue
        try:
            jobs.extend(SOURCES[name]())
        except Exception as exc:
            LOG.warning("%s failed: %s",name,exc); errors.append(f"{name}: {exc}")
    unique={j.id:j for j in jobs if matches(j,config)}
    minimum=datetime.min.replace(tzinfo=timezone.utc)
    return sorted(unique.values(),key=lambda j:j.published_at or minimum,reverse=True),errors

def unseen(jobs,state):
    seen=set(state.get("seen",[])); return [j for j in jobs if j.id not in seen]

def update_state(path,jobs,previous):
    ids=[j.id for j in jobs]+previous.get("seen",[])
    state={"seen":list(dict.fromkeys(ids))[:5000],"updated_at":datetime.now(timezone.utc).isoformat()}
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(state,indent=2)+"\n")
