from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from typing_extensions import Annotated

from src.app.api.models import BoardSchema, ResponseSchema
from src.app.api.repositories import BoardRepository

router = APIRouter()


async def verify_board_id(id: Annotated[int, Path(...)]):
    board = await BoardRepository.get_board(id)

    if not board:
        raise HTTPException(status_code=404, detail="Board not found")


@router.post("/", response_model=BoardSchema, status_code=201)
async def create_board(payload: BoardSchema):
    board_id = await BoardRepository.create_board(payload)

    response_object = {
        "id": board_id,
        "name": payload.name,
    }
    return response_object


@router.get("/", response_model=List[BoardSchema])
async def get_boards():
    return await BoardRepository.get_boards()


@router.get(
    "/{id}/", response_model=BoardSchema, dependencies=[Depends(verify_board_id)]
)
async def get_board(id: int):
    return await BoardRepository.get_board(id)


@router.put(
    "/{id}/", response_model=BoardSchema, dependencies=[Depends(verify_board_id)]
)
async def update_board(id: int, payload: BoardSchema):
    await BoardRepository.update_board(id, payload)
    response_object = {
        "id": id,
        "name": payload.name,
    }
    return response_object


@router.delete(
    "/{id}/", response_model=ResponseSchema, dependencies=[Depends(verify_board_id)]
)
async def delete_board(id: int):
    await BoardRepository.delete_board(id)
    return ResponseSchema().dict()
