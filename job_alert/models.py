from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import re

def clean_html(value: str) -> str:
    return re.sub(r"\\s+", " ", re.sub(r"<[^>]+>", " ", value or "")).strip()

def parse_date(value):
    try:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, timezone.utc)
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except (ValueError, OSError, AttributeError):
        return None

@dataclass(frozen=True)
class Job:
    title: str
    company: str
    location: str
    url: str
    source: str
    published_at: datetime | None = None
    description: str = ""
    @property
    def id(self):
        return hashlib.sha256(f"{self.source}|{self.url}".lower().encode()).hexdigest()[:20]
