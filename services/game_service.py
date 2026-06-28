import json
import discord

from database.game_repository import GameRepository


class GameService:

    def __init__(self):

        self.repo = GameRepository()

        with open("data/history.json", "r", encoding="utf-8") as file:
            self.history = json.load(file)

    def random_game(self):

        last_game = self.history["last_game"]

        while True:

            game = self.repo.random_game()

            if game is None:
                raise Exception("No games found in the database.")

            if game["name"] != last_game:
                break

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

        embed.add_field(
            name="📅 Release",
            value=game["release_year"] or "Unknown",
            inline=True
        )

        embed.add_field(
            name="🖥️ Platform",
            value=game["platform"] or "Unknown",
            inline=True
        )

        embed.add_field(
            name="🏢 Developer",
            value=game["developer"] or "Unknown",
            inline=True
        )

        if game["steam_url"]:
            embed.add_field(
                name="🔗 Steam",
                value=game["steam_url"],
                inline=False
            )

        if game["cover"]:
            embed.set_image(url=game["cover"])

        embed.set_footer(text="AfterHoursBot")

        return embed