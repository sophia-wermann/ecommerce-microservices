import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME: str = os.getenv("DATABASE_NAME", "catalog_db")

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


async def connect_to_mongo() -> None:
    global _client, _db
    _client = AsyncIOMotorClient(MONGODB_URL)
    _db = _client[DATABASE_NAME]
    print(f"[catalog-service] Connected to MongoDB — database: {DATABASE_NAME}")


async def close_mongo_connection() -> None:
    global _client
    if _client:
        _client.close()
        print("[catalog-service] Disconnected from MongoDB")


def get_database() -> AsyncIOMotorDatabase:
    if _db is None:
        raise RuntimeError("Database not initialised. Call connect_to_mongo() first.")
    return _db
