# IP Hash Load Balancing

## Configuration

- **Algorithm:** IP Hash
- **Backend instances:** 3
- **Nginx directive:** `ip_hash`
- **Endpoint:** `/info`

## Test

- **Requests:** 15
- **Client:** Local machine
- **Method:** Sequential curl requests
- **Client IP:** Same source IP for all requests

## Actual Results

| Backend | Requests received | Share |
|---|---:|---:|
| backend-1 | 15 | 100% |
| backend-2 | 0 | 0% |
| backend-3 | 0 | 0% |
| **Total** | **15** | **100%** |

- **Unique backends:** 1

## Observations

- All 15 requests from the same client were routed to `backend-1`.
- IP Hash uses the client's IP address to determine backend selection.
- Requests from the same client IP are generally routed to the same backend while the backend pool remains unchanged.
- Different client IPs can be mapped to different backends.
- Clients