
# Baseline Experiment

## 1. Objective

Measure the performance of a single Django application container under concurrent load before experimenting with vertical and horizontal scaling.

## 2. Configuration

| Setting | Value |
|---|---|
| Application instances | 1 |
| CPU limit | 1 CPU |
| Memory limit | 512 MB |
| Gunicorn workers | 1 |
| Gunicorn threads | 1 |
| Virtual users | 10 |
| Test duration | 30 seconds |
| Endpoint | `/api/work/` |
| Iterations per request | 1,000,000 |
| Load testing tool | k6 |

## 3. Results

| Metric | Measured value |
|---|---:|
| Total requests | 455 |
| Requests per second | 14.84 |
| Average latency | 666.86 ms |
| Minimum latency | 51.03 ms |
| Median (p50) latency | 687.89 ms |
| p90 latency | 777.53 ms |
| p95 latency | 871.69 ms |
| p99 latency | 1.21 seconds |
| Maximum latency | 1.24 seconds |
| Failed requests | 0 |
| Successful checks | 455 / 455 (100%) |

## 4. Resource Usage

Docker stats snapshot:

| Metric | Observed value |
|---|---:|
| Application CPU usage | 101.45% |
| Application memory usage | 52.09 MiB |
| Memory limit | 512 MiB |
| Memory utilization | 10.17% |

Note: Resource values are from a single Docker stats snapshot, not average or peak measurements.

## 5. Observations

- The application successfully handled 455 requests during the 30-second test.
- All HTTP checks passed, and no failed requests were recorded.
- Throughput was approximately 14.84 requests per second.
- Average response latency was approximately 667 ms.
- The p99 latency was approximately 1.21 seconds, meaning 99% of recorded requests completed within that time.
- CPU usage was approximately 100%, indicating that the application was close to its configured CPU limit at the time of the snapshot.
- Memory usage was relatively low at approximately 10.17% of the configured memory limit.

## 6. Initial Bottleneck Analysis

CPU appears to be the primary resource bottleneck in this experiment.

The application was using nearly all of its allocated CPU capacity, while memory usage remained relatively low.

This suggests that increasing available CPU resources or distributing incoming requests across multiple application instances may improve throughput.

However, this is an initial hypothesis. We need additional experiments to verify it.

## 7. Limitations

- This experiment uses one application instance.
- The load generator and application run on the same machine, so they share host resources.
- CPU and memory measurements are a single snapshot rather than time-series measurements.
- Results represent a local experiment, not production capacity.

## 8. Conclusion

The single-instance Django application handled 455 requests at approximately 14.84 requests per second, with an average latency of 666.86 ms and no failed requests.

CPU utilization was close to the configured limit, making CPU capacity a likely bottleneck.

This baseline will be used to compare the performance improvements achieved through vertical and horizontal scaling.
