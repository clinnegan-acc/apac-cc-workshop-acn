# Migration Decision Memo
**From:** Project Manager
**To:** Architect, Developer, Data Engineer
**Re:** Contoso Financial — Cloud Migration Strategy
**Date:** 2026-03-20

---

## The Decision

**We lift-and-shift first. We refactor on the way out.**

The CFO has a contract to honour and a board to answer to. We are not going to blow the deadline chasing architectural purity. We move fast, we get off prem, and we modernise from a position of stability — not mid-flight.

---

## What This Means Per Workload

**Customer-facing web app (Developer)**
Rehost into a container behind Nginx. Swap the database connection string to PostgreSQL. That is the migration. Redis caching comes in immediately after — it is low-risk and the performance argument writes itself. We do not refactor the app logic during this window.

**Nightly batch reconciliation job (Data Engineer)**
Rehost as a containerised cron job targeting PostgreSQL. Output files go to MinIO. The job runs on a schedule, same as today. Event-driven refactor is on the backlog — it is the right long-term call, but it is not the right call this week.

**Reporting database (Data Engineer)**
Re-platform to PostgreSQL with a proper schema and seed data. This one gets the most modernisation love because the risk of getting it wrong compounds across five internal teams. Read-scaling notes go in the handover doc.

---

## The Case

The CTO is right that lift-and-shift is not the destination. The CFO is right that we cannot spend six months refactoring before a single workload is off prem. The answer is sequencing, not compromise. A running rehost beats a perfect refactor that never ships. We demonstrate cloud connectivity, we validate the architecture locally, and we hand over artifacts a real team can deploy. That satisfies the contract. The refactor roadmap satisfies the CTO.

---

## Risks We Are Accepting

- **Technical debt is real.** The batch job as a cron container is not cloud-native. We are knowingly deferring the event-driven pattern. This is logged, not forgotten.
- **No autoscaling on the web app.** Horizontal scaling is available via Docker Compose but not wired up in this phase. Single point of failure risk remains until the refactor.
- **MinIO is not S3.** The local simulation is faithful but not identical. SDK compatibility has been validated; edge cases in production will surface post-migration.

---

## What I Need From Each of You

| Role | Commitment |
|------|------------|
| **Architect** | `docker-compose.yml` locked before anyone writes application code. No moving the goalposts on service topology mid-build. |
| **Developer** | Web app running end-to-end through Nginx + Redis by the midpoint. No scope creep into refactoring. |
| **Data Engineer** | PostgreSQL schema and batch job output to MinIO confirmed working. Document the event-driven refactor path in your handover notes — the CTO will ask. |

---

We are building something a real team could deploy. That is the bar. Move fast, make it real, defend the trade-offs.
