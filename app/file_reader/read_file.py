from typing import List, AsyncGenerator
from fastapi import UploadFile
from app.file_reader.jsonl_read import JSONLRead
from app.file_reader.cvs_read import CVSRead
from app.file_reader.txt_read import TXTRead
import logging
from app.models.models import Item

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def read_file(file: UploadFile, chunk_size: int = 100) -> AsyncGenerator[List[Item], None]:
    if file.filename.endswith('.csv'):
        logger.info("Leyendo archivo CSV")
        cvs_read = CVSRead(file, chunk_size)
        async for chunk in cvs_read.read():
            yield chunk
    elif file.filename.endswith('.jsonl'):
        logger.info("Leyendo archivo JSONL")
        jsonl_read = JSONLRead(file, chunk_size)
        async for chunk in jsonl_read.read():
            yield chunk
    elif file.filename.endswith('.txt'):
        logger.info("Leyendo archivo TXT")
        txt_read = TXTRead(file, chunk_size)
        async for chunk in txt_read.read():
            yield chunk
    else:
        logger.error("Tipo de archivo no soportado")
        raise ValueError("Tipo de archivo no soportado")





