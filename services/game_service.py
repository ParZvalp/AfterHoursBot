import json
import random
import discord


class GameService:

    def __init__(self):

        with open("data/games.json", "r", encoding="utf-8") as file:
            self.games = json.load(file)

        with open("data/history.json", "r", encoding="utf-8") as file:
            self.history = json.load(file)

    def random_game(self):

        last_game = self.history["last_game"]

        available = [
            game for game in self.games
            if game["name"] != last_game
        ]

        game = random.choice(available)

        self.history["last_game"] = game["name"]

        with open("data/history.json", "w", encoding="utf-8") as file:
            json.dump(self.history, file, indent=4)

        return game

    def create_embed(self, title="🎮 Random Game Recommendation"):

        game = self.random_game()

        embed = discord.Embed(
            title=title,
            description=f"**{game['name']}**\n\n{game['description']}",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🎯 Genre",
            value=game["genre"],
            inline=True
        )

        embed.add_field(
            name="👥 Players",
            value=game["players"],
            inline=True
        )

        embed.set_footer(text="AfterHoursBot")

        return embed