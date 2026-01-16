import redis.asyncio as redis

def make_redis(url: str) -> redis.Redis:
    return redis.from_url(url, decode_responses=True)
