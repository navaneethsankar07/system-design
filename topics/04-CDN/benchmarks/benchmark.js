const url = process.env.URL || "http://localhost:8080/api/products/";
const durationMs = Number(process.env.DURATION_MS || 10000);
const concurrency = Number(process.env.CONCURRENCY || 20);

const latencies = [];
const statuses = {};
let failures = 0;
let requests = 0;

const deadline = Date.now() + durationMs;

async function worker() {
    while (Date.now() < deadline) {
        const start = performance.now();

        try {
            const response = await fetch(url);
            await response.arrayBuffer();

            const elapsed = performance.now() - start;
            latencies.push(elapsed);

            const cacheStatus = response.headers.get("x-cache-status") || "NO_HEADER";
            statuses[cacheStatus] = (statuses[cacheStatus] || 0) + 1;

            if (!response.ok) failures++;
            requests++;
        } catch (error) {
            failures++;
        }
    }
}

function percentile(values, p) {
    if (!values.length) return 0;
    const sorted = [...values].sort((a, b) => a - b);
    return sorted[Math.min(Math.ceil(p * sorted.length) - 1, sorted.length - 1)];
}

async function main() {
    console.log("CDN edge benchmark");
    console.log({ url, durationMs, concurrency });

    // Warm the edge cache before measuring.
    await fetch(url);

    const start = Date.now();
    await Promise.all(Array.from({ length: concurrency }, () => worker()));
    const elapsedSeconds = (Date.now() - start) / 1000;

    const average = latencies.length
        ? latencies.reduce((a, b) => a + b, 0) / latencies.length
        : 0;

    console.log("\nResults");
    console.log("Requests:", requests);
    console.log("Failures:", failures);
    console.log("Duration:", elapsedSeconds.toFixed(2), "seconds");
    console.log("Throughput:", (requests / elapsedSeconds).toFixed(2), "req/s");
    console.log("Average latency:", average.toFixed(2), "ms");
    console.log("Median latency:", percentile(latencies, 0.50).toFixed(2), "ms");
    console.log("P95 latency:", percentile(latencies, 0.95).toFixed(2), "ms");
    console.log("Cache status counts:", statuses);
}

main();
