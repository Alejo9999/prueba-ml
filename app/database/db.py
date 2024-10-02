import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from app.models.models import FullItem

mongo_url = os.getenv('MONGO_URL', 'mongodb://mongo:27017')
client = AsyncIOMotorClient(mongo_url)
db = client['mercado_libre_db']
collection = db['items']

async def save_to_db(items: List[FullItem]):
    if not items:
        print("No items to save")
        return
    items_dict = [item.dict() for item in items]
    result = await collection.insert_many(items_dict)
    print(f"{len(result.inserted_ids)} ítems guardados en MongoDB")