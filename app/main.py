from fastapi import FastAPI, UploadFile, HTTPException
from app.database.db import save_to_db
from app.file_reader.read_file import read_file
from app.models.models import Item
from app.services.item_processor import fetch_items_data_concurrent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/file")
async def process_file(file: UploadFile):
    logger.info("Procesando archivo")
    chunk_size = 100
    total_items = 0

    try:

        async for items_chunk in read_file(file, chunk_size=chunk_size):

            if not all(isinstance(item, Item) for item in items_chunk):
                raise ValueError("items_chunk contiene un tipo de dato inválido.")
            
            print(f"Items leidos: {len(items_chunk)}")
            

            searched_items = await fetch_items_data_concurrent(items_chunk)
            print(f"Items obtenidos de API: {len(searched_items)}")
            

            await save_to_db(searched_items)
            total_items += len(searched_items)

    except Exception as err:

        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(err)}")

    return {"message": "Archivo procesado correctamente", "data": total_items}
