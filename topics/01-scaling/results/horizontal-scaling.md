# Horizontal Scaling Experiment

## Objective

Run multiple Django application instances behind an Nginx load balancer and measure the effect of distributing requests across multiple instances.

## Architecture

```text
                 k6 Load Tester
                       |
                       v
                 Nginx Load Balancer
                  /             \
                 v               v
            Django App 1     Django App 2
            (1 CPU limit)    (1 CPU limit)
```

## Configurations

| Test | Instances | CPU per instance | Total CPU limit |
|---|---:|---:|---:|
| H2 | 2 | 1 CPU | 2 CPUs |

## H2 Results

| Metric | Value |
|---|---:|
| Total requests | 900 |
| Requests per second | 29.60 RPS |
| Average latency | 335.23 ms |
| p50 latency | 322.09 ms |
| p90 latency | 592.18 ms |
| p95 latency | 617.32 ms |
| p99 latency | 690.38 ms |
| Maximum latency | 855.38 ms |
| Failed requests | 0 (0%) |
| Successful checks | 900/900 (100%) |
| Virtual users | 10 |
| Test duration | 30 seconds |

## H2 Resource Observations

| Metric | App 1 | App 2 |
|---|---:|---:|
| CPU snapshot during load | 100.71% | 103.57% |
| Memory snapshot during load | 83.51 MiB | 81.55 MiB |
| Memory limit | 512 MiB | 512 MiB |
| CPU limit | 1 CPU | 1 CPU |

These are individual Docker resource snapshots taken during the test, not averages or peaks.

## Observations

- Nginx successfully distributed requests between both Django application instances.
- Both application containers were healthy during the test.
- The `/api/info/` endpoint returned two different hostnames, confirming that requests reached both containers.
- The CPU snapshots show both application instances actively using approximately one CPU each during the load test.
- Both instances used approximately 82–84 MiB of memory, well below their 512 MiB limits.
- All 900 requests succeeded, with no HTTP request failures.
- Nginx acted as the entry point and distributed incoming requests to the application instances.

## Analysis

The H2 configuration achieved approximately 29.60 requests per second while distributing the workload across two application containers.

The resource snapshots show that both application instances were utilizing their allocated CPU capacity during the test. This suggests that the CPU-intensive workload was distributed across the two instances rather than being handled by a single application container.

However, horizontal scaling did not outperform the V2 vertical scaling experiment in this particular test:

| Metric | V2 (Vertical) | H2 (Horizontal) |
|---|---:|---:|
| Total requests | 963 | 900 |
| RPS | 31.76 | 29.60 |
| Average latency | 312.88 ms | 335.23 ms |
| p50 | 311.59 ms | 322.09 ms |
| p95 | 375.42 ms | 617.32 ms |
| p99 | 443.50 ms | 690.38 ms |
| Failed requests | 0 | 0 |

Compared with V2:

- Throughput was approximately 6.8% lower.
- Average latency was approximately 7.1% higher.
- p95 latency was approximately 64.4% higher.
- p99 latency was approximately 55.5% higher.

Both configurations had a total application CPU limit of 2 CPUs. However, H2 used two separate containers behind Nginx, while V2 used one container with two Gunicorn workers.

The horizontal setup also introduces Nginx proxying and additional container/network overhead. These factors, along with host resource contention and test variability, may contribute to the difference. The experiment does not prove that horizontal scaling is inherently slower than vertical scaling.

## Key Learnings

- Horizontal scaling increases application capacity by adding more application instances.
- A load balancer such as Nginx distributes incoming requests among available application instances.
- Multiple instances can process requests concurrently.
- The `/api/info/` endpoint can be used to verify which application instance handles a request.
- Docker CPU limits can be configured independently for each application container.
- Horizontal scaling provides an architectural path toward distributing workloads and improving availability.
- A load balancer introduces some additional overhead.
- Adding more instances does not automatically guarantee higher performance; the workload, resource allocation, load-balancer overhead, and host capacity all matter.
- Resource utilization should be measured during the test and interpreted as snapshots unless time-series measurements are collected.

## Conclusion

The H2 experiment successfully demonstrated horizontal scaling by running two Django application instances behind Nginx.

The workload was distributed across both instances, and both containers actively processed requests under load. The setup achieved 29.60 RPS with zero failed requests.

Although the H2 setup did not outperform the V2 vertical scaling configuration in this particular benchmark, it demonstrated the fundamental concept of horizontal scaling: distributing application workload across multiple instances through a load balancer.

Horizontal scaling becomes particularly valuable when designing systems that need to distribute traffic, scale out by adding instances, and reduce dependence on a single application instance. In a real production architecture, additional considerations such as shared state, database capacity, session management, health checks, and failure handling would also be important.
