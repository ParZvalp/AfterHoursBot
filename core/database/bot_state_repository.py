from core.database.db import Database


class BotStateRepository:

    def __init__(self):
        self.db = Database()

    def get(self, key):

        result = self.db.fetchone(
            """
            SELECT value
            FROM bot_state
            WHERE key = ?
            """,
            (key,)
        )

        if result:
            return result["value"]

        return None

    def set(self, key, value):

        self.db.execute(
            """
            INSERT INTO bot_state(key, value)
            VALUES(?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
            """,
            (key, str(value))
        )

    def delete(self, key):

        self.db.execute(
            """
            DELETE FROM bot_state
            WHERE key = ?
            """,
            (key,)
        )