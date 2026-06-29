
import discord

from core.config import Config
from core.database.bot_state_repository import BotStateRepository

from bot.services.game_service import GameService
from bot.services.recommendation_service import RecommendationService


class PanelService:

    def __init__(self, bot):

        self.bot = bot

        self.config = Config()

        self.state = BotStateRepository()

        self.game_service = GameService()

        self.recommendation = RecommendationService()

    async def update(self):

        print("\n========== PANEL UPDATE ==========")

        print(f"Configured Channel ID: {self.config.daily_channel}")

        # ------------------------------------
        # Get the configured Discord channel
        # ------------------------------------

        channel = self.bot.get_channel(
            self.config.daily_channel
        )

        print(f"Channel Object: {channel}")

        if channel is None:

            print("❌ Daily channel not found.")

            return

        # ------------------------------------
        # Get today's featured game
        # ------------------------------------

        game = self.recommendation.current_game()

        print(f"Featured Game: {game['name']}")

        embed = self.game_service.create_embed(
            game,
            title="🎮 Featured Game"
        )

        # ------------------------------------
        # Get stored dashboard message
        # ------------------------------------

        message_id = self.state.get(
            "daily_message_id"
        )

        print(f"Stored Message ID: {message_id}")

        # ------------------------------------
        # First startup
        # ------------------------------------

        if message_id is None:

            print("No dashboard exists. Creating one...")

            message = await channel.send(
                embed=embed
            )

            self.state.set(
                "daily_message_id",
                message.id
            )

            print(
                f"✅ Created dashboard ({message.id})"
            )

            return

        # ------------------------------------
        # Existing dashboard
        # ------------------------------------

        try:

            print("Fetching existing dashboard...")

            message = await channel.fetch_message(
                int(message_id)
            )

            print(f"Fetched message: {message.id}")

            await message.edit(
                embed=embed
            )

            print(
                f"✅ Updated dashboard ({message.id})"
            )

        # ------------------------------------
        # Dashboard deleted
        # ------------------------------------

        except discord.NotFound:

            print("⚠ Dashboard not found.")
            print("Creating replacement dashboard...")

            message = await channel.send(
                embed=embed
            )

            self.state.set(
                "daily_message_id",
                message.id
            )

            print(
                f"✅ Recreated dashboard ({message.id})"
            )

        except Exception as e:

            print("❌ Unexpected error inside PanelService")

            import traceback
            traceback.print_exc()

            print(e)
