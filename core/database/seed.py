import json

from database.game_repository import GameRepository


repo = GameRepository()

with open("data/games.json", "r", encoding="utf-8") as file:
    games = json.load(file)


# Prevent duplicate imports
existing_games = repo.all_games()

if len(existing_games) > 0:
    print("⚠️ Database already contains games.")
    print("Delete afterhours.db if you want a fresh import.")
    exit()


for game in games:

    repo.add_game(
        (
            game["name"],
            game["description"],
            game["genre"],
            game["players"],
            game["release_year"],
            game["platform"],
            game["developer"],
            game["steam_url"],
            game["cover"]
        )
    )

print(f"✅ Successfully imported {len(games)} games!")