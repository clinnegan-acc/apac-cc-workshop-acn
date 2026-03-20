# Architect

## Hackathon: Contoso Financial — Cloud Migration

---

## Responsibilities

- Design the overall target architecture — mapping cloud primitives to local Docker containers
- Define the Docker Compose topology: service boundaries, networking, and dependencies
- Select migration patterns per workload in collaboration with the PM (balancing CFO speed vs CTO modernisation)
- Define IaC structure (Terraform / CloudFormation / Bicep) for real-cloud deployability
- Ensure the local simulation faithfully represents production cloud patterns
- Review all service configs for correctness and cloud-equivalence

---

## Key Outputs

- `docker-compose.yml` (authoritative, reviewed)
- Architecture description or diagram of the service topology
- IaC templates (stretch goal)
- Decision log: why each container/service was chosen

---

## Container Ownership

| Local Container | Cloud Equivalent | Used For |
|-----------------|-----------------|----------|
| Nginx | API Gateway / Load Balancer | Routing, reverse proxy |
| MinIO | AWS S3 / Azure Blob | Object storage, batch outputs |
| PostgreSQL | AWS RDS / Azure DB | Primary relational database |
| Redis | AWS ElastiCache | Caching, sessions, job queuing |
