from datetime import datetime,timedelta,timezone
from pathlib import Path
import json,tempfile,unittest
from job_alert.core import matches,unseen,update_state
from job_alert.models import Job
from job_alert.slack import payload

class Tests(unittest.TestCase):
    def setUp(self):
        self.job=Job("Senior DV Engineer","Acme","Austin, TX","https://example.com/1","Test",datetime.now(timezone.utc))
        self.config={"keywords":["dv engineer"],"exclude_keywords":[],"locations":[],"max_age_days":14}
    def test_match(self): self.assertTrue(matches(self.job,self.config))
    def test_old_rejected(self):
        old=Job("DV Engineer","Acme","Remote","https://x","Test",datetime.now(timezone.utc)-timedelta(days=30))
        self.assertFalse(matches(old,self.config))
    def test_exclusion(self): self.assertFalse(matches(self.job,{**self.config,"exclude_keywords":["senior"]}))
    def test_seen(self): self.assertEqual([],unseen([self.job],{"seen":[self.job.id]}))
    def test_state(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"state.json"; update_state(path,[self.job],{})
            self.assertIn(self.job.id,json.loads(path.read_text())["seen"])
    def test_slack_payload(self):
        message=payload([self.job]); self.assertIn(self.job.url,json.dumps(message)); self.assertLessEqual(len(message["blocks"]),50)

if __name__=="__main__": unittest.main()
