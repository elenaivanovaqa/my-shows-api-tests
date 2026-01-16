from dataclasses import dataclass

import psycopg2
from psycopg2.extras import DictConnection, DictRow

from config.config import Config


@dataclass
class DatabaseResponse:
    data: list[DictRow] | None
    rows_count: int


class DbConnection:
    def __init__(self, config: Config):
        self.dbname = config.my_shows_postgres_db
        self.user = config.my_shows_postgres_user
        self.password = config.my_shows_postgres_password
        self.host = config.my_shows_postgres_host
        self.port = config.my_shows_postgres_port
        self.connection = None

    def execute(self, sql) -> DatabaseResponse | None:
        cursor = self.connection.cursor()
        error = None
        try:
            cursor.execute(sql)
        except psycopg2.DatabaseError as err:
            error = err
            self.connection.rollback()
        else:
            self.connection.commit()
            rows_count = cursor.rowcount
            try:
                data = cursor.fetchall()
            except psycopg2.ProgrammingError:
                data = None
            return DatabaseResponse(data=data, rows_count=rows_count)
        finally:
            cursor.close()
            if error:
                raise error

    def __enter__(self):
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            connection_factory=DictConnection,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
