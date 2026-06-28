import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "afterhours.db"
        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

    def execute(self, query, values=()):

        self.cursor.execute(query, values)

        self.connection.commit()

    def fetchone(self, query, values=()):

        self.cursor.execute(query, values)

        return self.cursor.fetchone()

    def fetchall(self, query, values=()):

        self.cursor.execute(query, values)

        return self.cursor.fetchall()