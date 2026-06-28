from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from config import Config
from services.game_service import GameService

class TaskScheduler:

    def __init__(self, bot):
        self.bot = bot
        self.config = Config()
        self.scheduler = AsyncIOScheduler(timezone=self.config.timezone)

    def start(self):

        print("✅ Scheduler Started")

        self.scheduler.add_job(
            self.test_scheduler,
            trigger="interval",
            minutes=1,
            id="scheduler_test"
        )

        self.scheduler.start()

        print(self.scheduler.get_jobs())

    async def test_scheduler(self):

        print(f"⏰ Scheduler fired at {datetime.now()}")

        channel = self.bot.get_channel(
            self.config.daily_channel
        )

        if channel is None:
            print("❌ Channel not found!")
            return

        print(f"✅ Found channel: {channel.name}")

        service = GameService()

        embed = service.create_embed(
            title="🌅 Game of the Day"
        )

        await channel.send(embed=embed)