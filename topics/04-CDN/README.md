# CDN Practical — Django + Nginx

A local CDN caching simulation using Django as the origin server and
Nginx as the edge caching layer.

## Architecture

Client -> Nginx edge cache -> Django origin

- Nginx: localhost:8080
- Django origin: localhost:8000
- Cacheable API: /api/products/
- Non-cacheable API: /api/health/
- Static asset: /assets/sample.txt

## Requirements

- Docker
- Docker Compose
- Node.js 18 or newer (for the benchmark)

## Start the project

```bash
docker compose up --build -d
```

Check running services:

```bash
docker compose ps
```

## Test the cache

First request — expected MISS:

```bash
curl -i http://localhost:8080/api/products/
```

Second request — expected HIT:

```bash
curl -i http://localhost:8080/api/products/
```

Check the `X-Cache-Status` response header.

## Compare origin and edge

Direct origin request:

```bash
curl -i http://localhost:8000/api/products/
```

Request through the Nginx edge:

```bash
curl -i http://localhost:8080/api/products/
```

## Test TTL expiration

The configured TTL is 30 seconds.

```bash
curl -i http://localhost:8080/api/products/
sleep 31
curl -i http://localhost:8080/api/products/
```

The request after expiration should fetch a fresh response from Django.

## Test cache bypass

```bash
curl -i http://localhost:8080/api/health/
```

Expected cache status: BYPASS.

## Test static asset delivery

```bash
curl -i http://localhost:8080/assets/sample.txt
```

The static file is served directly by Nginx.

## Run benchmark

```bash
node benchmarks/benchmark.js
```

Customize the run:

```bash
DURATION_MS=30000 CONCURRENCY=20 node benchmarks/benchmark.js
```

The benchmark reports throughput, average latency, median latency,
P95 latency, failures, and Nginx cache status counts.

## Inspect logs

```bash
docker compose logs -f nginx
docker compose logs -f web
```

## Clear the local cache

This removes the named cache volume and stops the containers:

```bash
docker compose down -v
docker compose up --build -d
```

Do not use `-v` if you need to preserve the cache volume.

## Stop the project

```bash
docker compose down
```

## Learning outcomes

- Understand origin and edge servers.
- Observe cache HIT and MISS.
- Understand TTL and expiration.
- Configure Nginx proxy caching.
- Serve static assets from an edge server.
- Understand cache bypass.
- Observe concurrent cache-fill protection.
- Benchmark requests through a cache.

## Important limitation

This is a local CDN simulation. A single Nginx instance is not a
geographically distributed CDN. It demonstrates the HTTP caching
behavior used as part of CDN architectures.
