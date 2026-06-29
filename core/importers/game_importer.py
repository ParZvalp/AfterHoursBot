from core.models.game import Game
from core.database.game_repository import GameRepository


class GameImporter:

    def __init__(self):

        self.repo = GameRepository()

    def map_rawg(self, rawg):

        return Game(

            provider="rawg",

            provider_id=rawg["id"],

            name=rawg["name"],

            slug=rawg["slug"],

            description=rawg.get("description_raw", ""),

            released=rawg.get("released", ""),

            rating=rawg.get("rating", 0),

            metacritic=rawg.get("metacritic", 0),

            genres=", ".join(
                g["name"] for g in rawg.get("genres", [])
            ),

            platforms=", ".join(
                p["platform"]["name"]
                for p in rawg.get("platforms", [])
            ),

            developers=", ".join(
                d["name"]
                for d in rawg.get("developers", [])
            ),

            publishers=", ".join(
                p["name"]
                for p in rawg.get("publishers", [])
            ),

            website=rawg.get("website", ""),

            image=rawg.get("background_image", "")
        )

    def import_rawg(self, rawg):

        if self.repo.provider_exists(
            "rawg",
            rawg["id"]
        ):
            return False

        game = self.map_rawg(rawg)

        self.repo.save(game)

        print(f"Imported: {game.name}")

        return True