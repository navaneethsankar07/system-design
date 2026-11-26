# Caching

A hands-on exploration of caching concepts, caching strategies, cache consistency, and performance optimization using Django and Redis.

## Objectives

- Understand caching and its importance in system design.
- Implement Cache-Aside and Write-Through strategies.
- Understand cache hits, misses, and TTL.
- Explore cache invalidation and stale data.
- Understand cache consistency.
- Simulate cache stampede, penetration, and avalanche.
- Benchmark application performance with and without caching.

## Architecture

```text
              Client
                 |
                 v
          Django Application
                 |
          +------+------+
          |             |
          v             v
       Redis          SQLite
       Cache          Database
```

## Technology Stack

- Python
- Django
- Redis
- Docker
- Docker Compose
- k6
- SQLite

## Implemented Concepts

- [x] Cache-Aside
- [x] Cache Hits and Misses
- [x] TTL and Expiration
- [x] Cache Invalidation
- [x] Write-Through
- [x] Cache Stampede and Redis Locking
- [x] Cache Penetration and Negative Caching
- [x] Cache Avalanche and TTL Jitter
- [x] Performance Benchmarking

## Cache Consistency

Cache consistency refers to keeping cached data synchronized with the primary database.

### Strong Consistency

Strong consistency ensures that every read returns the latest committed data.

When a database record is updated, the cache must also be updated or invalidated before subsequent reads are allowed to return potentially stale data.

This provides stronger consistency but can introduce additional latency and coordination overhead.

### Eventual Consistency

Eventual consistency allows the cache and database to temporarily contain different values.

After a database update, the cache may continue serving the old value until it is updated, invalidated, or expires.

Eventually, both systems converge to the latest data, assuming updates and invalidations complete successfully.

### How Database Updates Affect Cached Data

Consider a product whose price is stored in both SQLite and Redis.

1. The application reads the product from Redis.
2. If the cache contains the product, the application returns the cached value.
3. If the product is updated in the database without updating or invalidating Redis, subsequent requests may receive stale data.
4. Cache invalidation removes the outdated cache entry so the next request fetches the latest database value.
5. Write-Through updates the database and cache as part of the write operation.

**Key takeaway:** Cache invalidation and cache-update strategies are important for preventing stale data and maintaining consistency between the cache and the database.

## Running the Project

### Start Services

```bash
docker compose up -d --build
```

### Check Services

```bash
docker compose ps
```

### Test the API

```bash
curl -i http://localhost:8000/products/1/
```

Check the `X-Cache` response header:

- `MISS`: The product was fetched from the database and cached.
- `HIT`: The product was served from Redis.

Run the request again to observe a cache hit.

### Check Redis

```bash
docker exec caching-redis redis-cli ping
```

Expected output:

```text
PONG
```

Inspect Redis keys during development:

```bash
docker exec caching-redis redis-cli KEYS '*'
```

### Stop Services

```bash
docker compose down
```

## Experiments and Results

- [Baseline Performance](results/baseline.md)
- [Cache-Aside](results/cache-aside.md)
- [Cache Invalidation](results/cache-invalidation.md)
- [Write-Through](results/write-through.md)
- [Cache Stampede](results/cache-stampede.md)
- [Cache Penetration and Avalanche](results/cache-penetration-avalanche.md)
- [Performance Comparison](results/final-benchmark.md)

## Key Learnings

- Caching reduces repeated database access by storing frequently requested data in a faster storage system.
- Cache-Aside loads data into Redis only when it is not already available in the cache.
- Cache hits avoid unnecessary database lookups, while cache misses require fetching data from the database.
- TTL automatically expires cache entries and helps prevent outdated data from remaining indefinitely.
- Cache invalidation is essential when database records are modified.
- Write-Through keeps the cache updated during write operations, reducing the chance of serving stale cached values.
- Redis locking can help prevent multiple concurrent requests from performing the same expensive database operation during a cache miss.
- Negative caching stores information about missing records temporarily to reduce repeated database lookups for nonexistent resources.
- TTL jitter distributes cache expiration times and helps reduce the risk of simultaneous cache expirations.
- Performance benchmarking with k6 helps measure throughput, response times, and the impact of caching.
- Caching introduces consistency and invalidation challenges, so it should be implemented according to the application's requirements.

## Final Benchmark Summary

Under the tested conditions of 20 virtual users and a 30-second benchmark:

- Throughput increased from approximately 318.36 to 457.51 requests/sec.
- Average response time decreased from 62.67 ms to 43.54 ms.
- Database lookup attempts decreased from 9,562 to 10.
- Both benchmark tests recorded zero failed HTTP requests.

These results demonstrate the performance benefits of Redis caching for the tested product endpoint under the measured local workload.