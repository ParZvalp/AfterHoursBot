import os
import requests

from dotenv import load_dotenv

load_dotenv()


class RAWGClient:

    BASE_URL = "https://api.rawg.io/api"

    def __init__(self):
        self.api_key = os.getenv("RAWG_API_KEY")

    def search_game(self, name):

        response = requests.get(
            f"{self.BASE_URL}/games",
            params={
                "key": self.api_key,
                "search": name,
                "page_size": 1
            }
        )

        response.raise_for_status()

        results = response.json()["results"]

        if not results:
            return None

        return results[0]
    
    def get_game_details(self, game_id):

        response = requests.get(
            f"{self.BASE_URL}/games/{game_id}",
            params={
                "key": self.api_key
            }
        )

        response.raise_for_status()

        return response.json()
    
    def get_popular_games(self, page=1):

        response = requests.get(
            f"{self.BASE_URL}/games",
            params={
                "key": self.api_key,
                "ordering": "-added",
                "page": page,
                "page_size": 20
            }
        )

        response.raise_for_status()

        return response.json()["results"]