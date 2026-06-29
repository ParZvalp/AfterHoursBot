import os
import psycopg2
import psycopg2.extras


class Database:

    def __init__(self):
        self.url = os.environ.get("DATABASE_URL")

        if self.url is None:
            raise Exception("DATABASE_URL environment variable not set.")

    def _connect(self):
        return psycopg2.connect(self.url)

    def execute(self, sql, params=None):
        sql = sql.replace("?", "%s")
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
            conn.commit()

    def fetchone(self, sql, params=None):
        sql = sql.replace("?", "%s")
        with self._connect() as conn:
            with conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            ) as cur:
                cur.execute(sql, params or ())
                return cur.fetchone()

    def fetchall(self, sql, params=None):
        sql = sql.replace("?", "%s")
        with self._connect() as conn:
            with conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            ) as cur:
                cur.execute(sql, params or ())
                return cur.fetchall()