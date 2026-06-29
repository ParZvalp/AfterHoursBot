
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.config import Config

from bot.services.recommendation_service import RecommendationService
from bot.services.panel_service import PanelService


class TaskScheduler:

    def __init__(self, bot):

        self.bot = bot

        self.config = Config()

        self.scheduler = AsyncIOScheduler(
            timezone=self.config.timezone
        )

    def start(self):

        print("✅ Scheduler Started")

        # Sync games and generate today's featured game
        # Runs every day at 2:00 AM
        self.scheduler.add_job(
            self.sync_games,
            trigger="cron",
            hour=2,
            minute=0,
            id="sync_games"
        )

        # Update the persistent Discord dashboard
        # Runs every day at 8:00 AM
        self.scheduler.add_job(
            self.update_panel,
            trigger="cron",
            hour=8,
            minute=0,
            id="update_panel"
        )

        self.scheduler.start()

        print(self.scheduler.get_jobs())

    async def sync_games(self):

        try:

            print("🔄 Syncing games...")

            service = RecommendationService()

            imported, game = service.generate_today()

            print(
                f"✅ Imported {imported} new game(s)."
            )

            print(
                f"🎮 Today's Featured Game: {game['name']}"
            )

        except Exception as e:

            print(
                f"❌ Sync failed: {e}"
            )

    async def update_panel(self):

        try:

            print("🎮 Updating dashboard...")

            panel = PanelService(
                self.bot
            )

            await panel.update()

            print(
                "✅ Dashboard updated."
            )

        except Exception as e:

            print(
                f"❌ Dashboard update failed: {e}"
            )
