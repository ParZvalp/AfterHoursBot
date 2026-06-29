from core.database.db import Database

class GameRepository:

    def __init__(self):
        self.db = Database()

    def random_game(self, exclude_id=None):

        if exclude_id is None:
            return self.db.fetchone("""
                SELECT *
                FROM games
                ORDER BY RANDOM()
                LIMIT 1
            """)

        return self.db.fetchone("""
            SELECT *
            FROM games
            WHERE id != ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (exclude_id,))

    def all_games(self):
        return self.db.fetchall("""
            SELECT *
            FROM games
        """)

    def provider_exists(self, provider, provider_id):

        return self.db.fetchone("""
            SELECT id
            FROM games
            WHERE provider = ?
            AND provider_id = ?
        """, (provider, provider_id))

    def save(self, game):

        self.db.execute("""
            INSERT INTO games(

                provider,
                provider_id,

                name,
                slug,

                description,

                released,

                rating,
                metacritic,

                genres,
                platforms,

                developers,
                publishers,

                website,

                image

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            game.provider,
            game.provider_id,

            game.name,
            game.slug,

            game.description,

            game.released,

            game.rating,
            game.metacritic,

            game.genres,
            game.platforms,

            game.developers,
            game.publishers,

            game.website,

            game.image

        ))

    def count_games(self):

        result = self.db.fetchone("""
            SELECT COUNT(*) AS total
            FROM games
        """)

        return result["total"]
    
    def game_by_id(self, game_id):

        return self.db.fetchone(
            """
            SELECT *
            FROM games
            WHERE id = ?
            """,
            (game_id,)
        )