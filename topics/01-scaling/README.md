# 01 - Scaling

## Objective

Understand how applications handle increasing traffic using vertical and horizontal scaling.

Implement and benchmark different scaling strategies using Django, Gunicorn, Docker, Nginx, and k6.

## Concepts

- Vertical Scaling (Scale Up)
- Horizontal Scaling (Scale Out)
- Load Distribution
- Resource Utilization
- Performance Bottlenecks
- Application Concurrency
- Load Balancing

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
| Baseline | Single application instance with 1 CPU | Completed |
| Vertical Scaling V1 | Increase CPU allocation to 2 CPUs | Completed |
| Vertical Scaling V2 | Increase Gunicorn workers to 2 | Completed |
| Horizontal Scaling | Run multiple Django instances behind Nginx | Completed |
| Performance Comparison | Compare baseline, vertical and horizontal scaling | Completed |

## Performance Metrics

- Requests Per Second (RPS)
- Average Response Time
- p50 Latency
- p90 Latency
- p95 Latency
- p99 Latency
- Error Rate
- CPU Utilization
- Memory Utilization

## Analysis

### 1. Baseline Experiment

The baseline used a single Django application container with the following configuration:

- CPU limit: 1 CPU
- Memory limit: 512 MB
- Gunicorn workers: 1
- Gunicorn threads: 1
- Virtual users: 10
- Test duration: 30 seconds

The application handled 455 requests at approximately 14.84 requests per second.

Average response latency was 666.86 ms, with a p95 latency of 871.69 ms.

No failed requests were recorded.

CPU usage was observed near the configured CPU limit, suggesting that CPU capacity could be a bottleneck.

### 2. Vertical Scaling Analysis

Vertical scaling was performed by increasing the resources available to a single application instance and separately tuning Gunicorn workers.

**V1 - Increased CPU Allocation**

Configuration:
- CPU limit: 2 CPUs
- Memory limit: 512 MB
- Gunicorn workers: 1

Results:
- Requests: 547
- Throughput: 17.93 RPS
- Average latency: 553.02 ms
- p95 latency: 610.58 ms
- p99 latency: 631.64 ms
- Failed requests: 0

Compared with the baseline:
- Throughput improved by approximately 20.8%.
- Average latency decreased by approximately 17.1%.
- p95 latency decreased by approximately 30%.

**V2 - Increased Gunicorn Workers**

Configuration:
- CPU limit: 2 CPUs
- Memory limit: 512 MB
- Gunicorn workers: 2

Results:
- Requests: 963
- Throughput: 31.76 RPS
- Average latency: 312.88 ms
- p95 latency: 375.42 ms
- p99 latency: 443.50 ms
- Failed requests: 0

Compared with V1:
- Throughput improved by approximately 77.2%.
- Average latency decreased by approximately 43.5%.
- p95 latency decreased by approximately 38.5%.

The experiment demonstrated that both CPU allocation and application concurrency settings influence performance.

Increasing Gunicorn workers allowed the application to handle more concurrent requests.

### 3. Horizontal Scaling Analysis

Horizontal scaling was implemented by running multiple Django application containers behind an Nginx load balancer.

Architecture:

k6 → Nginx → Django Instance 1
             → Django Instance 2

Nginx distributes incoming requests across the application instances using its default round-robin load-balancing strategy.

Each application instance runs independently in its own Docker container.

The application hostname endpoint was used to verify that requests reached different application instances.

This experiment demonstrates how horizontal scaling distributes incoming traffic instead of increasing the resources of a single application instance.

### 4. Overall Analysis

The experiments demonstrate two approaches to increasing application capacity:

- Vertical scaling increases the resources allocated to an existing application instance.
- Horizontal scaling increases the number of application instances and distributes incoming requests between them.

Vertical scaling is relatively straightforward but is limited by the available resources of a single machine.

Horizontal scaling provides a way to distribute workload across multiple instances, but introduces additional architectural components such as load balancers and requires careful handling of shared state and dependencies.

The performance of either approach depends on the workload, application concurrency, available resources, and infrastructure configuration.

**Note:** These experiments were performed locally using Docker. The load generator and application containers shared the same host machine, so results should not be treated as production capacity benchmarks.

## Key Learnings

1. Under increasing traffic, a single application instance can become constrained by its available resources.

2. Vertical scaling (scale up) improves the capacity of an existing instance by increasing its allocated resources.

3. Increasing CPU allocation does not automatically guarantee proportional performance improvements.

4. Gunicorn worker processes allow a synchronous Django application to handle multiple requests concurrently.

5. Horizontal scaling (scale out) distributes incoming requests across multiple application instances.

6. Nginx can act as a load balancer and distribute traffic between backend application servers.

7. Docker Compose makes it possible to run and manage multiple application instances locally.

8. k6 helps measure throughput, latency, and failed requests under simulated concurrent traffic.

9. CPU and memory monitoring helps identify potential resource bottlenecks.

10. Scaling decisions should be based on measured workload characteristics rather than assumptions.

## Implementation Details

### Application

A Django application exposing four endpoints:

- `/api/health/` - Application health check.
- `/api/info/` - Returns application hostname and process information.
- `/api/light/` - Lightweight application response.
- `/api/work/` - CPU-intensive endpoint used for performance testing.

### Containerization

Docker is used to package the Django application.

Docker Compose manages application containers, resource limits, and the load-testing environment.

Separate Compose configurations are used for vertical and horizontal scaling experiments.

### Traffic Generation

k6 is used to simulate concurrent requests.

The same workload configuration is used across experiments to make performance comparisons more meaningful.

### Load Balancing

Nginx is configured as a reverse proxy and load balancer.

It distributes incoming requests across multiple Django application instances using round-robin balancing.

### Monitoring

Docker Stats is used to observe container CPU and memory utilization during load tests.

k6 provides request throughput, response latency, and failure metrics.

## Results

Detailed experimental measurements are documented separately:

- [Baseline Experiment](results/baseline.md)
- [Vertical Scaling Experiment](results/vertical-scaling.md)
- [Horizontal Scaling Experiment](results/horizontal-scaling.md)
- [Scaling Comparison](results/comparison.md)

## Conclusion

This experiment provided practical experience with vertical and horizontal scaling using a containerized Django application.

Vertical scaling demonstrated how increasing CPU allocation and Gunicorn worker count can improve the performance of a single application instance.

Horizontal scaling demonstrated how multiple application instances can be deployed behind an Nginx load balancer to distribute incoming traffic.

The main takeaway is that scaling is not simply about adding more CPU or application instances. It requires understanding workload characteristics, identifying bottlenecks, monitoring resource utilization, and selecting an appropriate architecture based on measured performance.