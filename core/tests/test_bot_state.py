from core.database.bot_state_repository import BotStateRepository

repo = BotStateRepository()

repo.set("daily_message_id", 123456789)

print(repo.get("daily_message_id"))

repo.delete("daily_message_id")

print(repo.get("daily_message_id"))