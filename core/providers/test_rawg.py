from core.providers.rawg_client import RAWGProvider

provider = RAWGProvider()

game = provider.search_game("Terraria")

details = provider.get_game_details(game["id"])

print(details["name"])
print(details["released"])
print(details["metacritic"])
print(details["description_raw"][:300])