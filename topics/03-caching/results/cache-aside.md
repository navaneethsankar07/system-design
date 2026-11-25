# Cache-Aside Implementation

## Strategy

Implemented Cache-Aside using Django and Redis.

## First Request

- Cache lookup: Miss
- Database query: Yes
- Redis write: Yes

## Second Request

- Cache lookup: Hit
- Database query: No
- Redis write: No

## Redis Key

`product:1`

## Observations

- The application checks Redis before querying the database.
- Missing data is retrieved from SQLite and stored in Redis.
- Subsequent requests can reuse the cached result.
- Cache expiration and invalidation will be tested in later phases.