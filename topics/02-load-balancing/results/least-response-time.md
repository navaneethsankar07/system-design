# Least Response Time — Experiment and Nginx Limitation

## Concept

Least Response Time selects a backend using observed response-time information, often combined with active connections.

## Implementation Limitation

- **Current load balancer:** Nginx Open Source (`nginx:alpine`)
- **Nginx Plus directive:** `least_time`
- **Availability:** Not supported by Nginx Open Source

A direct `least_time` configuration cannot be used with the current Nginx image.

## Test

- **Backend instances:** 3
- **Endpoint:** `/work`
- **Test duration:** 10 requests per backend
- **Method:** Direct curl requests
- **Requested delay:** 1 second per request

## Actual Results

| Backend | Requested delay | Average measured response time |
|---|---:|---:|
| backend-1 | 1 second | 1.004031 seconds |
| backend-2 | 1 second | 1.004075 seconds |
| backend-3 | 1 second | 1.007482 seconds |

## Additional Test — Different Processing Delays

Each backend was tested once with a different requested delay.

| Backend | Requested delay | Measured response time |
|---|---:|---:|
| backend-1 | 1 second | 1.001812 seconds |
| backend-2 | 2 seconds | 2.002051 seconds |
| backend-3 | 3 seconds | 3.002700 seconds |

## Observations

- All three backends had similar average response times when processing requests with the same one-second delay.
- Backend-1 had an average response time of approximately 1.004 seconds.
- Backend-2 had an average response time of approximately 1.004 seconds.
- Backend-3 had an average response time of approximately 1.007 seconds.
- Different processing delays produced different response times.
- Actual response times include network and application overhead.
- Nginx Open Source does not provide the `least_time` upstream directive.
- Measuring response time is not the same as implementing response-time-aware routing.

## Conclusion

Least Response Time can help route traffic toward faster backends. However, implementing this algorithm with Nginx requires Nginx Plus or a separate custom load-balancing implementation.

This experiment demonstrates how different processing delays affect backend response times without claiming that Nginx Open Source automatically routes requests based on response time.