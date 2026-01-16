from motor.motor_asyncio import AsyncIOMotorClient

def make_mongo(db_url: str) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(db_url)
