# Load Balancing

A hands-on project to understand, implement, and compare load-balancing algorithms using Docker, Flask, Nginx, and k6.

## Objectives

- Understand how a load balancer distributes traffic.
- Implement and experiment with different load-balancing algorithms.
- Observe request distribution across backend instances.
- Simulate different backend processing times and capacities.
- Test backend failures and recovery.
- Compare algorithms using load-test results.

## Architecture (Phase 1)

Currently, three backend instances are running independently. A load balancer has not been added yet.

```text
Client
  |
  | Direct requests (for testing)
  |
  +------ Backend 1 (5001)
  +------ Backend 2 (5002)
  +------ Backend 3 (5003)
```

## Technology Stack

- Python
- Flask
- Gunicorn
- Docker
- Docker Compose
- Nginx (planned)
- k6 (planned)

## Backend Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Basic application response |
| `/health` | Backend health check |
| `/info` | Instance identification |
| `/work?delay=2` | Simulates processing delay |

## Project Phases

- [x] Phase 1 — Backend foundation
- [x] Phase 2 — Round Robin
- [X] Phase 3 — Weighted Round Robin
- [x] Phase 4 — Least Connections
- [x] Phase 5 — IP Hash
- [ ] Phase 6 — Hash and Consistent Hashing
- [ ] Phase 7 — Least Response Time
- [ ] Phase 8 — Random and Power of Two Choices
- [ ] Phase 9 — Failure Handling
- [ ] Phase 10 — Benchmark and Comparison

## Running the Project

Start the backend instances:

```bash
docker compose up -d --build
```

Check status:

```bash
docker compose ps
```

Test the backend:

```bash
curl http://localhost:5001/info
curl http://localhost:5002/info
curl http://localhost:5003/info
```

Stop the project:

```bash
docker compose down
```

## Experiments

Benchmark results and observations will be documented under `results/` as each experiment is completed.

## Status

Phase 1 completed once all three instances are running and verified independently.