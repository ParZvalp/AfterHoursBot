from database.db import Database


class GameRepository:

    def __init__(self):
        self.db = Database()

    def random_game(self):
        return self.db.fetchone(
            """
            SELECT *
            FROM games
            ORDER BY RANDOM()
            LIMIT 1
            """
        )

    def all_games(self):
        return self.db.fetchall(
            """
            SELECT *
            FROM games
            """
        )

    def game_by_name(self, name):
        return self.db.fetchone(
            """
            SELECT *
            FROM games
            WHERE name = ?
            """,
            (name,)
        )

    def games_by_genre(self, genre):
        return self.db.fetchall(
            """
            SELECT *
            FROM games
            WHERE genre = ?
            """,
            (genre,)
        )

    def add_game(self, game):
        self.db.execute(
            """
            INSERT INTO games(
                name,
                description,
                genre,
                players,
                release_year,
                platform,
                developer,
                steam_url,
                cover
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            game
        )

    def delete_game(self, game_id):
        self.db.execute(
            """
            DELETE FROM games
            WHERE id = ?
            """,
            (game_id,)
        )