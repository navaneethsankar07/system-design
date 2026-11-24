# Power of Two Choices Load Balancing

## Configuration

- **Algorithm:** Power of Two Choices
- **Backend instances:** 3
- **Nginx directive:** `random two least_conn`
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
| backend-1 | 22 | 36.67% |
| backend-2 | 17 | 28.33% |
| backend-3 | 21 | 35.00% |
| **Total** | **60** | **100%** |

## Comparison with Least Connections

| Backend | Least Connections | Power of Two Choices |
|---|---:|---:|
| backend-1 | 19 | 22 |
| backend-2 | 21 | 17 |
| backend-3 | 20 | 21 |

Both algorithms produced a reasonably balanced distribution in these experiments. The results are close, and a single run is not enough to conclude that one algorithm is better.

## Observations

- Nginx randomly selects two backend servers.
- It compares the active connection counts of the selected servers.
- The backend with fewer active connections is preferred.
- It does not need to compare all backend servers for every selection.
- Results depend on request timing, concurrency, and random selection.
- The distribution was reasonably balanced across the three backends in this test.

## Conclusion

Power of Two Choices combines random selection with connection-aware routing. It can provide good load distribution while comparing only two randomly selected backends instead of considering the entire backend pool. In this experiment, it produced a reasonably balanced distribution similar to the earlier Least Connections test.