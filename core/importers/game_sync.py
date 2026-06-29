from core.providers.rawg_client import RAWGClient
from core.importers.game_importer import GameImporter


class GameSync:

    def __init__(self):

        self.client = RAWGClient()
        self.importer = GameImporter()

    def sync_popular(self, pages=3):

        imported = 0

        for page in range(1, pages + 1):

            games = self.client.get_popular_games(page)

            for game in games:

                details = self.client.get_game_details(
                    game["id"]
                )

                if self.importer.import_rawg(details):
                    imported += 1

        return imported