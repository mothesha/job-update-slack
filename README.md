# DV Job Radar → Slack

A production-minded daily search for **Design Verification (DV)** roles. It checks public job feeds, applies relevance and freshness filters, deduplicates openings, and sends a clean Slack digest—without a server or paid service.

## Why automation instead of a website?

A website needs hosting, storage, authentication, and a browser visit. A scheduled GitHub Action runs unattended and delivers results where you already work. This implementation runs every day at 13:15 UTC.

## Highlights

- Searches Arbeitnow and Remotive public feeds daily
- Configurable keywords, exclusions, locations, age, and digest size
- Persistent deduplication: the same opening is never sent twice
- Slack digest includes role, company, location, source, date, and direct link
- One unavailable provider does not stop results from the other
- Manual dry runs; no third-party Python dependencies

## Setup

1. In Slack, create an app, enable **Incoming Webhooks**, add a webhook to the desired channel, and copy its URL.
2. In GitHub, open **Settings → Secrets and variables → Actions → New repository secret**. Name it SLACK_WEBHOOK_URL and paste the URL.
3. Edit config.json to tune the search. An empty locations list accepts all locations.
4. Open **Actions → Daily DV job search → Run workflow**. First select dry-run to inspect results without posting; then run normally.

GitHub schedules use UTC and may be delayed during busy periods. Edit the cron expression in .github/workflows/daily-jobs.yml to change the time.

## Configuration

| Field | Purpose |
| --- | --- |
| keywords | Require at least one phrase in the title or description |
| exclude_keywords | Reject results containing any phrase |
| locations | Optional case-insensitive location allowlist |
| max_age_days | Ignore older dated postings |
| max_notifications | Maximum roles per Slack digest (20 recommended) |
| sources | Enable or disable providers |

“All over the internet” cannot literally be crawled reliably or legally. This project uses public feeds and is extensible: add a fetcher in job_alert/sources.py, register it in SOURCES, then enable it in config.json.

## Local use

Python 3.10 or newer is the only requirement.

    python -m unittest discover -s tests -v
    python -m job_alert --dry-run
    SLACK_WEBHOOK_URL='https://hooks.slack.com/services/…' python -m job_alert

The normal command updates data/state.json only after Slack succeeds, so failed messages are not marked as delivered. Never commit the webhook URL.

## Security

- The webhook is read only from an environment variable or GitHub encrypted secret.
- HTTPS requests have explicit timeouts and a descriptive user agent.
- The workflow has only the repository permission required to persist its deduplication history.
- Revoke and replace a webhook immediately if it is exposed.
