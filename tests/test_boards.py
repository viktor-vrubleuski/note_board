import json

import pytest

from src.app.api.models import BoardSchema
from src.app.api.repositories import BoardRepository


def test_create_board(test_app, monkeypatch):
    test_request_payload = {"name": "Board name"}
    test_response_payload = BoardSchema(id=1, name=test_request_payload["name"]).dict()

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(BoardRepository, "create_board", mock_post)

    response = test_app.post("/boards/", content=json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_board__invalid_payload(test_app):
    response = test_app.post("/boards/", content=json.dumps({}))

    assert response.status_code == 422


def test_read_board(test_app, monkeypatch, board):
    async def mock_get(id):
        return board.dict()

    monkeypatch.setattr(BoardRepository, "get_board", mock_get)

    response = test_app.get("/boards/1")

    assert response.status_code == 200
    assert response.json() == json.loads(board.json())


def test_read_board__incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(BoardRepository, "get_board", mock_get)

    response = test_app.get("/notes/123")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_read_boards(test_app, monkeypatch, board):
    async def mock_get():
        return [board.dict()]

    monkeypatch.setattr(BoardRepository, "get_boards", mock_get)

    response = test_app.get("/boards/")

    assert response.status_code == 200
    assert response.json() == [json.loads(board.json())]


def test_update_board(test_app, monkeypatch, board):
    board_id = 1

    test_update_request_payload = {
        "name": "Changed board name",
    }
    test_response_payload = BoardSchema(
        id=board_id,
        name=test_update_request_payload["name"],
    ).dict()

    async def mock_get(id):
        return board.dict()

    async def mock_update(id, payload):
        return test_response_payload

    monkeypatch.setattr(BoardRepository, "get_board", mock_get)
    monkeypatch.setattr(BoardRepository, "update_board", mock_update)

    response = test_app.put(
        "/boards/1", content=json.dumps(test_update_request_payload)
    )

    assert response.status_code == 200
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"name": None}, 422],
        [999, {"name": "Changed board name"}, 404],
    ],
)
def test_update_board__invalid(test_app, monkeypatch, id, payload, status_code, board):
    async def mock_get(id):
        if id == 1:
            return board.dict()
        return None

    monkeypatch.setattr(BoardRepository, "get_board", mock_get)

    response = test_app.put(f"/boards/{id}", content=json.dumps(payload))
    assert response.status_code == status_code


def test_remove_board(test_app, monkeypatch, board):
    async def mock_get(id):
        return board.dict()

    async def mock_delete(id):
        return 1

    monkeypatch.setattr(BoardRepository, "get_board", mock_get)
    monkeypatch.setattr(BoardRepository, "delete_board", mock_delete)

    response = test_app.delete("/boards/1/")
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}


def test_remove_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(BoardRepository, "get_board", mock_get)

    response = test_app.delete("/boards/123/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Board not found"
