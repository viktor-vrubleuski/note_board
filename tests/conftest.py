from datetime import datetime

import pytest
from starlette.testclient import TestClient

from src.app.api.models import BoardSchema, NoteSchema
from src.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture
def board() -> BoardSchema:
    return BoardSchema(
        id=1, name="Board name", created_on=datetime.now(), updated_on=datetime.now()
    )


@pytest.fixture
def note() -> NoteSchema:
    return NoteSchema(
        id=1,
        text="Text note",
        created_on=datetime.now(),
        updated_on=datetime.now(),
        count_view=0,
    )
