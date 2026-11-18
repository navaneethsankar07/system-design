# 01 - Scaling

## Objective

Understand how applications handle increasing traffic
using vertical and horizontal scaling.

## Concepts

- Vertical Scaling (Scale Up)
- Horizontal Scaling (Scale Out)
- Load Distribution
- Resource Utilization
- Performance Bottlenecks

## Technology Stack

- Django
- Gunicorn
- Docker
- Docker Compose
- Nginx
- k6

## Experiments

| Experiment | Description | Status |
|---|---|---|
| Baseline | Single application instance | Pending |
| Vertical Scaling | Increase resources of one instance | Pending |
| Horizontal Scaling | Run multiple instances | Pending |
| Performance Comparison | Compare experiment results | Pending |

## Performance Metrics

- Requests Per Second (RPS)
- Average Response Time
- p50 Latency
- p95 Latency
- p99 Latency
- Error Rate
- CPU Utilization
- Memory Utilization

## Analysis

Results and observations will be documented here.

## Key Learnings

To be updated after completing the experiments.

## Implementation Details

### Application

A Django application exposing four endpoints:

- `/api/health/`
- `/api/info/`
- `/api/light/`
- `/api/work/`

### Containerization

Docker is used to package the application.
Docker Compose manages the application and load generator.

### Traffic Generation

k6 is used to simulate concurrent requests.

### Monitoring

Docker Stats is used to observe container CPU
and memory utilization.

## Results

See [Baseline Experiment](results/baseline.md).