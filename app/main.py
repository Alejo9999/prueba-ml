from fastapi import FastAPI, UploadFile, HTTPException
from app.db import save_to_db
from app.ml_api import fetch_items_data

app = FastAPI()
    
@app.post("/file")
async def process_file(file:UploadFile):
    try:
        items = await file.read()
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {str(err)}")

    searched_items = await fetch_items_data(items)

    save_to_db(searched_items)

    return {"message": "File processed successfully", "data": len(searched_items)}





