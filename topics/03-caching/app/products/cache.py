import os

import redis
import time

from contextlib import contextmanager

CACHE_TTL = int(os.getenv("CACHE_TTL", 60))

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True,
)


@contextmanager
def cache_lock(key, timeout=10, wait=5):
    lock_key = f"lock:{key}"
    token = str(time.time_ns())

    acquired = redis_client.set(
        lock_key,
        token,
        nx=True,
        ex=timeout,
    )

    if not acquired:
        deadline = time.monotonic() + wait

        while time.monotonic() < deadline:
            time.sleep(0.05)

            acquired = redis_client.set(
                lock_key,
                token,
                nx=True,
                ex=timeout,
            )

            if acquired:
                break

    try:
        yield acquired
    finally:
        if acquired:
            redis_client.eval(
                """
                if redis.call('GET', KEYS[1]) == ARGV[1]
                then
                    return redis.call('DEL', KEYS[1])
                else
                    return 0
                end
                """,
                1,
                lock_key,
                token,
            )
