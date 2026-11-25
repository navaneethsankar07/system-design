# Baseline Performance — Without Caching

## Configuration

- Application: Django
- Database: SQLite
- Cache: Disabled
- Virtual Users: 20
- Test Duration: 30 seconds
- Endpoint: `GET /products/1/`

## Results

| Metric | Actual Result |
|---|---:|
| Total Requests | 9,406 |
| Requests/sec | 313.22 |
| Average Response Time | 63.68 ms |
| Median Response Time | 62.84 ms |
| p95 Response Time | 84.01 ms |
| p99 Response Time | Not reported |
| Failed Requests | 0 (0%) |

## Observations

- Every request retrieves the product from SQLite.
- No Redis cache lookup is performed.
- All 9,406 requests completed successfully.
- Average response time was 63.68 ms.
- The p95 response time was 84.01 ms.
- Throughput reached approximately 313.22 requests per second.
- These results will serve as the baseline for comparison with Redis caching.

## Additional Metrics

| Metric | Actual Result |
|---|---:|
| Minimum Response Time | 32.04 ms |
| Maximum Response Time | 1.04 s |
| p90 Response Time | 76.22 ms |
| Checks Passed | 9,406 (100%) |
| Checks Failed | 0 (0%) |
