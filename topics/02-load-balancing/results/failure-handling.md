# Failure Handling and Backend Health

## Configuration

- **Algorithm:** Passive Failure Detection
- **Backend instances:** 3
- **Nginx directives:** `max_fails`, `fail_timeout`, `proxy_next_upstream`
- **Failure threshold:** 2
- **Failure timeout:** 10 seconds
- **Retry attempts:** Up to 3

## Test A — Normal Operation

- **Backend status:** All three running
- **Requests:** 15
- **Method:** Sequential curl requests

### Actual Results

| Backend | Requests received | Share |
|---|---:|---:|
| backend-1 | 13 | 86.67% |
| backend-2 | 1 | 6.67% |
| backend-3 | 1 | 6.67% |
| **Total** | **15** | **100%** |

## Test B — Backend Failure

- **Stopped backend:** backend-2
- **Requests:** 30
- **Method:** Parallel curl requests using `xargs` with 10 workers

### Actual Results

| Backend | Requests received | Share |
|---|---:|---:|
| backend-1 | 14 | 46.67% |
| backend-2 | 0 | 0% |
| backend-3 | 16 | 53.33% |
| **Total** | **30** | **100%** |

### HTTP Status Summary

| Result | Count |
|---|---:|
| HTTP 200 | 30 |
| HTTP 4xx/5xx | 0 |
| Transport errors | 0 |
| Invalid responses | 0 |

## Test C — Backend Recovery

- **Restarted backend:** backend-2
- **Requests:** 15
- **Method:** Sequential curl requests

### Actual Results

| Backend | Requests received | Share |
|---|---:|---:|
| backend-1 | 5 | 33.33% |
| backend-2 | 5 | 33.33% |
| backend-3 | 5 | 33.33% |
| **Total** | **15** | **100%** |

Backend-2 successfully received requests again after being restarted.

## Observations

- During normal operation, backend-1 received most of the initial 15 requests. The small sample was not evenly distributed.
- When backend-2 was stopped, it received zero requests in the 30-request test.
- The remaining two backends handled all 30 requests successfully.
- All 30 requests returned HTTP 200, with no transport errors or invalid responses.
- After backend-2 was restarted, it received requests again.
- Passive failure detection and retry configuration help Nginx handle unavailable backends.

## Conclusion

Failure handling helps maintain service availability when a backend becomes unavailable. In this experiment, Nginx successfully routed requests to the remaining available backends when backend-2 was stopped.

After backend-2 was restarted, it started receiving requests again. This demonstrates basic backend failure and recovery behavior using Nginx passive failure handling.

However, passive health checks are not a replacement for active health monitoring, and these results do not establish recovery timing or behavior under every failure scenario.