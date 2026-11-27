# CDN Practical — Experimental Results

## Environment

- Origin: Django + Gunicorn
- Edge: Nginx 1.27
- Deployment: Local Docker containers
- Benchmark duration: 10 seconds
- Concurrency: 20 workers

## Cache behaviour

| Experiment | Observed result |
|---|---|
| First cache request | MISS |
| Repeated cache request | HIT |
| Expired cached response | EXPIRED |
| Health endpoint | BYPASS |
| Static asset | Served by Nginx |

## Benchmark

| Metric | Result |
|---|---:|
| Total requests | 57,165 |
| Duration | 9.94 seconds |
| Throughput | 5,749.27 req/s |
| Average latency | 3.47 ms |
| Median latency | 2.26 ms |
| P95 latency | 8.44 ms |
| Failures | 0 |
| Cache HIT | 57,165 |
| Cache MISS | 0 |

## Interpretation

The benchmark warmed the cache before measurement.
All measured requests were cache hits.

These results demonstrate the performance of the local
Nginx cached path under this particular test.

They do not establish a quantified improvement over
direct Django requests or a geographically distributed CDN.

## Limitations

- Single local Nginx edge instance.
- No geographic distribution.
- No real CDN provider.
- No direct-origin benchmark comparison.
- Results depend on local hardware and environment.
