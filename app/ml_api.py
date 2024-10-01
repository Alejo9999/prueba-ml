import httpx
from typing import List, Optional
from app.models import Item, FullItem

BASE_API_URL = "https://api.mercadolibre.com"

async def fetch_data_from_api(client: httpx.AsyncClient, endpoint: str, key: str) -> Optional[str]:
    response = await client.get(f"{BASE_API_URL}{endpoint}")
    if response.status_code == 200:
        return response.json().get(key, '')
    return ''

async def fetch_items_data(items: List[Item]) -> List[FullItem]:
    async with httpx.AsyncClient() as client:
        full_items = []
        for item in items:
            site, item_id = item.site, item.id
            item_key = f"{site}{item_id}"
           
            item_response = await client.get(f"{BASE_API_URL}/items/{item_key}")
            item_data = item_response.json()
            
           
            price = item_data.get('price')
            start_time = item_data.get('start_time', None) or None
            category_id = item_data.get('category_id')
            currency_id = item_data.get('currency_id')
            seller_id = item_data.get('seller_id')
            
            
            category_name = await fetch_data_from_api(client, f"/categories/{category_id}", "name") if category_id else ''
            currency_description = await fetch_data_from_api(client, f"/currencies/{currency_id}", "description") if currency_id else ''
            seller_nickname = await fetch_data_from_api(client, f"/users/{seller_id}", "nickname") if seller_id else ''

            
            full_items.append(FullItem(
                site=site,
                id=item_id,
                price=price,
                start_time=start_time,
                name=category_name,
                description=currency_description,
                nickname=seller_nickname
            ))
    return full_items
