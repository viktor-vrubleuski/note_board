import logging.config
import random
import string
import time

import sqlalchemy
from fastapi import FastAPI, Request

from src.app.api import board, note

from .app.db import DeclarativeBase, database, dialect

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms "
        f"status_code={response.status_code}"
    )

    return response


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
        for table in DeclarativeBase.metadata.tables.values():
            schema = sqlalchemy.schema.CreateTable(table, if_not_exists=True)
            query = str(schema.compile(dialect=dialect))
            await database.execute(query=query)


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Welcome!"}


app.include_router(board.router, prefix="/boards", tags=["boards"])
app.include_router(note.router, prefix="/boards/{id}/notes", tags=["notes"])
