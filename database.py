import motor.motor_asyncio
import os
import certifi

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo_admin:password@localhost:27017")

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo_admin:password@localhost:27017")
db = client.library

async def get_db():
    yield db