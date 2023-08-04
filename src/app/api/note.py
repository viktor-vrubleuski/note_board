from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from typing_extensions import Annotated

from src.app.api.board import verify_board_id
from src.app.api.models import NoteSchema, ResponseSchema
from src.app.api.repositories import NoteRepository

router = APIRouter()


async def verify_note_id_and_board_id(
    id: Annotated[int, Path(...)], note_id: Annotated[int, Path(...)]
):
    note = await NoteRepository.get_note(id, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")


@router.post(
    "/",
    response_model=NoteSchema,
    status_code=201,
    dependencies=[Depends(verify_board_id)],
)
async def create_note(
    id: int,
    payload: NoteSchema,
):
    note_id = await NoteRepository.create_note(id, payload)

    response_object = {
        "id": note_id,
        "text": payload.text,
        "count_view": payload.count_view,
    }
    return response_object


@router.get(
    "/", response_model=List[NoteSchema], dependencies=[Depends(verify_board_id)]
)
async def get_notes(id: int):
    return await NoteRepository.get_notes(id)


@router.get(
    "/{note_id}/",
    response_model=NoteSchema,
    dependencies=[Depends(verify_note_id_and_board_id)],
)
async def get_note(id: int, note_id: int):
    await NoteRepository.update_count_view_note(id, note_id)
    return await NoteRepository.get_note(id, note_id)


@router.put(
    "/{note_id}/",
    response_model=NoteSchema,
    dependencies=[Depends(verify_note_id_and_board_id)],
)
async def update_note(id: int, note_id: int, payload: NoteSchema):
    await NoteRepository.update_note(id, note_id, payload)
    response_object = {
        "id": note_id,
        "text": payload.text,
    }
    return response_object


@router.delete(
    "/{note_id}/",
    response_model=ResponseSchema,
    dependencies=[Depends(verify_note_id_and_board_id)],
)
async def delete_note(id: int, note_id: int):
    await NoteRepository.delete_note(id, note_id)
    return ResponseSchema().dict()
