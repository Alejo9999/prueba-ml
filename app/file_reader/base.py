from typing import AsyncGenerator, List
from fastapi import UploadFile
from app.models.models import Item

class BaseFileReader:
    def __init__(self, file: UploadFile, chunk_size: int = 100):
        self.file = file
        self.chunk_size = chunk_size
    async def read(self) -> AsyncGenerator[List[Item], None]:
        raise NotImplementedError("No implementado en subclases")