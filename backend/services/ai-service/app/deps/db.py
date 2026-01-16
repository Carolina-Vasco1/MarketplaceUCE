import aioredis
from app.core.config import settings

class RedisClient:
    redis = None

async def connect_redis():
    RedisClient.redis = await aioredis.create_redis_pool(settings.REDIS_URL)

async def close_redis():
    RedisClient.redis.close()
    await RedisClient.redis.wait_closed()

async def get_redis():
    return RedisClient.redis
