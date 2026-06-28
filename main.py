import os
import asyncio
import discord
from scheduler.tasks import TaskScheduler
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")


class AfterHoursBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):

        extensions = [
            "cogs.games",
        ]

        for extension in extensions:
            await self.load_extension(extension)

        synced = await self.tree.sync()

        print(f"✅ Synced {len(synced)} command(s)")

    async def on_ready(self):

        print("=" * 40)
        print(f"Logged in as {self.user}")
        print("=" * 40)

        if not hasattr(self, "scheduler_started"):
            self.scheduler_started = True

            try:
                self.scheduler = TaskScheduler(self)
                self.scheduler.start()
            except Exception as e:
                print("❌ Scheduler failed to start:")
                print(repr(e))


bot = AfterHoursBot()

bot.run(TOKEN)