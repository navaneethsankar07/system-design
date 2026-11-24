# Consistent Hashing Load Balancing

## Configuration

- **Algorithm:** Consistent Hashing
- **Backend instances:** 3
- **Nginx directive:** `hash $request_uri consistent`
- **Hash key:** Request URI
- **Endpoint:** `/info`

## Test A — Same Key

- **Requests:** 15
- **Key:** `user-100`
- **Method:** Sequential curl requests

### Actual Results

| Backend | Requests received | Share |
|---|---:|---:|
| backend-1 | 0 | 0% |
| backend-2 | 15 | 100% |
| backend-3 | 0 | 0% |
| **Total** | **15** | **100%** |

- **Unique backends:** 1

All 15 requests using the same key were routed to `backend-2`.

## Test B — Different Keys

- **Requests:** 60
- **Keys:** `user-1` to `user-60`
- **Method:** Sequential curl requests

### Actual Results

| Backend | Requests received | Share |
|---|---:|---:|
| backend-1 | 26 | 43.33% |
| backend-2 | 10 | 16.67% |
| backend-3 | 24 | 40.00% |
| **Total** | **60** | **100%** |

## Observations

- All 15 requests with the same key (`user-100`) consistently reached backend-2.
- Different keys were distributed across all three backends.
- The distribution of different keys was uneven: backend-1 received 26, backend-2 received 10, and backend-3 received 24.
- Consistent hashing maps keys to backends based on the hash value.
- Consistent hashing helps reduce key remapping when backend membership changes, compared with ordinary hashing strategies.
- Distribution depends on the keys and the backend pool.

## Conclusion

Consistent Hashing is useful when related requests should reach the same backend, such as caching systems and applications that partition data using stable keys.

This experiment demonstrated consistent routing for the same key and distribution across multiple backends for different keys. The distribution was not perfectly equal, which is expected with hash-based assignment.