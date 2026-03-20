# CLAUDE.md — Team 5: CTL Cloud Delete

## Project Purpose
This project simulates a cloud migration for Contoso Financial, a fictional financial services company. Three on-premises workloads are migrated from a Python Flask + SQLite monolith to a Docker Compose environment that mirrors real cloud primitives (AWS/Azure equivalents).

The goal is to produce cloud-ready artifacts: a working local stack, migrated application code, and a migration rationale that balances speed (CFO priority) vs. cloud-native modernization (CTO priority).

---

## Project Structure

```
team5_ctlCloudDelete/
├── CLAUDE.md                  # This file — Claude Code project context
├── README.md                  # Project overview and demo notes
├── submission.html            # Hackathon presentation slide
│
├── legacy/
│   ├── legacy_app.py          # Original monolith: Flask + SQLite, all workloads in one file
│   ├── inventory.db           # SQLite database (auto-created on first run)
│   └── requirements.txt
│
├── docker-compose.yml         # Full cloud simulation stack
│
├── backend/
│   ├── Dockerfile
│   ├── app.py                 # Extracted Flask API (re-platformed from monolith)
│   ├── models.py              # SQLAlchemy models (PostgreSQL)
│   ├── requirements.txt
│   └── .env.example
│
├── worker/
│   ├── Dockerfile
│   ├── reconcile.py           # Batch reconciliation job (refactored, event-driven)
│   ├── requirements.txt
│   └── .env.example
│
├── nginx/
│   ├── nginx.conf             # Reverse proxy config (simulates API Gateway)
│   └── static/                # Static frontend files (simulates S3/CloudFront)
│
└── infra/
    └── terraform/             # (Optional) IaC for real cloud deployment
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

---

## Key Files and Their Roles

| File | Role | Cloud Mapping |
|------|------|---------------|
| `legacy/legacy_app.py` | The "before" — monolith with SQLite | On-prem server |
| `docker-compose.yml` | Orchestrates all cloud-equivalent services | Cloud infrastructure |
| `backend/app.py` | Re-platformed API service | AWS ECS / Azure Container Apps |
| `backend/models.py` | SQLAlchemy ORM models | AWS RDS / Azure DB for PostgreSQL |
| `worker/reconcile.py` | Refactored batch job, queue-triggered | AWS Lambda + SQS / Azure Functions |
| `nginx/nginx.conf` | Reverse proxy + static serving | AWS API Gateway + CloudFront |

### Docker Compose Services

| Service | Image/Build | Simulates |
|---------|------------|-----------|
| `nginx` | `nginx:alpine` | API Gateway / CDN |
| `backend` | `./backend` | Compute (ECS task / container app) |
| `worker` | `./worker` | Batch / serverless worker |
| `postgres` | `postgres:15-alpine` | AWS RDS / Azure Database |
| `redis` | `redis:alpine` | AWS ElastiCache (cache + queue) |
| `minio` | `minio/minio` | AWS S3 / Azure Blob Storage |

---

## Conventions and Patterns

- **Database access**: Always use SQLAlchemy ORM in `backend/`. Never use raw SQLite or direct `psycopg2` calls.
- **Object storage**: Use the `boto3` S3 client pointed at MinIO (`MINIO_ENDPOINT` env var). Never write to local filesystem paths in production code paths.
- **Queue**: Use Redis `LPUSH`/`BRPOP` pattern (simulates SQS). The worker blocks on `BRPOP reconcile-queue 0`.
- **Config**: All secrets and endpoints via environment variables. See `.env.example` files. Never hardcode connection strings.
- **No state in containers**: Backend and worker containers must be stateless. All state goes to postgres, redis, or minio.
- **Health checks**: Each service in `docker-compose.yml` has a `healthcheck` block.

---

## Commands

### Run the full cloud stack
```bash
docker-compose up --build
```

### Run legacy monolith (for comparison demo)
```bash
cd legacy
pip install -r requirements.txt
python legacy_app.py
# Visit http://localhost:5000
```

### Scale the backend horizontally
```bash
docker-compose up --scale backend=3
```

### Manually trigger the batch reconciliation job
```bash
docker-compose run worker python reconcile.py
# Or enqueue via Redis:
docker-compose exec redis redis-cli LPUSH reconcile-queue '{"run_date":"2026-03-20"}'
```

### Run tests
```bash
docker-compose run backend pytest tests/
```

### Tear down
```bash
docker-compose down -v
```

---

## Migration Rationale (Summary)

| Workload | Pattern | Why |
|----------|---------|-----|
| Customer Web App | Re-platform | Fast migration, stateless, horizontally scalable |
| Batch Reconciliation | Refactor | Event-driven, decoupled, cloud-native — CTO win |
| Reporting Database | Re-platform | SQLite → PostgreSQL solves concurrent read problem |

The mixed strategy delivers quick wins for the CFO (web app and DB migrate fast) while demonstrating genuine cloud-native architecture for the CTO (batch job is fully refactored).

---

## Environment Variables

### backend/.env.example
```
DATABASE_URL=postgresql://contoso:contoso@postgres:5432/contoso
REDIS_URL=redis://redis:6379/0
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=reconciliation-output
```

### worker/.env.example
```
DATABASE_URL=postgresql://contoso:contoso@postgres:5432/contoso
REDIS_URL=redis://redis:6379/0
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=reconciliation-output
QUEUE_NAME=reconcile-queue
```
