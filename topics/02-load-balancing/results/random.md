# Random Load Balancing

## Configuration

- **Algorithm:** Random
- **Backend instances:** 3
- **Nginx directive:** `random`
- **Endpoint:** `/info`

## Test

- **Total requests:** 300
- **Method:** Sequential curl requests

## Actual Results

| Backend | Requests received | Share |
|---|---:|---:|
| backend-1 | 110 | 36.67% |
| backend-2 | 99 | 33.00% |
| backend-3 | 91 | 30.33% |
| **Total** | **300** | **100%** |

## Observations

- Nginx selects a backend randomly for each request.
- No fixed request sequence is followed.
- With equal weights, each backend has an equal selection probability.
- The expected distribution is approximately 100 requests per backend for 300 requests.
- Actual counts vary due to randomness.
- Backend-1 received the most requests, while backend-3 received the fewest in this experiment.
- Random selection does not consider active connections.

## Conclusion

Random Load Balancing is a simple approach when backend servers have similar capacities and there is no need to consider their current connection load. In this experiment, all three backends received a reasonably balanced share of the 300 requests, with some variation expected from random selection.