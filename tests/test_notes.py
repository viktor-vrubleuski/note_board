import json

import pytest

from src.app.api.models import NoteSchema
from src.app.api.repositories import BoardRepository, NoteRepository


def test_create_notes(test_app, monkeypatch, board):
    test_request_payload = {"text": "Text note"}
    test_response_payload = NoteSchema(
        id=board.id, text=test_request_payload["text"]
    ).dict()

    async def mock_get(id):
        return board.dict()

    async def mock_post(id, payload):
        return 1

    monkeypatch.setattr(NoteRepository, "create_note", mock_post)
    monkeypatch.setattr(BoardRepository, "get_board", mock_get)

    response = test_app.post(
        f"/boards/{board.id}/notes/", content=json.dumps(test_request_payload)
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "board_id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"text": None}, 422],
        [999, {"name": "Text note"}, 404],
    ],
)
def test_create_note__invalid(
    test_app, monkeypatch, board_id, payload, status_code, board
):
    async def mock_get(id):
        if id == 1:
            return board.dict()
        return None

    monkeypatch.setattr(BoardRepository, "get_board", mock_get)

    response = test_app.post(f"/boards/{board_id}/notes/", content=json.dumps({}))

    assert response.status_code == status_code


def test_read_note(test_app, monkeypatch, note):
    async def mock_update_count_view(board_id, note_id):
        note.count_view += 1
        return note.dict()

    async def mock_get_note(board_id, note_id):
        return note.dict()

    monkeypatch.setattr(
        NoteRepository, "update_count_view_note", mock_update_count_view
    )
    monkeypatch.setattr(NoteRepository, "get_note", mock_get_note)

    response = test_app.get(f"/boards/1/notes/{note.id}/")

    assert response.status_code == 200
    assert response.json() == json.loads(note.json())


@pytest.mark.parametrize(
    "board_id, note_id, status_code",
    [
        [1, 123, 404],
        [123, 1, 404],
    ],
)
def test_read_note__incorrect_id(test_app, monkeypatch, board_id, note_id, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(NoteRepository, "get_note", mock_get)

    response = test_app.get(f"/notes/{board_id}/notes/{note_id}/")
    assert response.status_code == status_code


def test_read_notes(test_app, monkeypatch, note, board):
    async def mock_get(id):
        return board.dict()

    async def mock_get_notes(id):
        return [note.dict()]

    monkeypatch.setattr(NoteRepository, "get_notes", mock_get_notes)
    monkeypatch.setattr(BoardRepository, "get_board", mock_get)

    response = test_app.get("/boards/1/notes/")

    assert response.status_code == 200
    assert response.json() == [json.loads(note.json())]


def test_update_note(test_app, monkeypatch, note):
    board_id = 1
    note_id = 1

    test_update_request_payload = {
        "text": "Changed text note",
    }
    test_response_payload = NoteSchema(
        id=note_id,
        text=test_update_request_payload["text"],
    ).dict()

    async def mock_get(board_id, note_id):
        return note.dict()

    async def mock_update(board_id, note_id, payload):
        return test_response_payload

    monkeypatch.setattr(NoteRepository, "get_note", mock_get)
    monkeypatch.setattr(NoteRepository, "update_note", mock_update)

    response = test_app.put(
        f"/boards/{board_id}/notes/{note_id}",
        content=json.dumps(test_update_request_payload),
    )

    assert response.status_code == 200
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "board_id, note_id, payload, status_code",
    [
        [1, 1, {}, 422],
        [1, 1, {"text": None}, 422],
        [999, 1, {"text": "Changed board name"}, 404],
        [1, 999, {"text": "Changed board name"}, 404],
    ],
)
def test_update_board__invalid(
    test_app, monkeypatch, board_id, note_id, payload, status_code, note
):
    async def mock_get(board_id, note_id):
        if board_id == 1 and note_id == 1:
            return note.dict()
        return None

    monkeypatch.setattr(NoteRepository, "get_note", mock_get)

    response = test_app.put(
        f"/boards/{board_id}/notes/{note_id}", content=json.dumps(payload)
    )
    assert response.status_code == status_code


def test_remove_note(test_app, monkeypatch, note):
    async def mock_get(board_id, note_id):
        return note.dict()

    async def mock_delete(board_id, note_id):
        return 1

    monkeypatch.setattr(NoteRepository, "get_note", mock_get)
    monkeypatch.setattr(NoteRepository, "delete_note", mock_delete)

    response = test_app.delete("/boards/1/notes/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}


@pytest.mark.parametrize(
    "board_id, note_id, status_code",
    [[999, 1, 404], [1, 999, 404]],
)
def test_remove_note_incorrect_id(
    test_app, monkeypatch, board_id, note_id, status_code
):
    async def mock_get(board_id, note_id):
        return None

    monkeypatch.setattr(NoteRepository, "get_note", mock_get)

    response = test_app.delete(f"/boards/{board_id}/notes/{note_id}")
    assert response.status_code == status_code
