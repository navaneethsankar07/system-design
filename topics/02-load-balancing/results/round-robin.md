
# Round Robin Load Balancing

## Configuration
- Load balancer: Nginx
- Backend instances: 3
- Algorithm: Round Robin
- Backend weights: Equal

## Distribution Test

Sent 30 sequential requests to `/info`.

| Backend | Requests | Percentage |
|---|---:|---:|
| backend-1 | 10 | 33.33% |
| backend-2 | 10 | 33.33% |
| backend-3 | 10 | 33.33% |
| Total | 30 | 100% |

## k6 Performance Test

- Virtual users: 10
- Duration: 30 seconds
- Total requests: 192,240
- Throughput: 6,407.33 req/s
- Average response time: 1.46 ms
- p95 response time: 2.68 ms
- Failed requests: 0

## Observations

- Nginx distributed requests equally across the three backends.
- Round Robin does not consider backend CPU usage or current workload.
- Equal request distribution does not necessarily mean equal workload.
- The k6 test measured endpoint performance, not per-backend distribution.

## Conclusion

Round Robin is a simple load-balancing algorithm that distributes requests sequentially across available backend servers.

It works well when backend capacities and request processing costs are relatively similar.
