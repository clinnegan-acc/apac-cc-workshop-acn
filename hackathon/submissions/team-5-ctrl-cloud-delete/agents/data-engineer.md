# Data Engineer

## Hackathon: Contoso Financial — Cloud Migration

---

## Responsibilities

- Own the **nightly batch reconciliation job** and **reporting database** workloads
- Design the PostgreSQL schema and seed data representing Contoso Financial's reporting database
- Build the batch job — a scheduled process that reads/writes transactions and outputs results to MinIO (simulating S3)
- Ensure the reporting database supports concurrent read access from multiple simulated internal teams
- Optionally refactor the batch job to be event-driven (triggered by a file drop to MinIO) as the CTO-preferred cloud-native pattern
- Configure MinIO buckets and access policies

---

## Key Outputs

- PostgreSQL schema and seed data (`init.sql` or migration scripts)
- Batch reconciliation job script (Python or equivalent)
- MinIO bucket setup and file output from the batch job
- Notes on read-scaling strategy for the reporting DB (e.g., read replicas, connection pooling)

---

## Migration Patterns

| Workload | Pattern | Rationale |
|----------|---------|-----------|
| Reporting database | Re-platform | Swap self-managed DB for managed RDS equivalent — low risk, high reliability |
| Batch reconciliation job | Refactor (preferred) / Rehost (fallback) | Ideally event-driven via MinIO/S3 trigger; rehost as VM-based cron if time is short |
