# Uptimer

A simple, reliable website and API uptime monitoring engine built with Python and Django.

I started this project because I wanted to step away from basic CRUD tutorials and build actual backend systems—focusing on things like network I/O, database relationships, logging historical metrics, and background task execution.

## What it does right now

At the moment, the core backend monitoring logic is working:
* **Monitor Management:** Stores monitored endpoints with custom check intervals and status tracking in the database.
* **Ping Engine:** An HTTP checker service that sends requests, handles network exceptions/timeouts cleanly, measures latency in milliseconds, and evaluates HTTP response codes.
* **Audit Logging:** Every check creates a timestamped `PingLog` entry linked via foreign keys, tracking response code, latency, success state, and failure tracebacks.
* **Status Updates:** Dynamically flips monitor state between `up` and `down` based on real response contracts.

## How it works (nerds shit)

1. A `Monitor` entry defines a target URL and how often it should be checked.
2. The `check_status` service pings the target using a strict timeout to prevent hanging connections.
3. Round-trip time is recorded in milliseconds. (im so smart)
4. If the connection fails, drops, or times out, the service catches the exception properly, flags the check as failed, and stores the raw error message rather than crashing the process.
5. The result is saved to an immutable historical log table (`PingLog`).

## Future Roadmap & Trajectory

- [ ] **Custom Management Command:** Add `python manage.py run_checks` to trigger checks for only the monitors that are actually due.
- [ ] **Background Scheduling & Concurrency:** Move checks away from synchronous execution by integrating Celery + Redis so hundreds of sites can be pinged in parallel without blocking.
- [ ] **Alerting Engine:** Add alert thresholds (e.g., alert only after 3 consecutive failures to avoid false alarms) with Discord or email webhooks.
- [ ] **Frontend Dashboard:** Wire up a clean UI (Google Stitch) to show active monitors, 24-hour latency charts, and uptime percentages.
- [ ] **Public Status Pages:** Generate simple, read-only incident status pages for monitored services.

## Why this exists

Built as a hands-on project to get deep into Django's ORM, learn how production backend systems handle failure states, and understand how to design scalable monitoring tools from scratch. Wanted to learn more than the e-commerce system and this was what I felt a very interesting project so :p
