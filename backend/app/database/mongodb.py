from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from backend/.env
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# MongoDB bağlantı bilgileri
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "anlikcevirisistemi")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "users")

# Google Cloud credentials
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if GOOGLE_CREDENTIALS:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_CREDENTIALS
    print(f"Google Cloud credentials loaded from: {GOOGLE_CREDENTIALS}")
else:
    print("WARNING: GOOGLE_APPLICATION_CREDENTIALS not set!")

print(f"MongoDB Config - URL: {MONGODB_URL}, DB: {DATABASE_NAME}, Collection: {COLLECTION_NAME}")

# Asenkron MongoDB client
async def get_mongodb():
    client = AsyncIOMotorClient(MONGODB_URL)
    return client[DATABASE_NAME]

# Senkron MongoDB client (gerekirse)
def get_sync_mongodb():
    client = MongoClient(MONGODB_URL)
    return client[DATABASE_NAME]

# Veritabanı koleksiyonları
async def get_user_collection():
    db = await get_mongodb()
    return db[COLLECTION_NAME] 