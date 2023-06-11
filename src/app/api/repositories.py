from src.app.api.models import BoardSchema, NoteSchema
from src.app.db import board, database, note


class BoardRepository:
    async def create_board(payload: BoardSchema):
        query = board.insert().values(name=payload.name)
        return await database.execute(query=query)

    async def get_boards():
        query = board.select()
        return await database.fetch_all(query)

    async def get_board(id: int):
        query = board.select().where(id == board.c.id)
        return await database.fetch_one(query)

    async def update_board(id: int, payload):
        query = (
            board.update()
            .where(id == board.c.id)
            .values(name=payload.name)
            .returning(board.c.id)
        )
        return await database.fetch_one(query)

    async def delete_board(id: int):
        query = board.delete().where(id == board.c.id)
        return await database.execute(query=query)


class NoteRepository:
    async def create_note(board_id: int, payload: NoteSchema):
        query = note.insert().values(
            text=payload.text, board_id=board_id, count_view=payload.count_view
        )
        return await database.execute(query=query)

    async def get_notes(board_id: int):
        query = note.select().where(board_id == note.c.board_id)
        return await database.fetch_all(query)

    async def get_note(board_id: int, note_id: int):
        query = note.select().where(board_id == note.c.board_id, note_id == note.c.id)
        return await database.fetch_one(query)

    async def update_count_view_note(board_id: int, note_id: int):
        query = (
            note.update()
            .where(note_id == note.c.id, board_id == note.c.board_id)
            .values(count_view=note.c.count_view + 1)
            .returning(note.c.id)
        )
        return await database.fetch_one(query)

    async def update_note(board_id: int, note_id: int, payload: NoteSchema):
        query = (
            note.update()
            .where(note_id == note.c.id, board_id == note.c.board_id)
            .values(text=payload.text)
            .returning(note.c.id)
        )
        return await database.fetch_one(query)

    async def delete_note(board_id: int, note_id: int):
        query = note.delete().where(note_id == note.c.id, board_id == note.c.board_id)
        return await database.execute(query=query)
