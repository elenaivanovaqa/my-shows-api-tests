from http import HTTPStatus

import jsonschema
import pytest

from config.config import SERIES_ENDPOINT, SERIES_TABLE_NAME
from data.mappings import API_SERIES_STATUS_TO_DB_MAPPING
from helpers.api_helpers import ApiSession
from helpers.db_helpers import DbConnection
from helpers.file_helpers import load_yaml


@pytest.mark.parametrize(
    "add_several_shows_to_db",
    [
        "",
        "series_fill_1_row.sql",
        "series_fill_3_rows.sql",
    ],
    indirect=True,
)
def test_series_get(api_session: ApiSession, add_several_shows_to_db):
    response = api_session.get(SERIES_ENDPOINT)
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert len(body) == add_several_shows_to_db, body
    template = load_yaml("series_get_schema.yml")
    jsonschema.validate(body, template)


@pytest.mark.parametrize("param,value", [
    ("name", "А тута вота новое имечко"),
    ("photo", "http://new_example.org/"),
    ("rating", 1),
    ("status", "Посмотрел"),
    ("review", "Чепуха какая-то..."),
])
def test_update_show(
        add_one_show_to_db: int,
        db_connection: DbConnection,
        api_session: ApiSession,
        param,
        value
):
    put_body = {
        "name": "Перехрюндель и друзья",
        "photo": "https://example.com/",
        "rating": 10,
        "status": "Смотрю",
        "review": "string"
    }
    put_body[param] = value
    response = api_session.put(f"{SERIES_ENDPOINT}/{add_one_show_to_db}", body=put_body)
    assert response.status_code == HTTPStatus.OK
    response_body = response.json()
    assert response_body[param] == value
    db_data = db_connection.execute(f"SELECT * FROM {SERIES_TABLE_NAME} WHERE id = {add_one_show_to_db}").data
    if param == "status":
        value = API_SERIES_STATUS_TO_DB_MAPPING[value]
    assert db_data[0][param] == value
