import discord
from discord.ext import commands
from discord import app_commands

from bot.services.game_service import GameService


class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="dailytest",
        description="Test the daily Game of the Day post."
    )
    async def dailytest(self, interaction: discord.Interaction):

        service = GameService()

        embed = service.create_embed(
            title="🌅 Game of the Day"
        )

        await interaction.channel.send(embed=embed)

        await interaction.response.send_message(
            "✅ Daily test posted.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Dev(bot))