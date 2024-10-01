from typing import List
from fastapi import UploadFile
import csv
import json
from app.config import CONFIG
from app.models import Item


async def read_file(file: UploadFile) -> List[Item]:

    if file.filename.endswith('.csv'):
        return await csv_reader(file)
    elif file.filename.endswith('.jsonl'):
        return await jsonlines_reader(file)
    elif file.filename.endswith('.txt'):
        return await txt_reader(file)
    elif file.filename.endswith('.json'):
        raise print("no se soporta json")
    else:
        raise("Tipo de archivo no soportado")

async def csv_reader(file: UploadFile) -> List[Item]:
    delimiter = CONFIG['csv']['delimiter']
    encoding = CONFIG['csv']['encoding']
    items = []
    content = await file.read()
    lines = content.decode(encoding).splitlines()
    reader = csv.reader(lines , delimiter=delimiter)
    
    next(reader, None)
    
    for row in reader:
        try:
            site = row[0].strip()
            item_id = int(row[1].strip())
            items.append(Item(site=site, id=item_id))
        except ValueError:
            print(f"Fila ignorada por valor incorrecto en 'id': {row}")
            continue
    return items

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