from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from app.models import FullItem

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client['mercado_libre_db']
collection = db['items']

async def save_to_db(items: List[FullItem]):
    await collection.insert_many(items)
