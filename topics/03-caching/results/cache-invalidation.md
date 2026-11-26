# Cache Invalidation

## Initial State

- Database price: 100.00
- Cached price: 100.00

## Stale Data Experiment

- Updated the database directly.
- Redis continued storing the old value.
- Application returned stale data.

## Invalidation Experiment

- Updated the product through the API.
- Database transaction committed.
- Cached product key was deleted.
- Next request fetched fresh data from the database.

## Observation

Deleting the cached entry after a successful database update
prevents subsequent requests from reading the outdated entry.