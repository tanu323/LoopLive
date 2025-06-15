from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from app.core.config import get_config

# Load current config
config = get_config()

# Build MongoDB connection URI
def get_mongo_uri() -> str:
    user = config.DB_USER
    password = config.DB_PASSWORD
    host = config.DB_HOST
    port = config.DB_PORT
    db = config.DB_NAME

    return f"mongodb://{user}:{password}@{host}:{port}/{db}?authSource=admin"

# Initialize the MongoDB client
mongo_client: Optional[AsyncIOMotorClient] = None

# Access MongoDB database instance
def get_database():
    global mongo_client
    if mongo_client is None:
        mongo_uri = get_mongo_uri()
        mongo_client = AsyncIOMotorClient(mongo_uri)
    return mongo_client[config.DB_NAME]

# Optional: function to close connection (e.g. for graceful shutdown)
async def close_mongo_connection():
    if mongo_client:
        mongo_client.close()
