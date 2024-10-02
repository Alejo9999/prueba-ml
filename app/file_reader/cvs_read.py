from app.models.models import Item
from app.config.config import CONFIG
from app.file_reader.base import BaseFileReader

class CVSRead(BaseFileReader):
    async def read(self):
        delimiter = CONFIG['csv']['delimiter']
        encoding = CONFIG['csv']['encoding']
        
        items_chunk = []
        first_line = True
        
        while True:
            line =  self.file.file.readline()
            if not line:
                break
    
            if first_line:
                first_line = False
                continue
        
            row = line.decode(encoding).strip().split(delimiter)
        
            try:
                site = row[0].strip()
                item_id = int(row[1].strip())
                items_chunk.append(Item(site=site, id=item_id))
            
                if len(items_chunk) >= self.chunk_size:
                    yield items_chunk
                    items_chunk = []
            except ValueError:
                continue
        
        if items_chunk:
            yield items_chunk