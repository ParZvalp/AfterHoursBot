import discord

from discord.ext import commands
from discord import app_commands

from bot.services.game_service import GameService


class Games(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.service = GameService()

    @app_commands.command(
        name="game",
        description="Get a random game recommendation."
    )
    async def game(
        self,
        interaction: discord.Interaction
    ):

        game = self.service.random_game()

        embed = self.service.create_embed(
            game,
            title="🎲 Random Game Recommendation"
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Games(bot))