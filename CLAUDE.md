# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

Workshop package for the APAC Claude Code Workshop (Accenture cohort). Contains two runnable applications and hackathon materials for a cloud migration exercise.

## Applications

### Legacy App (`legacy/`)

Flask monolith with a retro terminal UI — represents the "before" in the cloud migration hackathon.

```bash
# Terminal UI (default)
cd legacy && ./run.sh

# Flask API server on port 8001
cd legacy && ./run.sh --api
```

- **Stack:** Flask, JSON flat files, Python 3
- **`app.py`** — Single-file Flask API with all routes (inventory, orders, demand, backlog, spending, dashboard)
- **`terminal_ui.py`** — Menu-driven ANSI terminal interface that reads JSON data directly
- **`data/`** — 7 JSON files loaded into memory at startup; writes persist to disk
- First run creates a `.venv` and installs Flask automatically

### Modern App (`inventory-management/`)

Full-stack app — the workshop starter that students fork and work with.

```bash
# Both servers at once
cd inventory-management && ./scripts/start.sh

# Or manually:
cd inventory-management/server && uv run python main.py    # Backend: port 8001
cd inventory-management/client && npm install && npm run dev # Frontend: port 3000
```

- **Backend:** FastAPI + Pydantic + uvicorn, managed with `uv`
- **Frontend:** Vue 3 + Composition API + Vite + vue-router + axios
- **Data:** Same JSON format as legacy app, loaded in-memory via `server/mock_data.py`
- **Tests:** `cd inventory-management/tests && uv run pytest backend/ -v`
- **API docs:** http://localhost:8001/docs (auto-generated Swagger)
- Has its own `CLAUDE.md` files at root, `server/`, and `client/` levels with detailed component-specific guidance — defer to those when working inside `inventory-management/`

## Shared Data Model

Both apps use identical JSON data in their respective `data/` directories:

| File | Content |
|------|---------|
| `inventory.json` | Items with SKU, category, warehouse, quantity, unit cost, reorder point |
| `orders.json` | Orders with customer, items array, status (Delivered/Shipped/Processing/Backordered), dates, value |
| `demand_forecasts.json` | SKU-level demand with current/forecasted amounts and trend |
| `backlog_items.json` | Shortage items with quantity needed vs available, days delayed, priority |
| `spending.json` | Nested: spending_summary, monthly_spending, category_spending |
| `transactions.json` | Individual transaction records |
| `purchase_orders.json` | Links backlog items to purchase orders |

## Cloud Migration Hackathon

`cloud-migration-hackathon.md` contains the full plan: migrate the legacy Flask monolith to a Docker Compose architecture simulating cloud services (Nginx, PostgreSQL, Redis, separate frontend/backend containers).

**Target architecture:**
- `api-gateway` — Nginx reverse proxy
- `frontend` — Nginx serving static files
- `backend` — Flask/FastAPI compute service
- `database` — PostgreSQL (replacing JSON flat files)
- `cache` — Redis
- `queue` — Redis pub/sub or RabbitMQ

Hackathon scenarios are in `hackathon/scenarios/` (5 challenges including code modernization, cloud migration, data engineering, analytics, and agentic solutions).

## Hackathon Submissions

- Live under `hackathon/submissions/` with naming convention `teamN_hackathon-name`
- Each team folder must contain: `README.md`, `CLAUDE.md`, and `submission.html`
- Do not modify other teams' submission folders

## Facilitation Notes

- Starter app source: [beck-source/inventory-management](https://github.com/beck-source/inventory-management) — students fork this
- API keys from [console.anthropic.com](https://console.anthropic.com)
- Encourage `/init` to generate CLAUDE.md in student projects
- Reference `snippets/` for approved code patterns; direct questions to `faq/` first
