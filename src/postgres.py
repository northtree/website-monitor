import os
from typing import Union

from psycopg2 import connect, sql, errors

from .model import URLStatus


class PGClient:

    def __init__(self, database: str=None, table: str=None):
        self.database = database or os.environ.get('PG_DATABASE')
        self.table = table or os.environ.get('PG_TABLE')

        try:
            self.conn = connect(os.environ.get('PG_URI'))
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()

            self._create_table()

        except errors.Error as e:
            print(f'Cannot connect to PostgreSQL: {e}')
            raise e

    def __enter__(self):
        print('Enter PGClient')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exit PGClient')
        # self.cursor.close()
        self.conn.close()
        print('Cleanup DB Connection')

    def current_database(self) -> Union[str, None]:
        try:
            self.cursor.execute('SELECT current_database()')
            result = self.cursor.fetchone()
            print(f'Successfully connected to: {result[0]}')
            if result:
                return result[0]
            return None

        except errors.DatabaseError as e:
            print(f'DB query error: {e}')
            return None

    def _create_table(self):
        try:
            # BIGINT for nanoseconds
            # https://www.postgresql.org/docs/9.1/datatype-numeric.html
            query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id serial PRIMARY KEY,
                url VARCHAR (2048) NOT NULL,
                status SMALLINT NOT NULL,
                start_time BIGINT NOT NULL,
                end_time BIGINT NOT NULL
            );
            """).format(sql.Identifier(self.table))
            # print(query.as_string(self.conn))
            self.cursor.execute(query)

        except errors.DatabaseError as e:
            print(f'DB query error: {e}')

    def insert(self, url_status: URLStatus):
        try:
            # Use `psycopg2.sql` module to generate SQL statements in
            # safe way to avoid SQL injection.
            # https://www.psycopg.org/docs/sql.html
            query = sql.SQL("""
            INSERT INTO {}
            (url, status, start_time, end_time)
            VALUES (%s, %s, %s, %s);
            """).format(sql.Identifier(self.table))
            self.cursor.execute(query, url_status.to_tuple())

        except errors.DatabaseError as e:
            print(f'DB insert error: {e}')
