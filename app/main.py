from fastapi import FastAPI, UploadFile, HTTPException
from app.db import save_to_db
from app.ml_api import fetch_items_data
from app.read_file import csv_reader

app = FastAPI()
    
@app.post("/file")
async def process_file(file:UploadFile):
    try:
        items = await csv_reader(file)
        print(f"Items leidos del archivo: {len(items)}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(err)}")

    searched_items = await fetch_items_data(items)
    print(f"Items obtenidos de las APIs: {len(searched_items)}")

    await save_to_db(searched_items)

    return {"message": "File processed successfully", "data": len(searched_items)}