import json
import random
import discord


class GameService:

    def __init__(self):
        with open("data/games.json", "r", encoding="utf-8") as file:
            self.games = json.load(file)

    def random_game(self):
        return random.choice(self.games)

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