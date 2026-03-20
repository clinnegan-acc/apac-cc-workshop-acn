# Current State Discovery
**Author:** Architect
**Reviewed with:** Project Manager, Developer, Data Engineer
**Date:** 2026-03-20
**Status:** Confirmed — do not migrate anything until this document is signed off

---

## Overview

Three workloads. None of them are clean. This document captures what is actually running, not what the runbooks say is running. Everything below was found by reading configs, tracing process trees, and asking the one developer who has been here since 2019.

---

## Workload 1 — Customer-Facing Web App

**Runtime:** Python Flask, single process, served via `gunicorn` on port `8080`
**Host:** `app-prod-01` (bare metal, on-prem DC)
**Database:** SQLite at `/var/app/data/inventory.db`
**Session storage:** Filesystem — sessions written to `/var/app/sessions/`

### Config (actual, not documented)

```
FLASK_ENV=production
DB_PATH=/var/app/data/inventory.db
SESSION_DIR=/var/app/sessions
REPORT_HOST=10.0.1.45        # ← hardcoded IP. This is the reporting DB host.
REPORT_PORT=5432             # ← direct Postgres connection to the reporting schema
SECRET_KEY=contoso2019!      # ← hardcoded in app.py, line 12. Not in env.
```

### Undocumented dependency

The web app has a `/dashboard` route that does a **live read directly against the reporting database** at `10.0.1.45:5432`. It joins `reporting.monthly_summary` with the app's own `inventory` table in a single query. This is not in any architecture doc. The Data Engineer found it at 11pm during a previous incident.

```python
# app.py — line 214 (nobody told the Architect this existed)
conn = psycopg2.connect(host="10.0.1.45", port=5432, dbname="reporting", user="app_ro")
```

**Migration blocker:** If we move the web app before the reporting DB, the `/dashboard` route breaks silently — it catches the exception and returns an empty chart. No alert fires. Users just see no data.

---

## Workload 2 — Nightly Batch Reconciliation Job

**Runtime:** Python script, triggered by `cron` at `02:00 AEST`
**Host:** `batch-prod-01` (separate bare metal box)
**Input:** Reads transaction CSVs from a **shared NFS mount** at `/mnt/findata/incoming/`
**Output:** Writes reconciled results back to `/mnt/findata/processed/` AND directly inserts into `reporting.reconciliation_runs`

### Config (actual)

```
CRON=0 2 * * *
INPUT_DIR=/mnt/findata/incoming/
OUTPUT_DIR=/mnt/findata/processed/
DB_HOST=10.0.1.45            # ← same hardcoded IP as the web app
DB_NAME=reporting
DB_USER=batch_rw
DB_PASS=Rec0nc!le99          # ← plaintext in /etc/cron.d/reconcile.conf
NFS_MOUNT=//fileserver-01/findata
```

### Undocumented dependency

The batch job does **not** write to its own schema. It writes directly into `reporting.reconciliation_runs` — the same table the reporting DB exposes to five internal teams. There is no staging table, no transaction wrapper, no lock. If the job fails mid-run, partial data sits in the reporting schema until someone manually deletes it.

There is also a **secondary cron** on `app-prod-01` that runs at `02:45 AEST` and reads `/mnt/findata/processed/` to update a `last_reconciled_at` timestamp in the app's SQLite DB. This is not in the batch job docs. The Developer found it while grepping for the NFS mount path.

```bash
# /etc/cron.d/sync_reconcile on app-prod-01 — undocumented
45 2 * * * app_user python /var/app/scripts/sync_last_reconciled.py
```

**Migration blocker:** The shared NFS mount is the connective tissue between all three workloads. It cannot be removed until both the batch job and the web app sync script are rewritten to use object storage (MinIO/S3).

---

## Workload 3 — Reporting Database

**Runtime:** PostgreSQL 11.8, self-managed
**Host:** `db-prod-01` at `10.0.1.45` (yes, the hardcoded IP above)
**Storage:** Attached SAN volume, `/data/pgdata/`
**Consumers:** 5 internal teams + the web app + the batch job = **7 active connections minimum**

