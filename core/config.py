import json


class Config:
    def __init__(self):
        with open("data/config.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)

    @property
    def timezone(self):
        return self.data["timezone"]

    @property
    def channels(self):
        return self.data["channels"]

    @property
    def daily_channel(self):
        return self.channels["daily"]

    @property
    def gaming_channel(self):
        return self.channels["gaming"]

    @property
    def logs_channel(self):
        return self.channels["logs"]