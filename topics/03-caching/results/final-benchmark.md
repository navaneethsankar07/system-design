# Final Caching Benchmark

## Configuration

- Application: Django
- Database: SQLite
- Cache: Redis
- Load Testing Tool: Grafana k6
- Virtual Users: 20
- Duration: 30 seconds
- Endpoint: `GET /products/1/`
- Baseline Endpoint: `GET /products/1/?cache=off`
- Cached Endpoint: `GET /products/1/`

## Performance Results

| Metric | Without Cache | With Cache |
|---|---:|---:|
| Total Requests | 9,562 | 13,744 |
| Requests/sec | 318.36 | 457.51 |
| Average Response Time | 62.67 ms | 43.54 ms |
| Median Response Time | 62.93 ms | 42.80 ms |
| p95 Response Time | 75.92 ms | 46.71 ms |
| p99 Response Time | Not reported | Not reported |
| Failed HTTP Requests | 0 | 0 |

## Database Query Comparison

| Test | Database Lookup Attempts |
|---|---:|
| Without Cache | 9,562 |
| With Cache | 10 |

The database lookup counter recorded 9,562 lookups during the uncached test and only 10 during the cached test.

This represents an approximately **99.90% reduction in database lookup attempts**.

## Observations

- Both benchmark tests completed with zero failed HTTP requests.
- Redis caching increased measured request throughput from 318.36 requests/sec to 457.51 requests/sec, an improvement of approximately 43.71%.
- Average response time decreased by approximately 30.52%.
- Median response time decreased by approximately 31.99%.
- p95 response time decreased by approximately 38.47%.
- Database lookup attempts decreased from 9,562 to 10, representing an approximately 99.90% reduction.
- The cached test recorded 13,734 cache hits out of 13,744 requests, giving a cache-hit rate of approximately 99.93%.
- The remaining 10 requests were cache misses, consistent with concurrent requests reaching the endpoint before the cache was populated.
- The p99 response time was not reported by these benchmark outputs and is therefore not included.

## Conclusion

Under the tested conditions of 20 virtual users and a 30-second test duration, Redis caching improved the measured performance of the product detail endpoint.

The cached implementation achieved approximately 43.71% higher throughput and reduced average response time by approximately 30.52%. It also reduced database lookup attempts by approximately 99.90%.

These results demonstrate the benefits of Redis caching for this endpoint under the tested local workload. However, they represent individual benchmark runs on a local development environment and should not be treated as universal performance guarantees.