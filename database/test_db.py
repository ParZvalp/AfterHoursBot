from database.game_repository import GameRepository

repo = GameRepository()

games = repo.all_games()

print("===== GAMES =====")

for game in games:
    print(game["name"])

print("=================")