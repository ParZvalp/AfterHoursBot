import json
import random
import discord

from discord.ext import commands
from discord import app_commands


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="game",
        description="Get a random game recommendation."
    )
    async def game(self, interaction: discord.Interaction):

        with open(
            "data/games.json",
            encoding="utf-8"
        ) as file:

            games = json.load(file)

        game = random.choice(games)

        embed = discord.Embed(
            title=f"🎮 {game['name']}",
            description=game["description"],
            color=discord.Color.green()
        )

        embed.add_field(
            name="🎯 Genre",
            value=game["genre"]
        )

        embed.add_field(
            name="👥 Players",
            value=game["players"]
        )

        embed.set_footer(
            text="AfterHoursBot"
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Games(bot))