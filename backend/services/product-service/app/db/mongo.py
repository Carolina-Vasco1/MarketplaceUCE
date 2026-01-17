from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

_client: AsyncIOMotorClient | None = None


def get_mongo_client() -> AsyncIOMotorClient:
    """
    Singleton de MongoClient (seguro para FastAPI + Docker)
    """
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(
            settings.MONGO_URL,
            uuidRepresentation="standard",
        )
    return _client


def get_db():
    client = get_mongo_client()
    return client[settings.MONGO_DB]


def get_products_collection():
    return get_db()["products"]


def get_categories_collection():
    return get_db()["categories"]


def get_audit_logs_collection():
    return get_db()["audit_logs"]
