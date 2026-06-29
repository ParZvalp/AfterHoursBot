import discord

from discord.ext import commands
from discord import app_commands

from core.database.game_repository import GameRepository
from core.importers.game_sync import GameSync

from bot.services.panel_service import PanelService


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.repo = GameRepository()

    @app_commands.command(
        name="syncgames",
        description="Synchronize games from RAWG."
    )
    async def syncgames(
        self,
        interaction: discord.Interaction,
        pages: app_commands.Range[int, 1, 50] = 1
    ):

        await interaction.response.defer()

        sync = GameSync()

        count = sync.sync_popular(pages)

        await interaction.followup.send(
            f"✅ Imported **{count}** new game(s)."
        )

    @app_commands.command(
        name="stats",
        description="View AfterHoursBot statistics."
    )
    async def stats(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer()

        total_games = self.repo.count_games()

        embed = discord.Embed(
            title="📊 AfterHoursBot Statistics",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🎮 Games in Database",
            value=f"**{total_games}**",
            inline=False
        )

        embed.set_footer(
            text="AfterHoursBot"
        )

        await interaction.followup.send(
            embed=embed
        )

    @app_commands.command(
        name="updatepanel",
        description="Create or update the persistent game dashboard."
    )
    async def updatepanel(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer()

        panel = PanelService(self.bot)

        await panel.update()

        await interaction.followup.send(
            "✅ Game dashboard updated."
        )


async def setup(bot):
    await bot.add_cog(Admin(bot))