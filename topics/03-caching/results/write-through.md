# Write-Through Caching

## Implementation

- Updated the database first.
- Updated Redis after the database transaction committed.
- Used the existing product cache key.

## Verification

- Updated product price through the write-through endpoint.
- Verified the updated value in Redis.
- Confirmed the next read returned a cache hit.

## Limitation

The database and Redis do not share an atomic transaction.
A Redis failure after database commit can leave stale cache data.