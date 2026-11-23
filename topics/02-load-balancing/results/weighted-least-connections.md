# Weighted Least Connections Load Balancing

## Configuration

| Backend | Weight |
|---|---:|
| backend-1 | 2 |
| backend-2 | 1 |
| backend-3 | 1 |

- **Algorithm:** Weighted Least Connections
- **Nginx directive:** `least_conn`
- **Endpoint:** `/work?delay=2`

## Test

- **Total requests:** 60
- **Concurrent requests:** 30
- **Request delay:** 2 seconds
- **Method:** Parallel curl requests using `xargs`

## Actual Results

| Backend | Requests received | Share |
|---|---:|---:|
| backend-1 | 29 | 48.33% |
| backend-2 | 16 | 26.67% |
| backend-3 | 15 | 25.00% |
| **Total** | **60** | **100%** |

## Observations

- Nginx considers active connections and configured server weights when selecting a backend.
- The higher-weight backend received more requests in this experiment.
- The distribution depends on the current connection load and request timing.
- The results do not have to match the weight ratio exactly.
- Backend-1 received approximately 48.33% of requests, while the other two received approximately 26.67% and 25%.

## Conclusion

Weighted Least Connections is useful when backend servers have different capacities and we also need to consider their current connection load. Server weights influence backend selection, while active connection counts help account for current load.