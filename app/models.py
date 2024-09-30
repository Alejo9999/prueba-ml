from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    site: str
    id: int

class FullItem(Item):
    price: float
    start_time: str
    name: str
    description: str
    nickname: str
