import argparse
import logging
import os
from pathlib import Path
from .core import collect,load_json,unseen,update_state
from .slack import send

def main(argv=None):
    parser=argparse.ArgumentParser(description="Find new Design Verification jobs and notify Slack.")
    parser.add_argument("--config",type=Path,default=Path("config.json"))
    parser.add_argument("--state",type=Path,default=Path("data/state.json"))
    parser.add_argument("--dry-run",action="store_true")
    args=parser.parse_args(argv); logging.basicConfig(level=logging.INFO,format="%(levelname)s %(message)s")
    config=load_json(args.config,{}); state=load_json(args.state,{"seen":[]})
    jobs,errors=collect(config); fresh=unseen(jobs,state)[:config.get("max_notifications",20)]
    for job in fresh: print(f"{job.title} | {job.company} | {job.location} | {job.url}")
    if args.dry_run: print(f"Dry run: {len(fresh)} new match(es); state unchanged."); return 0
    webhook=os.environ.get("SLACK_WEBHOOK_URL")
    if fresh and not webhook: logging.error("SLACK_WEBHOOK_URL is required."); return 2
    if fresh: send(webhook,fresh,errors); logging.info("Sent %d job(s).",len(fresh))
    else: logging.info("No new matching jobs; notification skipped.")
    update_state(args.state,jobs,state); return 0
