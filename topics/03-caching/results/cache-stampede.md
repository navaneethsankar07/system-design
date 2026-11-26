# Cache Stampede Prevention Results

## Objective

Understand the cache stampede problem and evaluate how Redis locking prevents multiple concurrent requests from performing the same database lookup when a cache entry expires or is missing.

## Experiment Setup

- **Application:** Django
- **Cache:** Redis
- **Load testing tool:** Grafana k6
- **Virtual users:** 50
- **Total iterations:** 50
- **Simulated database lookup delay:** 1 second
- **Product endpoint:** `/products/1/`
- **Database lookup measurement:** Redis counter (`metrics:product_db_loads`)

The application increments the Redis counter immediately before executing the product database lookup.

## Results

### Without Redis Locking

| Metric | Result |
|---|---:|
| Virtual users | 50 |
| Total requests | 50 |
| Database lookups | 18 |
| Average response time | 723.03 ms |
| Median response time | 1.03 s |
| p90 response time | 1.24 s |
| p95 response time | 1.25 s |
| Maximum response time | 1.25 s |
| Failed requests | 0 |

**Observation:** Multiple concurrent requests encountered the cache miss and performed duplicate database lookups.

### With Redis Locking

| Metric | Result |
|---|---:|
| Virtual users | 50 |
| Total requests | 50 |
| Database lookups | 1 |
| Average response time | 750.77 ms |
| Median response time | 1.04 s |
| p90 response time | 1.22 s |
| p95 response time | 1.23 s |
| Maximum response time | 1.23 s |
| Failed requests | 0 |

**Observation:** Only one request performed the database lookup. The other requests used the cached result after it was populated.

## Comparison

| Metric | Without Lock | With Lock |
|---|---:|---:|
| Database lookups | 18 | 1 |
| Average response time | 723.03 ms | 750.77 ms |
| Median response time | 1.03 s | 1.04 s |
| p95 response time | 1.25 s | 1.23 s |
| Failed requests | 0 | 0 |

### Database Lookup Reduction

\[
\frac{18-1}{18}\times100=94.44\%
\]

Redis locking reduced the measured product database lookup attempts from 18 to 1, representing a **94.44% reduction** in this experiment.

## Key Learnings

1. A cache stampede occurs when multiple concurrent requests encounter the same cache miss and independently query the database.
2. Redis locking allows one request to load the missing data while other requests wait for the cache to be populated.
3. Rechecking the cache after acquiring or waiting for the lock prevents unnecessary database lookups.
4. Measuring database lookup attempts provides stronger evidence of stampede prevention than relying on response times alone.
5. Reducing database lookups does not necessarily mean that response latency will improve, because concurrent requests may still wait for the cache to be populated.

## Limitations

- The one-second delay is artificially introduced to simulate a slow database lookup.
- The Redis counter measures product lookup attempts, not total database CPU, memory, disk I/O, or all SQL queries.
- Only one run per configuration was recorded, so additional runs are needed for stronger conclusions.
- The benchmark uses a single product ID and a local Docker environment.

## Conclusion

Redis locking successfully reduced duplicate product database lookups during concurrent cache misses in this experiment.

Without locking, 18 database lookups occurred. With locking, only one lookup occurred. This demonstrates how distributed locking can help prevent cache stampedes and reduce unnecessary database work.
