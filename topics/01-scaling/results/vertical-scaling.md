# Vertical Scaling Experiment

## Objective

Study the effect of increasing resources allocated to a single Django application instance and observe how CPU allocation and Gunicorn worker count affect throughput and latency.

## Configurations

| Test | CPU limit | Memory | Gunicorn workers | Instances |
|---|---:|---:|---:|---:|
| Baseline | 1 CPU | 512 MB | 1 | 1 |
| V1 | 2 CPUs | 512 MB | 1 | 1 |
| V2 | 2 CPUs | 512 MB | 2 | 1 |

## V1 Results

| Metric | Baseline | V1 |
|---|---:|---:|
| Total requests | 455 | 547 |
| RPS | 14.84 | 17.93 |
| Average latency | 666.86 ms | 553.02 ms |
| p50 | 687.89 ms | 550.06 ms |
| p90 | 777.53 ms | 602.54 ms |
| p95 | 871.69 ms | 610.58 ms |
| p99 | 1.21 s | 631.64 ms |
| Failed requests | 0 | 0 |

## V1 Resource Observation

| Metric | V1 |
|---|---:|
| CPU snapshot during load | 121.81% |
| Memory snapshot during load | 82.05 MiB |
| Memory limit | 512 MiB |

> These are individual snapshots, not averages or peaks.

## V1 Analysis

Compared with the baseline:

- Throughput increased by approximately **20.8%**.
- Average latency decreased by approximately **17.1%**.
- p95 latency decreased by approximately **30.0%**.
- p99 latency decreased by approximately **47.8%**.
- No failed requests were recorded.

Increasing the CPU limit from 1 CPU to 2 CPUs improved the performance observed in this particular test. However, this does not isolate CPU allocation as the only cause of the improvement.

## V2 Results

V2 used 2 CPUs, the same 512 MB memory limit, and increased Gunicorn workers from 1 to 2.

| Metric | Baseline | V1 | V2 |
|---|---:|---:|---:|
| Total requests | 455 | 547 | 963 |
| RPS | 14.84 | 17.93 | 31.76 |
| Average latency | 666.86 ms | 553.02 ms | 312.88 ms |
| p50 | 687.89 ms | 550.06 ms | 311.59 ms |
| p90 | 777.53 ms | 602.54 ms | 349.93 ms |
| p95 | 871.69 ms | 610.58 ms | 375.42 ms |
| p99 | 1.21 s | 631.64 ms | 443.50 ms |
| Max latency | 1.24 s | 637.35 ms | 500.07 ms |
| Failed requests | 0 | 0 | 0 |

## V2 Analysis

Compared with V1:

- Throughput increased by approximately **77.2%**.
- Average latency decreased by approximately **43.5%**.
- p95 latency decreased by approximately **38.5%**.
- p99 latency decreased by approximately **29.8%**.
- No failed requests were recorded.

Compared with the baseline:

- Throughput increased by approximately **114.0%** (about 2.14×).
- Average latency decreased by approximately **53.1%**.
- p95 latency decreased by approximately **56.9%**.
- All requests succeeded in all three tests.

The two Gunicorn workers allowed the application to handle multiple requests concurrently. Since the workload is CPU-intensive, multiple workers could also execute CPU-bound requests across the available CPU quota, subject to the container's CPU limit.

## Resource Observations

| Metric | V1 |
|---|---:|
| CPU snapshot during load | 121.81% |
| Memory snapshot during load | 82.05 MiB |
| Memory limit | 512 MiB |

V2 resource observations were not recorded in the available results. Therefore, a direct comparison of CPU and memory utilization between V1 and V2 cannot be made.

## Key Learnings

- Vertical scaling increases the resources allocated to a single application instance.
- Increasing CPU allocation alone showed a performance improvement in V1.
- Gunicorn worker count significantly affected throughput in this CPU-intensive workload.
- A single synchronous Gunicorn worker handles one request at a time, while multiple workers allow multiple requests to be processed concurrently.
- More workers do not always mean better performance; the appropriate number depends on workload, CPU capacity, memory, and application behavior.
- Throughput and latency should be analyzed together when evaluating performance.
- Resource utilization should be measured during load testing and preferably recorded over time, rather than relying on a single snapshot.
- Performance results from a local Docker environment may vary because the host also runs the load generator and other processes.

## Conclusion

Vertical scaling improved the performance of the Django application in the experiments conducted.

Increasing the CPU limit from 1 CPU to 2 CPUs resulted in a moderate improvement, while increasing Gunicorn workers from 1 to 2 produced a much larger improvement in throughput and latency under the tested workload.

These results demonstrate that vertical scaling can improve application performance, but its effectiveness depends on resource allocation, application concurrency, and workload characteristics. Vertical scaling also has practical limits because a single machine cannot be scaled indefinitely.

