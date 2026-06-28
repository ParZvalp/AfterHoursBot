import json
import random
import discord
from services.game_service import GameService
from discord.ext import commands
from discord import app_commands


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.service = GameService()

    @app_commands.command(
        name="game",
        description="Get a random game recommendation."
    )
    async def game(self, interaction: discord.Interaction):

        embed = self.service.create_embed()

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Games(bot))