# Weighted Round Robin Load Balancing

## Experiment A — Equal Weights

**Configuration**

| Backend | Weight |
|---|---:|
| backend-1 | 1 |
| backend-2 | 1 |
| backend-3 | 1 |

**Test**
- Requests: 90
- Method: Sequential curl requests
- Endpoint: `/info`

**Expected Distribution**

| Backend | Expected count | Expected share |
|---|---:|---:|
| backend-1 | 30 | 33.33% |
| backend-2 | 30 | 33.33% |
| backend-3 | 30 | 33.33% |

**Actual Results**

| Backend | Actual count | Actual share |
|---|---:|---:|
| backend-1 | 29 | 32.22% |
| backend-2 | 29 | 32.22% |
| backend-3 | 32 | 35.56% |

## Experiment B — Unequal Weights

**Configuration**

| Backend | Weight |
|---|---:|
| backend-1 | 10 |
| backend-2 | 1 |
| backend-3 | 1 |

**Test**
- Requests: 90
- Method: Sequential curl requests
- Endpoint: `/info`

**Expected Distribution**

| Backend | Expected share |
|---|---:|
| backend-1 | 83.33% |
| backend-2 | 8.33% |
| backend-3 | 8.33% |

**Actual Results**

| Backend | Actual count | Actual share |
|---|---:|---:|
| backend-1 | 76 | 84.44% |
| backend-2 | 9 | 10.00% |
| backend-3 | 5 | 5.56% |

## Experiment C — Different Capacity Ratios

**Configuration**

| Backend | Weight |
|---|---:|
| backend-1 | 2 |
| backend-2 | 4 |
| backend-3 | 6 |

**Test**
- Requests: 90
- Method: Sequential curl requests
- Endpoint: `/info`

**Expected Distribution**

| Backend | Expected count | Expected share |
|---|---:|---:|
| backend-1 | 15 | 16.67% |
| backend-2 | 30 | 33.33% |
| backend-3 | 45 | 50.00% |

**Actual Results**

| Backend | Actual count | Actual share |
|---|---:|---:|
| backend-1 | 15 | 16.67% |
| backend-2 | 29 | 32.22% |
| backend-3 | 46 | 51.11% |

## Observations

- Equal weights distribute requests approximately equally.
- Increasing a backend's weight increases its share of incoming requests.
- Nginx weights are manually configured.
- Nginx does not automatically change weights based on CPU or memory usage.
- Weights control request distribution, not actual processing speed.
- The actual distribution can differ slightly from the theoretical ratio.

## Conclusion

Weighted Round Robin is useful when backend servers have different capacities and we want to control their relative traffic share.

It improves on standard Round Robin by allowing higher-capacity servers to receive