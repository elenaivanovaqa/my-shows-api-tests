import os
from collections.abc import Generator

import pytest
import requests

from config.config import Config
from helpers.api_helpers import ApiSession
from helpers.db_helpers import DbConnection


pytest_plugins = ["fixtures.db_fixtures"]


@pytest.fixture(scope="session")
def settings() -> Config:
    # Environment variables can be stored in .env file.
    # To read from the file automatically, one can install pytest-dotenv plugin.
    return Config(
        my_shows_host=os.environ["MY_SHOWS_HOST"],
        my_shows_postgres_db=os.environ["MY_SHOWS_POSTGRES_DB"],
        my_shows_postgres_user=os.environ["MY_SHOWS_POSTGRES_USER"],
        my_shows_postgres_host=os.environ["MY_SHOWS_POSTGRES_HOST"],
        my_shows_postgres_port=os.environ["MY_SHOWS_POSTGRES_PORT"],
        my_shows_postgres_password=os.environ["MY_SHOWS_POSTGRES_PASSWORD"]
    )


@pytest.fixture(scope="session")
def api_session(settings) -> Generator[ApiSession, None, None]:
    with requests.Session() as session:
        yield ApiSession(session, settings.my_shows_host)


@pytest.fixture()
def db_connection(settings) -> Generator[DbConnection, None, None]:
    with DbConnection(settings) as connection:
        yield connection
