import asyncio
from typing import List
from app.models.models import Item, FullItem
from app.services.ml_api import MeLiAPI  # Import the API client

class ItemProcessor:
    def __init__(self, api_client: MeLiAPI):
        # Use the API client to process items
        self.api_client = api_client

    async def process_item(self, item: Item) -> FullItem:
        # Process individual item data
        item_data = await self.api_client.fetch_item(item.site, item.id)
        
        price = item_data.get('price')
        start_time = item_data.get('start_time') or None
        category_id = item_data.get('category_id')
        currency_id = item_data.get('currency_id')
        seller_id = item_data.get('seller_id')

        category_name = await self.api_client.fetch_data(f"/categories/{category_id}", "name") if category_id else ''
        currency_description = await self.api_client.fetch_data(f"/currencies/{currency_id}", "description") if currency_id else ''
        seller_nickname = await self.api_client.fetch_data(f"/users/{seller_id}", "nickname") if seller_id else ''

        return FullItem(
            site=item.site,
            id=item.id,
            price=price,
            start_time=start_time,
            name=category_name,
            description=currency_description,
            nickname=seller_nickname
        )

async def fetch_items_data_concurrent(items: List[Item]) -> List[FullItem]:
    # This will initialize the API client and process items concurrently
    api_client = MeLiAPI()
    item_processor = ItemProcessor(api_client)
    
    try:
        tasks = [item_processor.process_item(item) for item in items]
        full_items = await asyncio.gather(*tasks)
    finally:
        await api_client.close()
    
    return full_items
