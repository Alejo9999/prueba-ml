from typing import List, AsyncGenerator
from fastapi import UploadFile
import json
from app.config import CONFIG
from app.models import Item
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def read_file(file: UploadFile) -> List[Item]:
    logger.info("Logger configurado correctamente")

    if file.filename.endswith('.csv'):
        #logger.info("Leyendo archivo CSV")
        return await csv_reader(file)
    elif file.filename.endswith('.jsonl'):
        #logger.info("Leyendo archivo JSONL")
        return await jsonlines_reader(file)
    elif file.filename.endswith('.txt'):
        #logger.info("Leyendo archivo TXT")
        return await txt_reader(file)
    elif file.filename.endswith('.json'):
        #logger.error("json no soportado")
        raise ValueError("json no soportado")
    else:
        raise("Tipo de archivo no soportado")

async def csv_reader(file: UploadFile, chunk_size: int = 100) -> AsyncGenerator[List[Item], None]:
    delimiter = CONFIG['csv']['delimiter']
    encoding = CONFIG['csv']['encoding']
  
    items_chunk = []
    first_line = True
    
    while True:
        line =  file.file.readline()
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
            
            if len(items_chunk) >= chunk_size:
                yield items_chunk
                items_chunk = []
                
        except ValueError:
            #logger.error(f"Fila ignorada por valor incorrecto en 'id': {row}")
            continue
    if items_chunk:
        yield items_chunk

async def jsonlines_reader(file: UploadFile) -> List[Item]:
    encoding = CONFIG['jsonlines']['encoding']
    items = []
    async for line in file:
        data = json.loads(line.decode(encoding))
        items.append({"site": data['site'], "id": data['id']})
    return items

async def txt_reader(file: UploadFile) -> List[Item]:
    encoding = CONFIG['txt']['encoding']
    delimiter = CONFIG['txt']['delimiter']
    items = []
    async for line in file:
        line = line.decode(encoding).strip()
        site, item_id = line.split(delimiter)
        items.append({"site": site.strip(), "id": int(item_id.strip())})
    return items