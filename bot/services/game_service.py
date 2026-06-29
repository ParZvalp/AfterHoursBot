
from bot.embeds.game_embed import GameEmbed

from core.database.game_repository import GameRepository


class GameService:

    def __init__(self):

        self.repo = GameRepository()

        self.last_game_id = None

    def random_game(self):

        game = self.repo.random_game(self.last_game_id)

        if game is None:
            raise Exception("No games found in the database.")

        self.last_game_id = game["id"]

        return game

    def game_by_id(self, game_id):

        game = self.repo.game_by_id(game_id)

        if game is None:
            raise Exception("Game not found.")

        return game

    def create_embed(
        self,
        game,
        title="🎮 Random Game Recommendation"
    ):

        return GameEmbed.create(
            game,
            title
        )
