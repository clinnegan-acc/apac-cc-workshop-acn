# The Lift, the Shift, and no Regrets
## Hackathon Problem Statement

---

## The Scenario

**Contoso Financial** is a fictional company with three existing ("on-prem") workloads that need to move to the cloud:

1. **A customer-facing web app** — something users interact with directly, so availability and performance matter
2. **A nightly batch reconciliation job** — a scheduled process that likely crunches financial transactions, balances accounts, etc.
3. **A reporting database** — a shared data store that 5 internal teams query, meaning it has concurrent read load and probably can't go down

---

## The Organizational Tension (This Is Intentional)

There are two stakeholders in conflict:

- **The CFO** just signed a cloud contract — the priority is *getting off prem*, likely to cut infrastructure costs. They want results fast.
- **The CTO** wants *cloud-native*, not just "lift-and-shift" — meaning don't just move the same old VM to the cloud; actually re-architect to use managed services, autoscaling, serverless where appropriate, etc.

You have to navigate this tension. Your migration design needs to justify its choices, balancing speed/pragmatism against modernization — and ideally satisfy both stakeholders, or at least make the trade-offs explicit.

---

## What You're Actually Building

You won't touch real cloud infrastructure. Instead, you simulate a **production-equivalent cloud architecture locally** using Docker Compose, where each container maps to a real cloud primitive:

| Local Container | Cloud Equivalent        | Used For                                          |
|-----------------|-------------------------|---------------------------------------------------|
| **MinIO**       | AWS S3 (or Azure Blob)  | Object storage, batch job outputs, file staging   |
| **PostgreSQL**  | AWS RDS / Azure DB      | Primary relational database                       |
| **Redis**       | AWS ElastiCache         | Caching, session management, job queuing          |

This mirrors exactly how real migration teams work — you validate architecture locally before committing to live cloud spend.

---

## The Deliverables

The phrase **"cloud-ready artifacts"** is key. You're expected to produce:

- A **Docker Compose file** that wires up the local cloud-equivalent environment
- **Application code / configs** for each of the three workloads, written to target cloud primitives (e.g., your app talks to MinIO using the S3 SDK, not a local file path)
- A **migration rationale** — which cloud you picked, which migration pattern you chose for each workload (rehost vs. re-platform vs. refactor), and why, given the CFO/CTO tension
- Potentially **IaC templates** (Terraform, CloudFormation, Bicep) that could deploy the same architecture to real cloud

---

## The Core Design Challenge

For each of the three workloads, you need to pick a **migration pattern** along this spectrum:

| Pattern | Description | Trade-off |
|---|---|---|
| **Rehost** ("lift-and-shift") | Move it as-is to a VM in the cloud | Fast and cheap, but not cloud-native. CFO loves it, CTO hates it. |
| **Re-platform** | Minimal changes to use a managed service (e.g., swap self-managed Postgres for RDS) | Middle ground — some modernization, low risk. |
| **Refactor / Re-architect** | Redesign the workload to be cloud-native (e.g., batch job becomes a serverless function triggered by S3 events) | CTO loves it, but it takes longer. |

A strong solution will likely **mix patterns** — perhaps lifting the web app initially while refactoring the batch job to be serverless — and will **defend those choices** in the context of a financial services company where uptime and data integrity are non-negotiable.

---

## TL;DR

Build a local Docker Compose environment that faithfully simulates a cloud architecture, migrate three workloads into it using thoughtful patterns, and produce artifacts that a real team could use to deploy to actual cloud — all while making a coherent argument for **why your architecture resolves the CFO vs. CTO standoff**.
