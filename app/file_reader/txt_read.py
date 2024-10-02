from app.models.models import Item
from app.config.config import CONFIG
from app.file_reader.base import BaseFileReader

class TXTRead(BaseFileReader):
    async def read(self):
        delimiter = CONFIG['csv']['delimiter']
        encoding = CONFIG['csv']['encoding']
        
        items_chunk = []
        
        while True:
            line =  self.file.file.readline()
            if not line:
                break

            line = line.decode(encoding).strip()
            parts = line.split(delimiter)

            if len(parts) < 2:
                continue

            site, item_id = parts[0].strip(), parts[1].strip()

            try:
                item_id = int(item_id)
                items_chunk.append(Item(site=site, id=item_id))
            except ValueError:
                continue

        if len(items_chunk) >= self.chunk_size:
            yield items_chunk
            items_chunk = []

        if items_chunk:
            yield items_chunk