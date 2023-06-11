from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NoteSchema(BaseModel):
    id: Optional[int] = None
    text: str
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None
    count_view: int = 0


class BoardSchema(BaseModel):
    id: Optional[int] = None
    name: str
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None


class ResponseSchema(BaseModel):
    message: str = "Success"
