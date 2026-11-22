# 01 - Scaling

## Objective

Understand how applications handle increasing traffic using vertical and horizontal scaling.

Experiment with resource allocation, application concurrency, and load distribution to understand how scaling affects application performance.

## Concepts

- Vertical Scaling (Scale Up)
- Horizontal Scaling (Scale Out)
- Load Distribution
- Resource Utilization
- Performance Bottlenecks
- Application Concurrency
- Load Balancing

## Technology Stack

- Django
- Gunicorn
- Docker
- Docker Compose
- Nginx
- k6

## Experiments

| Experiment | Description | Status |
|---|---|---|
| Baseline | Single application instance with default resource allocation | Completed |
| Vertical Scaling | Increase CPU allocation and tune Gunicorn workers | Completed |
| Horizontal Scaling | Run multiple application instances behind a load balancer | Pending |
| Performance Comparison | Compare vertical and horizontal scaling results | Pending |

## Performance Metrics

- Requests Per Second (RPS)
- Average Response Time
- p50 Latency
- p90 Latency
- p95 Latency
- p99 Latency
- Error Rate
- CPU Utilization
- Memory Utilization

## Hardware and Environment

| Resource | Specification |
|---|---|
| Processor | Intel Core i5-1235U (12th Gen) |
| Physical Cores | 10 |
| Logical CPUs | 12 |
| Total RAM | 7.43 GiB |
| Operating System | Ubuntu 24.04.5 LTS |
| Docker Engine | 29.9.2 |

## Implementation Details

### Application

A Django application exposing four endpoints:

- `/api/health/`
- `/api/info/`
- `/api/light/`
- `/api/work/`

The `/api/work/` endpoint performs CPU-intensive calculations and is used to generate a measurable workload.

### Containerization

Docker packages the Django application.

Docker Compose manages the application containers, resource limits, and load-testing environment.

### Application Server

Gunicorn serves the Django application.

Worker processes are configured to experiment with application concurrency.

### Traffic Generation

k6 simulates concurrent requests using:

- 10 virtual users
- 30-second test duration
- 1,000,000 iterations per request

### Monitoring

Docker Stats is used to observe container CPU and memory utilization.

---

## 1. Baseline Experiment

### Configuration

| Setting | Value |
|---|---|
| Application Instances | 1 |
| CPU Limit | 1 CPU |
| Memory Limit | 512 MB |
| Gunicorn Workers | 1 |
| Gunicorn Threads | 1 |
| Virtual Users | 10 |
| Duration | 30 seconds |

### Results

| Metric | Value |
|---|---:|
| Total Requests | 455 |
| Requests Per Second | 14.84 |
| Average Latency | 666.86 ms |
| p50 Latency | 687.89 ms |
| p90 Latency | 777.53 ms |
| p95 Latency | 871.69 ms |
| p99 Latency | 1.21 seconds |
| Maximum Latency | 1.24 seconds |
| Failed Requests | 0 |

### Resource Observation

| Metric | Value |
|---|---:|
| CPU Usage | 101.45% |
| Memory Usage | 52.09 MiB |
| Memory Limit | 512 MiB |

Resource measurements are individual Docker Stats observations, not averages or peaks.

---

## 2. Vertical Scaling Experiment

### Objective

Increase the resources available to a single application instance and investigate how CPU allocation and Gunicorn worker count affect performance.

**Important:** The number of Docker containers remained one throughout the vertical scaling experiments.

### V1 - Increasing CPU Allocation

#### Configuration

| Setting | Value |
|---|---|
| Application Instances | 1 |
| CPU Limit | 2 CPUs |
| Memory Limit | 512 MB |
| Gunicorn Workers | 1 |
| Gunicorn Threads | 1 |
| Virtual Users | 10 |
| Duration | 30 seconds |

#### Results

| Metric | Value |
|---|---:|
| Total Requests | 547 |
| Requests Per Second | 17.93 |
| Average Latency | 553.02 ms |
| p50 Latency | 550.06 ms |
| p90 Latency | 602.54 ms |
| p95 Latency | 610.58 ms |
| p99 Latency | 631.64 ms |
| Maximum Latency | 637.35 ms |
| Failed Requests | 0 |

