from collections.abc import Generator

import pytest

from config.config import SERIES_TABLE_NAME
from helpers.db_helpers import DbConnection
from helpers.file_helpers import load_sql


@pytest.fixture()
def add_several_shows_to_db(db_connection: DbConnection, request) -> Generator[int, None, None]:
    """
    Adds several shows from the file to the database and clears them afterwards.
    """
    row_count = 0
    if hasattr(request, "param") and request.param:
        sql = load_sql(request.param)
        res = db_connection.execute(sql)
        row_count = res.rows_count
    yield row_count
    db_connection.execute(f"truncate table {SERIES_TABLE_NAME}")


@pytest.fixture()
def add_one_show_to_db(db_connection: DbConnection) -> Generator[int, None, None]:
    """
    Adds only one show to the database and removes it afterwards.
    :return: ID of the row with added show.
    """
    sql = (f"INSERT INTO {SERIES_TABLE_NAME} (name,photo,rating,status,review) VALUES "
           f"('Перехрюндель и друзья','https://example.com/',10,'watching'::public.seriesstatus,'Вау!') RETURNING id")
    res = db_connection.execute(sql)
    # RETURNING statement is added to the SQL script above to get added row's 'id' column value, so here it is:
    show_id = res.data[0][0]
    yield show_id
    db_connection.execute(f"DELETE FROM {SERIES_TABLE_NAME} WHERE id = {show_id}")
