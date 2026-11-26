# Cache Penetration and Cache Avalanche

## Cache Penetration

### Problem

Cache penetration occurs when requests for nonexistent records repeatedly bypass the cache and query the database. This can cause unnecessary database load, especially when the same nonexistent records are requested repeatedly.

### Solution

Implemented **negative caching** using a special Redis value (`__NOT_FOUND__`) with a 30-second TTL.

When a requested product does not exist, the application stores the special value in Redis instead of repeatedly querying the database.

### Verification

Tested using the nonexistent product ID `999999`.

| Test | Result |
|---|---|
| First request | HTTP 404, `X-Cache: MISS` |
| Second request | HTTP 404, `X-Cache: HIT` |
| Database lookups across both requests | 1 |
| Negative-cache value | `__NOT_FOUND__` |
| Negative-cache TTL | 30 seconds when written |

### Observation

The first request queried the database, found no matching product, and stored the negative result in Redis.

The second request retrieved the cached negative result and returned HTTP 404 without querying the database again.

This verifies that negative caching prevents repeated database lookups for the same nonexistent product while the negative-cache entry remains valid.

**Limitation:** Negative cache entries expire after 30 seconds. If a product is created during that period, its negative-cache entry must be invalidated to prevent the application from continuing to return a cached 404.

---

## Cache Avalanche

### Problem

A cache avalanche occurs when many cache entries expire around the same time, potentially causing a sudden increase in database requests as applications attempt to reload expired data.

### Solution

Implemented **TTL jitter** by adding a random value between 0 and 30 seconds to the normal cache TTL.

The effective TTL is:

`CACHE_TTL + random.randint(0, TTL_JITTER)`

Configuration:

| Setting | Value |
|---|---:|
| `CACHE_TTL` | 60 seconds |
| `TTL_JITTER` | 30 seconds |
| Minimum possible TTL | 60 seconds |
| Maximum possible TTL | 90 seconds |

The jitter range is configurable through the `CACHE_TTL_JITTER` environment variable, which defaults to 30 seconds.

### Verification

Created 100 product cache entries by sending requests to product IDs from 1 to 100. Then inspected their remaining TTLs using Redis.

**Latest Measurement**

| Metric | Result |
|---|---:|
| Product keys | 100 |
| Cached keys with positive TTL | 100 |
| Minimum remaining TTL | 55 seconds |
| Maximum remaining TTL | 86 seconds |
| Unique remaining TTL values | 32 |

Observed TTL distribution:

`[55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86]`

### Earlier Measurements

| Measurement | Cached Keys | Minimum TTL | Maximum TTL | Unique TTL Values |
|---|---:|---:|---:|---:|
| First | 100 | 52s | 52s | 1 |
| Second | 100 | 25s | 66s | 3 |
| Latest | 100 | 55s | 86s | 32 |

The earlier measurements showed identical or limited TTL variation. The latest measurement, after rebuilding the web container and checking the configuration, showed a much wider distribution.

### Observations

- All 100 product cache entries had positive TTL values.
- The remaining TTLs ranged from 55 to 86 seconds.
- There were 32 distinct remaining TTL values.
- The configured base TTL was 60 seconds, with up to 30 seconds of random jitter.
- The latest result demonstrates that cache entries no longer all have the same expiration time.

This helps spread cache expiration over a wider time window instead of allowing many entries to expire together.

**Limitation:** This test verifies TTL distribution, not a reduction in database load during an actual cache avalanche. A separate concurrent-load test would be needed to measure that effect.

---

## Conclusion

Implemented and verified two caching protection techniques:

1. **Cache Penetration Prevention:** Negative caching stores nonexistent-product results in Redis for 30 seconds, preventing repeated database lookups for the same missing product while the entry remains valid.
2. **Cache Avalanche Mitigation:** TTL jitter adds a random 0–30 seconds to the normal 60-second cache TTL, distributing expiration times across a wider window.

The negative-caching test confirmed that two requests for the same nonexistent product resulted in only one database lookup. The latest TTL test confirmed that 100 product cache entries had 32 distinct remaining TTL values.

These implementations demonstrate how Redis caching strategies can reduce unnecessary database requests and help avoid synchronized cache expiration.