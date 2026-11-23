# Least Connections Load Balancing

## Configuration

- **Algorithm:** Least Connections
- **Backend instances:** 3
- **Nginx directive:** `least_conn`
- **Endpoint:** `/work?delay=2`

## Test

- **Total requests:** 60
- **Concurrent requests:** 30
- **Request delay:** 2 seconds
- **Method:** Parallel curl requests using `xargs`
- **Load balancer:** Nginx

## Actual Results

| Backend | Requests received | Share |
|---|---:|---:|
| backend-1 | 19 | 31.67% |
| backend-2 | 21 | 35.00% |
| backend-3 | 20 | 33.33% |
| **Total** | **60** | **100%** |

## Observations

- Nginx considers the number of active connections when selecting a backend.
- A backend with fewer active connections is preferred.
- The distribution can change as requests start and finish.
- All three backends received a nearly equal number of requests in this test.
- The result is influenced by request timing and concurrency.

## Conclusion

Least Connections is useful when requests take different amounts of time to complete and backend servers may have different numbers of active connections. Unlike Round Robin, it considers the current number of active connections when selecting a backend.