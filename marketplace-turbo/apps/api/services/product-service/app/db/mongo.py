from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URL)
    return _client


def get_db():
    client = get_client()
    return client[settings.MONGO_DB]


def get_products_collection():
    return get_db()["products"]


def get_categories_collection():
    return get_db()["categories"]


def get_audit_logs_collection():
    return get_db()["audit_logs"]


# (Opcional) Si tu código viejo importa variables directas:
products = get_products_collection()
categories = get_categories_collection()
audit_logs = get_audit_logs_collection()
