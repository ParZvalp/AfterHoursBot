from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import Config
from services.game_service import GameService


class TaskScheduler:

    def __init__(self, bot):
        self.bot = bot
        self.config = Config()
        self.scheduler = AsyncIOScheduler(
            timezone=self.config.timezone
        )

    def start(self):

        print("✅ Scheduler Started")

        # Daily at 8:00 AM
        self.scheduler.add_job(
            self.post_game_of_the_day,
            trigger="cron",
            hour=8,
            minute=0,
            id="daily_game"
        )

        self.scheduler.start()

        print(self.scheduler.get_jobs())

    async def post_game_of_the_day(self):

        channel = self.bot.get_channel(
            self.config.daily_channel
        )

        if channel is None:
            print("❌ Daily channel not found.")
            return

        service = GameService()

        embed = service.create_embed(
            title="🌅 Game of the Day"
        )

        await channel.send(embed=embed)

        print("✅ Posted Game of the Day")