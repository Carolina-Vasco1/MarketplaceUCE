from libs.db.redis import make_redis
from ..core.config import settings

redis_client = make_redis(settings.REDIS_URL)
