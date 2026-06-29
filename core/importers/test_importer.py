from core.providers.rawg_client import RAWGProvider
from core.importers.game_importer import GameImporter

provider = RAWGProvider()
importer = GameImporter()

search = provider.search_game("Terraria")

details = provider.get_game_details(search["id"])

game = importer.map_rawg(details)

print(game)