#### Analysis

Compared with the baseline:

- Throughput increased by approximately 20.8%.
- Average latency decreased by approximately 17.1%.
- p95 latency decreased by approximately 30%.
- p99 latency decreased by approximately 47.8%.

The CPU quota was increased from one CPU to two CPUs while retaining a single Gunicorn worker.

The improvement was measurable, but additional CPU quota alone does not guarantee proportional performance improvement.

### V2 - Increasing Gunicorn Workers

#### Configuration

| Setting | Value |
|---|---|
| Application Instances | 1 |
| CPU Limit | 2 CPUs |
| Memory Limit | 512 MB |
| Gunicorn Workers | 2 |
| Gunicorn Threads | 1 |
| Virtual Users | 10 |
| Duration | 30 seconds |

#### Results

| Metric | Value |
|---|---:|
| Total Requests | 963 |
| Requests Per Second | 31.76 |
| Average Latency | 312.88 ms |
| p50 Latency | 311.59 ms |
| p90 Latency | 349.93 ms |
| p95 Latency | 375.42 ms |
| p99 Latency | 443.50 ms |
| Maximum Latency | 500.07 ms |
| Failed Requests | 0 |

#### Analysis

Compared with V1:

- Throughput increased by approximately 77.2%.
- Average latency decreased by approximately 43.5%.
- p95 latency decreased by approximately 38.5%.
- p99 latency decreased by approximately 29.6%.

Increasing the Gunicorn worker count allowed multiple requests to be processed concurrently.

This demonstrates that application concurrency configuration can significantly affect performance, even without adding another application container.

### Vertical Scaling Comparison

| Metric | Baseline | V1 | V2 |
|---|---:|---:|---:|
| Application Instances | 1 | 1 | 1 |
| CPU Limit | 1 | 2 | 2 |
| Memory Limit | 512 MB | 512 MB | 512 MB |
| Gunicorn Workers | 1 | 1 | 2 |
| Total Requests | 455 | 547 | 963 |
| RPS | 14.84 | 17.93 | 31.76 |
| Average Latency | 666.86 ms | 553.02 ms | 312.88 ms |
| p95 Latency | 871.69 ms | 610.58 ms | 375.42 ms |
| p99 Latency | 1.21 s | 631.64 ms | 443.50 ms |
| Failed Requests | 0 | 0 | 0 |

### Vertical Scaling Conclusion

The experiments demonstrated two ways to improve the capacity of a single application instance:

1. Increase the CPU resources allocated to the application.
2. Increase Gunicorn worker processes to improve request concurrency.

The V2 configuration achieved 31.76 requests per second compared with 14.84 requests per second in the baseline experiment.

This is approximately a 114% increase in throughput in the tested environment.

These are local benchmark results, not production performance guarantees. The tests were performed on the same laptop, where the application and load generator shared host resources.

---

## 3. Horizontal Scaling Experiment

### Objective

To be completed.

Run multiple Django application instances behind an Nginx load balancer and measure the effect of distributing requests across instances.

## 4. Performance Comparison

To be completed after horizontal scaling.

## Analysis

The baseline and vertical scaling experiments show that application performance depends on resource allocation and application concurrency.

Horizontal scaling will be tested next to investigate how multiple application instances distribute workload.

## Key Learnings

- Vertical scaling increases the resources available to an existing application instance.
- Horizontal scaling increases the number of application instances.
- Increasing CPU allocation does not automatically increase application concurrency.
- Gunicorn worker configuration affects how many requests can be processed concurrently.
- Load testing helps identify performance bottlenecks.
- Throughput and latency should be evaluated together.
- Benchmark results must be interpreted in the context of the test environment.

## Results and Detailed Documentation

- [Baseline Experiment](results/baseline.md)
- [Vertical Scaling Experiment](results/vertical-scaling.md)
- [Horizontal Scaling Experiment](results/horizontal-scaling.md)
- [Performance Comparison](results/comparison.md)
