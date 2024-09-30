import httpx
from typing import List
from app.models import Item, FullItem

BASE_API_URL = "https://api.mercadolibre.com"

async def fetch_items_data(items: List[Item]) -> List[FullItem]:
    async with httpx.AsyncClient() as client:
        full_items = []
        for item in items:
            site, item_id = item['site'], item['id']
            item_key = f"{site}{item_id}"
           
            item_response = await client.get(f"{BASE_API_URL}/items/{item_key}")
            item_data = item_response.json()
            
           
            price = item_data['price']
            start_time = item_data['start_time']
            category_id = item_data['category_id']
            currency_id = item_data['currency_id']
            seller_id = item_data['seller_id']
            
           
            category_response = await client.get(f"{BASE_API_URL}/categories/{category_id}")
            category_name = category_response.json().get('name', '')

           
            currency_response = await client.get(f"{BASE_API_URL}/currencies/{currency_id}")
            currency_description = currency_response.json().get('description', '')

           
            user_response = await client.get(f"{BASE_API_URL}/users/{seller_id}")
            seller_nickname = user_response.json().get('nickname', '')

            full_items.append({
                "site": site,
                "id": item_id,
                "price": price,
                "start_time": start_time,
                "name": category_name,
                "description": currency_description,
                "nickname": seller_nickname
            })
    return full_items
