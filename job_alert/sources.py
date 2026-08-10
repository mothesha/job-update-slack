import json
from urllib.request import Request, urlopen
from .models import Job, clean_html, parse_date

def fetch_json(url):
    request = Request(url, headers={"User-Agent":"DVJobAlert/1.0","Accept":"application/json"})
    with urlopen(request, timeout=20) as response:
        return json.load(response)

def fetch_arbeitnow():
    return [Job(i["title"], i.get("company_name","Unknown"), i.get("location","Not specified"), i["url"], "Arbeitnow", parse_date(i.get("created_at")), clean_html(i.get("description",""))) for i in fetch_json("https://www.arbeitnow.com/api/job-board-api").get("data",[]) if i.get("title") and i.get("url")]

def fetch_remotive():
    return [Job(i["title"], i.get("company_name","Unknown"), i.get("candidate_required_location","Remote"), i["url"], "Remotive", parse_date(i.get("publication_date")), clean_html(i.get("description",""))) for i in fetch_json("https://remotive.com/api/remote-jobs?limit=100").get("jobs",[]) if i.get("title") and i.get("url")]

SOURCES={"arbeitnow":fetch_arbeitnow,"remotive":fetch_remotive}
