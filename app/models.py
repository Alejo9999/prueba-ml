from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    site: str
    id: int

class FullItem(Item):
    price: Optional[float] = None
    start_time: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    nickname: Optional[str] = None
