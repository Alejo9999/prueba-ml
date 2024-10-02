import httpx
from typing import Optional

BASE_API_URL = "https://api.mercadolibre.com"

class MeLiAPI:
    def __init__(self, base_url: str = BASE_API_URL, max_connections: int = 10):

        self.client = httpx.AsyncClient(base_url=base_url, limits=httpx.Limits(max_connections=max_connections))
    
    async def fetch_data(self, endpoint: str, key: str) -> Optional[str]:

        response = await self.client.get(endpoint)
        if response.status_code == 200:
            return response.json().get(key, '')
        return ''
    
    async def fetch_item(self, site: str, item_id: int) -> dict:

        endpoint = f"/items/{site}{item_id}"
        response = await self.client.get(endpoint)
        return response.json()
    
    async def close(self):

        await self.client.aclose()
