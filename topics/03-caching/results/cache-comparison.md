# Performance Comparison

## Test Configuration

- Virtual Users: 20
- Duration: 30 seconds
- Endpoint: `GET /products/1/`
- Database: SQLite
- Cache: Redis
- Cache TTL: 60 seconds

## Results

| Metric | Without Cache | With Cache |
|---|---:|---:|
| Total Requests | 9,406 | 13,508 |
| Requests/sec | 313.22 | 449.64 |
| Average Response Time | 63.68 ms | 44.27 ms |
| Median Response Time | 62.84 ms | 42.91 ms |
| p95 Response Time | 84.01 ms | 47.87 ms |
| p99 Response Time | Not reported | Not reported |
| Failed Requests | 0 (0%) | 0 (0%) |

## Observations

- Without caching, the application handled 313.22 requests/sec.
- With Redis caching, throughput increased to 449.64 requests/sec.
- Average response time decreased from 63.68 ms to 44.27 ms.
- p95 response time decreased from 84.01 ms to 47.87 ms.
- Both tests completed with zero failed HTTP requests.
- The cached benchmark's `X-Cache: HIT` check passed for all 13,508 requests.
- Redis caching reduced repeated database queries for this frequently requested product.

## Performance Improvement

- Throughput increased by approximately 43.6%.
- Average response time decreased by approximately 30.5%.
- p95 response time decreased by approximately 43.0%.

## Conclusion

Redis caching improved throughput and reduced response times in this experiment. Since the same product was repeatedly requested and already cached before the second benchmark, requests could be served from Redis instead of querying SQLite each time.

These results represent this specific local test setup and workload, not a guaranteed improvement for every application.
