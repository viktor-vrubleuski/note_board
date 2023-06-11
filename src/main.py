import sqlalchemy
from fastapi import FastAPI

from src.app.api import board, note

from .app.db import DeclarativeBase, database, dialect

app = FastAPI()


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
