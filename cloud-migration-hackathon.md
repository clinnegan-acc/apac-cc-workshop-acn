# Mock Cloud Migration Hackathon Plan

## Tech Stack

### Legacy Architecture (build first ~15 min)

- **Monolithic app**: Python Flask — single server handling everything
- **Database**: SQLite file (simplest "legacy" DB)
- **Architecture**: One process serving API + static HTML, direct DB calls, no separation of concerns

### "Cloud" Architecture (migrate to ~25 min)

Simulate with **Docker Compose** — each container represents a cloud service:

| Container | Simulates | Tech |
|-----------|-----------|------|
| `api-gateway` | API Gateway / Load Balancer | Nginx reverse proxy |
| `frontend` | Static hosting (S3/CloudFront) | Nginx serving static files |
| `backend` | Compute (ECS/Lambda) | Flask (same code, extracted) |
| `database` | Managed DB (RDS) | PostgreSQL container |
| `cache` | ElastiCache | Redis container |
| `queue` | SQS/message broker | Redis pub/sub or RabbitMQ |

### Summary

```
Legacy:       Python Flask + SQLite (1 file, 1 process)
Cloud:        Docker Compose with 4-6 containers
Migration:    Same Python code, split into services
```

---

## Team Roles (6 people)

| Role | Person | Responsibility |
|------|--------|----------------|
| **Legacy Dev** | 1 | Build the Flask monolith + SQLite, seed data |
| **Frontend Dev** | 2 | Build static HTML/CSS UI, split it out for Nginx container later |
| **DevOps Lead** | 3 | Write Dockerfiles, `docker-compose.yml`, Nginx config |
| **Backend Dev** | 4 | Migrate Flask to use Postgres + Redis, split into service |
| **Cloud Architect** | 5 | Design the architecture diagrams, map containers to AWS equivalents |
| **Demo Lead / PM** | 6 | Coordinate timing, prepare the demo script, present |

### Parallel Workstreams

```
Minutes 0-15:   Legacy Dev + Frontend Dev build the monolith together
                DevOps Lead + Backend Dev prep Docker configs
                Cloud Architect draws before/after architecture diagrams
                Demo Lead plans the demo narrative

Minutes 15-35:  DevOps Lead wires up docker-compose
                Backend Dev migrates DB from SQLite to Postgres
                Frontend Dev extracts static files into Nginx container
                Legacy Dev adds Redis caching layer
                Cloud Architect labels each container with AWS equivalent
                Demo Lead tests the legacy app, documents the "before"

Minutes 35-50:  Everyone converges — integration, testing, demo prep
```

---

## 50-Minute Timeline

| Time | Task |
|------|------|
| 0-5 | Scaffold legacy Flask app + SQLite (inventory CRUD) |
| 5-15 | Get legacy working end-to-end, show it's a monolith |
| 15-20 | Write `docker-compose.yml`, Dockerfiles |
| 20-35 | Split monolith: extract API, move to Postgres, add Nginx |
| 35-45 | Add Redis cache layer, show the "cloud" version running |
| 45-50 | Demo: side-by-side comparison, talk about what each container represents |

---

## Key Demo Talking Points

- **Before**: single process, SQLite file, no scaling, single point of failure
- **After**: containerized microservices, managed DB, caching layer, reverse proxy
- Show `docker-compose ps` to visualize the services
- Show `docker-compose scale backend=3` for horizontal scaling

---

## Minimal Starting Point

### Legacy App (single file)

```python
# legacy_app.py — your entire "legacy system"
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("inventory.db")

@app.route("/products")
def products():
    db = get_db()
    rows = db.execute("SELECT * FROM products").fetchall()
    return jsonify(rows)

# ... CRUD routes, HTML templates, everything in one file
```

### Cloud Architecture (Docker Compose)

```yaml
# docker-compose.yml — your "cloud"
services:
  nginx:
    image: nginx:alpine
    ports: ["80:80"]
  backend:
    build: ./backend
    depends_on: [db, redis]
  db:
    image: postgres:15-alpine
  redis:
    image: redis:alpine
```
