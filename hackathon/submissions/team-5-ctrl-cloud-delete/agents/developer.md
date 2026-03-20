# Developer

## Hackathon: Contoso Financial — Cloud Migration

---

## Responsibilities

- Build and migrate the **customer-facing web app** workload
- Refactor application code to target cloud primitives (e.g., use S3 SDK against MinIO, not local file paths)
- Implement Redis caching and session management where applicable
- Write Dockerfiles for the backend and frontend services
- Ensure the app is wired correctly through the Nginx reverse proxy
- Handle API design, routes, and any frontend static assets

---

## Key Outputs

- Backend application code (Flask or equivalent) targeting cloud-native services
- `Dockerfile` for backend and frontend containers
- Redis integration (caching layer)
- Working end-to-end demo of the web app running via Docker Compose

---

## Migration Pattern

**Re-platform** — swap local file/DB calls for managed service SDKs with minimal code changes. The goal is speed of migration while demonstrating cloud-native connectivity.