### Schema surface (relevant tables)

```
reporting.monthly_summary         ← read by web app /dashboard (live, no cache)
reporting.reconciliation_runs     ← written by batch job (no staging, no lock)
reporting.team_snapshots          ← read by 5 internal teams via shared read-only user
reporting.audit_log               ← append-only, written by a trigger on reconciliation_runs
```

### Undocumented dependency

There is a **PostgreSQL trigger** on `reconciliation_runs` that appends to `audit_log` on every insert. Nobody documented this. It means the batch job is implicitly writing to two tables, and any migration of `reconciliation_runs` must carry the trigger or audit records will silently stop being created. Compliance will care about this.

The five internal teams all connect using the **same read-only credential** (`reporting_ro` / `R3port!ng2020`). There is no connection pooling. On month-end, concurrent connections spike to ~40 and the DB slows enough that the batch job has missed its 02:00 window three times this year.

---

## Dependency Map (What Talks to What)

```
                    ┌─────────────────────┐
                    │   NFS Fileserver     │
                    │  //fileserver-01     │
                    │  /mnt/findata/       │
                    └──────┬──────┬────────┘
                           │      │
                    writes │      │ reads
                           ▼      ▼
              ┌──────────────┐  ┌───────────────────┐
              │  Batch Job   │  │   Web App          │
              │  batch-prod  │  │   app-prod-01:8080 │
              │  cron 02:00  │  │   (Flask/gunicorn) │
              └──────┬───────┘  └────────┬───────────┘
                     │                   │
          direct DB  │                   │ direct DB
          INSERT      │                   │ SELECT (hardcoded IP)
                     ▼                   ▼
              ┌──────────────────────────────────┐
              │       Reporting DB               │
              │       db-prod-01 / 10.0.1.45     │
              │       PostgreSQL 11.8            │
              │                                  │
              │  reporting.reconciliation_runs   │◄── trigger → audit_log
              │  reporting.monthly_summary       │
              │  reporting.team_snapshots        │
              └──────────────────────────────────┘
                           ▲
                           │ concurrent reads (~40 on month-end)
                    5 internal teams (shared credential)
```

---

## Migration Risk Register

| Risk | Severity | Owner | Notes |
|------|----------|-------|-------|
| Hardcoded IP `10.0.1.45` in web app and batch job | High | Developer + Data Engineer | Must be replaced with service DNS before cutover |
| `/dashboard` route reads reporting DB directly | High | Developer | Silent failure if reporting DB unreachable — needs Redis cache or dedicated API endpoint |
| Batch job writes directly to `reporting` schema | High | Data Engineer | Needs staging table + transaction wrapper before re-platform |
| PostgreSQL trigger on `reconciliation_runs` | Medium | Data Engineer | Must be carried to new DB — compliance dependency |
| Shared NFS mount between all three workloads | High | Architect | Replaced by MinIO — both consumers must be rewritten simultaneously |
| Shared read-only credential for 5 teams | Medium | Architect + Data Engineer | Replace with per-team credentials and connection pooler (PgBouncer) |
| `SECRET_KEY` hardcoded in `app.py` | Medium | Developer | Move to environment variable before containerisation |
| Plaintext `DB_PASS` in `/etc/cron.d/` | High | Data Engineer | Move to secrets manager or environment injection |
| Undocumented `sync_last_reconciled.py` cron on app server | Medium | Developer | Must be rewritten as a MinIO event or scheduled task |

---

## What Needs to Happen Before Anyone Writes a Dockerfile

1. **Architect** locks the Docker Compose service topology and defines internal DNS names to replace `10.0.1.45`
2. **Data Engineer** audits the full `reporting` schema and confirms all triggers and dependencies before PostgreSQL migration
3. **Developer** isolates the `/dashboard` route and confirms the silent failure behaviour with a test
4. **PM** updates the risk register above and confirms cutover sequencing — reporting DB must move before or simultaneously with the web app, not after

Discovery is done. The picture is not pretty. We migrate it anyway.
