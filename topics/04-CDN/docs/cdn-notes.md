# Content Delivery Network (CDN)

## 1. What is a CDN?

A **Content Delivery Network (CDN)** is a geographically distributed network of servers that delivers content to users from locations closer to them.

Instead of every user requesting content directly from one central origin server, a CDN can serve cached copies from its edge servers.

**Main objectives:**
- Reduce latency.
- Reduce requests reaching the origin server.
- Reduce origin bandwidth consumption.
- Improve content delivery under heavy traffic.
- Improve availability and resilience.

## 2. Important CDN components

### Origin server
The original server where the application's content is hosted.

It generates or stores the requested resources.

### Edge server
A server positioned closer to users that receives requests and can serve cached content.

### Cache
A temporary stored copy of a response or resource.

### Cache key
The identifier used by a cache to determine whether two requests refer to the same cached object.

### TTL (Time To Live)
The freshness period of a cached object.

After the TTL expires, the cache may need to fetch a fresh response from the origin.

## 3. How a CDN works

### Cache miss

1. A client requests a resource.
2. The edge server checks its cache.
3. The requested resource is not available as a fresh cached object.
4. The edge forwards the request to the origin.
5. The origin generates and returns the response.
6. The edge stores the response if caching rules permit.
7. The edge returns the response to the client.

### Cache hit

1. A client requests a resource.
2. The edge checks its cache.
3. A fresh cached copy is available.
4. The edge returns that copy directly.
5. The origin does not need to handle that request.

This reduces the work performed by the origin server.

## 4. Types of content delivered by CDNs

### Static content
Content that does not change frequently.

Examples:
- Images
- CSS files
- JavaScript files
- Fonts
- Videos
- Downloadable files

Static content is generally suitable for CDN caching.

### Dynamic content
Content generated based on application logic or request parameters.

Some dynamic responses can also be cached, provided they are safe to share and have an appropriate caching policy.

### Personalized content
Content specific to an individual user.

Examples:
- Account details
- Private dashboards
- Shopping cart information

Such responses must not accidentally be shared between users through a public cache.

## 5. Cache-Control headers

HTTP caching behaviour is commonly controlled through the `Cache-Control` response header.

Important directives:

- `public`: Shared caches are allowed to store the response.
- `private`: The response is intended for private caches, not shared caches.
- `no-store`: Caches should not store the response.
- `no-cache`: A stored response must be revalidated before reuse.
- `max-age`: Specifies how long a response is fresh, in seconds.
- `s-maxage`: Specifies freshness lifetime for shared caches.

Example:

```http
Cache-Control: public, max-age=3600
```

This permits shared caching and sets a freshness lifetime of one hour.

## 6. Cache expiration and invalidation

### Expiration
A cached object becomes stale after its freshness lifetime expires.

The edge may then fetch a new version from the origin.

### Invalidation
Sometimes content changes before its TTL expires.

For example, an image is updated but the old version is still cached.

Common solutions:

- Purge or invalidate cached objects.
- Use versioned URLs.
- Configure appropriate TTL values.
- Revalidate content with HTTP validators.

### Versioned URLs

Instead of repeatedly using:

```text
/assets/app.css
```

Use a versioned or fingerprinted URL:

```text
/assets/app.v2.css
```

A changed URL creates a different cache key, allowing clients and caches to fetch the new resource.

## 7. HTTP caching validators

### ETag
An identifier representing a particular version of a resource.

Clients can send:

```http
If-None-Match: "abc123"
```

If the resource has not changed, the origin can return:

```http
304 Not Modified
```

### Last-Modified
Indicates when a resource was last modified.

Clients can use `If-Modified-Since` to request revalidation.

### Age
Indicates approximately how long a response has been in a shared cache.

### Vary
Specifies which request headers influence the cached representation.

For example:

```http
Vary: Accept-Encoding
```

This tells caches that different content encodings may need separate representations.

## 8. Cache keys

A cache key determines which requests map to the same cached object.

A cache key may include:

- Request scheme.
- HTTP method.
- Host.
- Request path.
- Query parameters.
- Relevant request headers.

For example:

```text
/products/?category=electronics
/products/?category=books
```

These requests should not share the same cached response if the query parameter changes the returned content.

An incorrectly configured cache key can serve the wrong response.

## 9. CDN routing

A CDN must determine which edge location should handle a request.

Common techniques include:

- DNS-based routing.
- Anycast routing.
- Geographic or latency-based traffic steering.

The geographically nearest server is not necessarily the server selected. Network conditions, routing policies, server health, and capacity also matter.

## 10. Cache stampede

A cache stampede occurs when many requests simultaneously discover that a cache entry is missing or expired.

They may all request the same resource from the origin, creating unnecessary load.

Possible solutions:

- Request collapsing.
- Cache locks.
- Stale-while-revalidate.
- TTL jitter.
- Background refresh.

In this practical, Nginx `proxy_cache_lock` is enabled to help prevent multiple concurrent requests from performing the same cache fill.

## 11. CDN versus Redis

| CDN | Redis |
|---|---|
| Caches HTTP responses and assets | Stores application data |
| Can operate across geographic edge locations | Usually accessed by application servers |
| Reduces client-to-origin latency | Reduces application-to-database work |
| Commonly caches images, scripts, and API responses | Commonly caches queries, objects, and computed results |

They solve related but different caching problems and can be used together.

## 12. CDN architecture with an application cache

A typical architecture can look like:

```text
Client
  |
  v
CDN Edge Cache
  |
  v
Application Server
  |
  v
Redis Cache
  |
  v
Database
```

Each layer can reduce work for the layer behind it.

## 13. Practical implementation: Django + Nginx

I built a local CDN caching simulation using:

- Django as the origin server.
- Nginx as the edge caching layer.
- Docker Compose to run both services.
- Node.js to benchmark requests.

### Architecture

```text
Client
  |
  v
Nginx Edge (8080)
  |
  v
Django Origin (8000)
```

Nginx also serves static assets directly.

### Experiments performed

1. Cache MISS: First request fetched the response from Django.
2. Cache HIT: Repeated request returned the cached response.
3. TTL expiration: The cached response expired after 30 seconds.
4. Cache refresh: Nginx fetched a fresh response.
5. Cache bypass: The health endpoint was not cached.
6. Static delivery: Nginx served a static asset directly.

### Verified cache sequence

```text
MISS → HIT → EXPIRED → HIT
```

### Benchmark results

| Metric | Result |
|---|---:|
| Requests | 57,165 |
| Throughput | 5,749.27 req/s |
| Average latency | 3.47 ms |
| Median latency | 2.26 ms |
| P95 latency | 8.44 ms |
| Failures | 0 |

The cache was warmed before the benchmark. All measured requests were cache hits.

These measurements represent one local test, not a direct-origin performance comparison or a real geographically distributed CDN benchmark.

## 14. Limitations of the practical

This project demonstrates CDN caching behaviour locally.

It does not implement:

- Geographically distributed edge locations.
- Global DNS routing.
- Anycast.
- Multi-region replication.
- A commercial CDN provider's purge API.
- Real-world geographic latency comparisons.

A single local Nginx instance is an edge-cache simulation, not a complete CDN.

## 15. Key takeaways

- A CDN distributes content delivery across edge servers.
- Edge caching reduces requests reaching the origin.
- Cache hits serve stored responses; misses require fetching from the origin.
- TTL controls freshness.
- Cache invalidation handles outdated content.
- HTTP headers control caching behaviour.
- Cache keys must distinguish different representations.
- Personalized data requires careful cache isolation.
- CDNs and Redis can work together in a multi-layer caching architecture.