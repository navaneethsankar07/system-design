# Load Balancing Algorithm Benchmark Comparison

## Benchmark Configuration

- **Backend instances:** 3
- **Load balancer:** Nginx
- **Load testing tool:** k6
- **Virtual users:** 30
- **Duration:** 30 seconds
- **Endpoint:** `/work?delay=0.1`

## Performance Comparison

| Algorithm | Requests/sec | Average latency | p95 latency | p99 latency | Failed requests |
|---|---:|---:|---:|---:|---:|
| Round Robin | 117.54 | 253.17 ms | 406.77 ms | 505.38 ms | 0 (0%) |
| Weighted Round Robin | 78.78 | 376.22 ms | 710.07 ms | 713.96 ms | 0 (0%) |
| Least Connections | 117.87 | 253.22 ms | 398.00 ms | 404.92 ms | 0 (0%) |
| Weighted Least Connections | 117.82 | 252.59 ms | 404.70 ms | 406.51 ms | 0 (0%) |
| IP Hash | 39.18 | 752.07 ms | 1,010 ms | 1,010 ms | 0 (0%) |
| Consistent Hashing | 39.37 | 752.40 ms | 811.09 ms | 812.53 ms | 0 (0%) |
| Random | 104.48 | 281.56 ms | 607.08 ms | 812.74 ms | 0 (0%) |
| Power of Two Choices | 111.42 | 266.34 ms | 500.06 ms | 540.14 ms | 0 (0%) |

## Individual Benchmark Results

### 1. Round Robin

- Completed requests: 3,573
- Throughput: 117.54 requests/sec
- Average latency: 253.17 ms
- p95 latency: 406.77 ms
- p99 latency: 505.38 ms
- Failed requests: 0 (0%)
- All response checks passed.

### 2. Weighted Round Robin

- Completed requests: 2,414
- Throughput: 78.78 requests/sec
- Average latency: 376.22 ms
- p95 latency: 710.07 ms
- p99 latency: 713.96 ms
- Failed requests: 0 (0%)
- All response checks passed.

### 3. Least Connections

- Completed requests: 3,569
- Throughput: 117.87 requests/sec
- Average latency: 253.22 ms
- p95 latency: 398.00 ms
- p99 latency: 404.92 ms
- Failed requests: 0 (0%)
- All response checks passed.

### 4. Weighted Least Connections

- Completed requests: 3,582
- Throughput: 117.82 requests/sec
- Average latency: 252.59 ms
- p95 latency: 404.70 ms
- p99 latency: 406.51 ms
- Failed requests: 0 (0%)
- All response checks passed.

### 5. IP Hash

- Completed requests: 1,214
- Throughput: 39.18 requests/sec
- Average latency: 752.07 ms
- p95 latency: 1,010 ms
- p99 latency: 1,010 ms
- Failed requests: 0 (0%)
- All response checks passed.

### 6. Consistent Hashing

- Completed requests: 1,210
- Throughput: 39.37 requests/sec
- Average latency: 752.40 ms
- p95 latency: 811.09 ms
- p99 latency: 812.53 ms
- Failed requests: 0 (0%)
- All response checks passed.

### 7. Random

- Completed requests: 3,225
- Throughput: 104.48 requests/sec
- Average latency: 281.56 ms
- p95 latency: 607.08 ms
- p99 latency: 812.74 ms
- Failed requests: 0 (0%)
- All response checks passed.

### 8. Power of Two Choices

- Completed requests: 3,398
- Throughput: 111.42 requests/sec
- Average latency: 266.34 ms
- p95 latency: 500.06 ms
- p99 latency: 540.14 ms
- Failed requests: 0 (0%)
- All response checks passed.

## Initial Comparison

### Round Robin vs Weighted Round Robin

Round Robin achieved higher throughput and lower latency than Weighted Round Robin in these runs.

Weighted Round Robin distributes requests according to configured weights. Its lower measured throughput does not establish that the algorithm itself is slower. Backend weights and resulting traffic distribution may have affected this result.

### Least Connections vs Weighted Least Connections

Both algorithms achieved almost identical throughput and average latency.

Weighted Least Connections completed slightly more requests, while Least Connections recorded slightly lower p95 and p99 latency.

The differences are small and should not be treated as evidence that one algorithm is consistently better.

### IP Hash vs Consistent Hashing

Both algorithms recorded almost identical throughput and average latency in these runs.

IP Hash completed 1,214 requests, while Consistent Hashing completed 1,210 requests.

Consistent Hashing recorded lower p95 and p99 latency in this particular run. However, this difference should be verified through repeated tests.

Both algorithms use key-based backend selection. With the benchmark running from a single k6 container, requests generally originate from the same client IP, which can cause IP Hash to concentrate traffic on one backend.

Consistent Hashing depends on the configured hash key. Its behavior should be interpreted based on the key and backend distribution.

### Random vs Power of Two Choices

Power of Two Choices achieved higher throughput than Random in these runs:

- Random: 104.48 requests/sec
- Power of Two Choices: 111.42 requests/sec

Power of Two Choices also recorded lower average, p95, and p99 latency.

This is consistent with the idea that comparing two randomly selected backends using their active connection counts can improve request distribution under concurrent workloads.

However, repeated tests are needed before concluding that it consistently performs better.

### Comparison Across All Algorithms

- Least Connections and Weighted Least Connections achieved approximately 118 requests/sec.
- Round Robin achieved approximately 118 requests/sec.
- Power of Two Choices achieved approximately 111 requests/sec.
- Random achieved approximately 104 requests/sec.
- Weighted Round Robin achieved approximately 79 requests/sec.
- IP Hash and Consistent Hashing achieved approximately 39 requests/sec.
- All eight benchmark runs recorded zero failed requests.

## Observations Across Completed Experiments

- All eight algorithms successfully handled their respective benchmark workloads without recorded HTTP failures.
- Least Connections, Weighted Least Connections, and Round Robin delivered similar throughput.
- Power of Two Choices performed better than Random in this particular comparison.
- Weighted Round Robin recorded lower throughput and higher latency in its observed run.
- IP Hash and Consistent Hashing recorded lower throughput and higher latency.
- Client affinity and traffic concentration may explain the lower throughput observed with IP Hash.
- Backend configuration, request distribution, system load, and benchmark variability can influence results.

## Conclusion

All eight tested load-balancing algorithms successfully handled their benchmark workloads without recording failed requests.

In these experiments, Round Robin, Least Connections, and Weighted Least Connections delivered similar throughput and latency.

Power of Two Choices performed better than Random in the observed run, with higher throughput and lower latency.

Weighted Round Robin recorded lower throughput, while IP Hash and Consistent Hashing recorded substantially lower throughput. The results for the hash-based algorithms may be influenced by client affinity and traffic concentration.

These results represent individual benchmark runs, not a universal ranking of load-balancing algorithms. Repeated tests under controlled conditions are necessary to determine whether the observed differences are consistent.

The most suitable load-balancing algorithm depends on backend capacity, request processing time, traffic patterns, session requirements, and application requirements.

## Limitations and Future Improvements

- Repeat each benchmark multiple times and compare averages.
- Keep backend resources and configurations identical across experiments.
- Record backend-level request distribution during each benchmark.
- Test with different request processing times.
- Test with different numbers of virtual users.
- Compare behavior when one backend has lower capacity.
- Measure CPU and memory utilization during load tests.
- Investigate the effect of client affinity on hash-based algorithms.

**Note:** The throughput values above are the rates reported by k6. The completed request counts and rates may not equal a simple count divided by exactly 30 seconds because k6 calculates its rate over the actual measured test duration.