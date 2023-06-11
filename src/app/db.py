import databases
import sqlalchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

from src.config import settings

database = databases.Database(settings.db_url)
dialect = sqlalchemy.dialects.postgresql.dialect()

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())


class Board(Base):
    __tablename__ = "board"

    name = Column(String)
    notes = relationship("Note", cascade="all,delete", back_populates="board")


class Note(Base):
    __tablename__ = "note"

    text = Column(Text)
    board_id = Column(Integer, ForeignKey("board.id", ondelete="CASCADE"))
    count_view = Column(Integer, default=0)
    board = relationship("Board", back_populates="notes")


board = Board.__table__
note = Note.__table__
