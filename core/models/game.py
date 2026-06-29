from dataclasses import dataclass


@dataclass
class Game:

    provider: str
    provider_id: int

    name: str
    slug: str

    description: str

    released: str

    rating: float
    metacritic: int

    genres: str
    platforms: str

    developers: str
    publishers: str

    website: str

    image: str