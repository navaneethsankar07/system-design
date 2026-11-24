# Load Balancing

A hands-on project to understand, implement, and evaluate different load-balancing algorithms using Docker, Flask, Nginx, and k6.

## Objectives

- Understand how load balancers distribute incoming traffic.
- Implement different load-balancing algorithms.
- Analyze request distribution across backend instances.
- Experiment with different backend capacities and processing times.
- Simulate backend failures and recovery.
- Compare algorithm performance using load-testing results.

## Architecture

The project consists of three Flask backend instances behind an Nginx load balancer.

```text
                  Client
                    |
                    v
              Nginx Load Balancer
                    |
          +---------+---------+
          |         |         |
          v         v         v
       Backend 1 Backend 2 Backend 3
        :5000     :5000     :5000
```

## Technology Stack

- **Backend:** Python, Flask, Gunicorn
- **Containerization:** Docker, Docker Compose
- **Load Balancer:** Nginx
- **Load Testing:** k6

## Backend Endpoints

| Endpoint | Description |
|---|---|
| `/` | Basic application response |
| `/health` | Backend health check |
| `/info` | Returns backend instance information |
| `/work?delay=2` | Simulates processing delays |

## Load Balancing Algorithms

- [x] Round Robin
- [x] Weighted Round Robin
- [x] Least Connections
- [x] Weighted Least Connections
- [x] IP Hash
- [x] Consistent Hashing
- [x] Least Response Time Experiment
- [x] Random
- [x] Power of Two Choices
- [x] Failure Handling
- [x] Benchmark and Comparison

## Running the Project

**Start the backend and load balancer:**

```bash
docker compose up -d --build
```

**Check running containers:**

```bash
docker compose ps
```

**Test the load balancer:**

```bash
curl http://localhost:8000/info
```

**Check backend health:**

```bash
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
```

**Stop the project:**

```bash
docker compose down
```

## Experiment Results

Each experiment includes its configuration, test methodology, actual results, observations, and conclusion.

| Experiment | Results |
|---|---|
| Round Robin | [View Results](results/round-robin.md) |
| Weighted Round Robin | [View Results](results/weighted-round-robin.md) |
| Least Connections | [View Results](results/least-connections.md) |
| Weighted Least Connections | [View Results](results/weighted-least-connections.md) |
| IP Hash | [View Results](results/ip-hash.md) |
| Consistent Hashing | [View Results](results/consistent-hashing.md) |
| Least Response Time | [View Results](results/least-response-time.md) |
| Random | [View Results](results/random.md) |
| Power of Two Choices | [View Results](results/power-of-two.md) |
| Failure Handling | [View Results](results/failure-handling.md) |
| Benchmark Comparison | [View Results](results/benchmark-comparison.md) |

## Project Status

The implementation and experimentation phases are documented in the `results/` directory. Benchmark findings and observations are based on the workloads and configurations tested.