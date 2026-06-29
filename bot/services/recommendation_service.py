
from bot.services.game_service import GameService

from core.database.bot_state_repository import BotStateRepository
from core.importers.game_sync import GameSync


class RecommendationService:

    def __init__(self):

        self.sync = GameSync()

        self.games = GameService()

        self.state = BotStateRepository()

    def generate_today(self):

        # ----------------------------------
        # Sync latest games from RAWG
        # ----------------------------------

        imported = self.sync.sync_popular()

        # ----------------------------------
        # Pick today's featured game
        # ----------------------------------

        game = self.games.random_game()

        # ----------------------------------
        # Save today's featured game
        # ----------------------------------

        self.state.set(
            "featured_game_id",
            game["id"]
        )

        return imported, game

    def current_game(self):

        featured = self.state.get(
            "featured_game_id"
        )

        if featured is None:

            imported, game = self.generate_today()

            return game

        return self.games.game_by_id(
            int(featured)
        )

    def refresh_today(self):

        game = self.games.random_game()

        self.state.set(
            "featured_game_id",
            game["id"]
        )

        return game

