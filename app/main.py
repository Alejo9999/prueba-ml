from fastapi import FastAPI, UploadFile, HTTPException
from app.db import save_to_db
from app.ml_api import fetch_items_data_concurrent
from app.read_file import csv_reader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()
    
@app.post("/file")
async def process_file(file:UploadFile):
    logger.info("Procesando archivo")
    chunk_size = 100
    total_items = 0
    
    try:
        async for items_chunk in csv_reader(file, chunk_size=chunk_size):
            print(f"Items leidos: {len(items_chunk)}")
            
            searched_items = await fetch_items_data_concurrent(items_chunk)
            print(f"Items obtenidos de API: {len(searched_items)}")
            
            await save_to_db(searched_items)
            total_items += len(searched_items)
            
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(err)}")

    return {"message": "Archivo procesado correctamente", "data": total_items}