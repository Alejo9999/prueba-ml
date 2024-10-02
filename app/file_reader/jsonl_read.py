from app.models.models import Item
from app.config.config import CONFIG
from app.file_reader.base import BaseFileReader
import json

class JSONLRead(BaseFileReader):
    async def read(self):
        encoding = CONFIG['csv']['encoding']
        items_chunk = []
        
        while True:
            line = self.file.file.readline()
            if not line:
                break
            
            data = json.loads(line.decode(encoding).strip())
            items_chunk.append(Item(site=data['site'], id=int(data['id'])))
            
            if len(items_chunk) >= self.chunk_size:
                yield items_chunk
                items_chunk = []

        if items_chunk:
            yield items_chunk