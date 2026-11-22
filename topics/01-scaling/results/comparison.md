# Scaling Comparison

## Performance Comparison

| Metric | Baseline | Vertical V1 | Vertical V2 | Horizontal H2 |
|---|---:|---:|---:|---:|
| App instances | 1 | 1 | 1 | 2 |
| CPU per instance | 1 CPU | 2 CPUs | 2 CPUs | 1 CPU |
| Total CPU limit | 1 CPU | 2 CPUs | 2 CPUs | 2 CPUs |
| Gunicorn workers per instance | 1 | 1 | 2 | 2 |
| Total Gunicorn workers | 1 | 1 | 2 | 4 |
| Total requests | 455 | 547 | 963 | 900 |
| RPS | 14.84 | 17.93 | 31.76 | 29.60 |
| Average latency | 666.86 ms | 553.02 ms | 312.88 ms | 335.23 ms |
| p50 latency | 687.89 ms | 550.06 ms | 311.59 ms | 322.09 ms |
| p95 latency | 871.69 ms | 610.58 ms | 375.42 ms | 617.32 ms |
| p99 latency | 1.21 s | 631.64 ms | 443.50 ms | 690.38 ms |
| Failed requests | 0 | 0 | 0 | 0 |

## Architectural Differences

### Vertical Scaling

- Increases resources available to a single application instance.
- Can improve performance by increasing CPU, memory, or other resources.
- Simple to implement because it does not require additional application instances or a load balancer.
- Limited by the capacity of the underlying machine.
- A single application instance remains a potential single point of failure.
- Increasing Gunicorn workers can improve concurrency, depending on the workload and available resources.

### Horizontal Scaling

- Adds multiple application instances instead of relying on a single instance.
- Uses a load balancer such as Nginx to distribute incoming requests.
- Allows workload to be processed by multiple instances concurrently.
- Can increase aggregate processing capacity by adding instances.
- Requires consideration of shared state, session management, health checks, database capacity, networking and load-balancer overhead.
- Can improve application-level availability when instances and infrastructure are appropriately configured, although multiple instances alone do not guarantee high availability.

## Final Observations

- The baseline configuration achieved 14.84 RPS using 1 CPU and 1 Gunicorn worker.
- Vertical V1 increased the CPU limit from 1 CPU to 2 CPUs while keeping 1 Gunicorn worker. Throughput improved by approximately 20.8%.
- Vertical V2 kept the 2 CPU limit but increased Gunicorn workers from 1 to 2. Throughput increased to 31.76 RPS, approximately 2.14 times the baseline.
- Horizontal H2 used two application instances, each with a 1 CPU limit and 2 Gunicorn workers, behind Nginx. It achieved 29.60 RPS.
- Both V2 and H2 had a total application CPU limit of 2 CPUs, but V2 achieved higher throughput and lower latency in this test.
- V2 had the best measured performance among the tested configurations, with the highest throughput and lowest average, p95 and p99 latency.
- H2 outperformed the baseline and V1 in throughput and average latency, but its p95 and p99 latency were higher than V1's.
- All four configurations recorded zero failed requests during their respective load tests.

The results show that scaling decisions should be based on the application's workload and measured performance. In this CPU-intensive workload, increasing Gunicorn workers in the vertical configuration produced the best benchmark result. Horizontal scaling successfully distributed requests across multiple instances but introduced additional architectural and proxying overhead.

These results are specific to this local test environment and should not be treated as universal scaling benchmarks.

## Conclusion

Both vertical and horizontal scaling improved performance compared with the baseline in the experiments conducted.

Vertical V2 produced the best performance for the tested CPU-intensive workload by using 2 CPUs and 2 Gunicorn workers in a single application container. Horizontal H2 successfully distributed requests across two application instances through Nginx and demonstrated how an application can scale out.

Vertical scaling is a simpler approach when a single machine has sufficient resources and the goal is to improve the capacity of one application instance. Horizontal scaling is useful when distributing workloads across instances, expanding capacity incrementally, and designing systems for resilience and larger-scale traffic.

The appropriate scaling strategy depends on measured performance, resource availability, workload characteristics, reliability requirements and application architecture.