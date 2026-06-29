import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot.scheduler.tasks import TaskScheduler

load_dotenv()

TOKEN = os.getenv("TOKEN")
SERVER_ID = int(os.getenv("SERVER_ID"))


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
        # Load all cogs
        extensions = [
            "bot.cogs.games",
            "bot.cogs.dev",
            "bot.cogs.admin",
            # "cogs.fun",
            # "cogs.utility",
            # "cogs.events",
            # "cogs.daily",
        ]

        for extension in extensions:
            await self.load_extension(extension)

        # Sync commands only to your development server
        guild = discord.Object(id=SERVER_ID)

        # Copy all global commands to your development server
        self.tree.copy_global_to(guild=guild)

        synced = await self.tree.sync(guild=guild)

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
                print(e)


bot = AfterHoursBot()

bot.run(TOKEN)