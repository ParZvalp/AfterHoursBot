from core.providers.rawg_client import RAWGClient

client = RAWGClient()

games = client.get_popular_games()

for game in games:
    print(game["name"])