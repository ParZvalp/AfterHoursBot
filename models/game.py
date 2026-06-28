class Game:

    def __init__(
        self,
        id,
        name,
        description,
        genre,
        players,
        release_year,
        platform,
        developer,
        steam_appid,
        steam_url,
        cover,
        rating,
        price,
        tags
    ):
        self.id = id
        self.name = name
        self.description = description
        self.genre = genre
        self.players = players
        self.release_year = release_year
        self.platform = platform
        self.developer = developer
        self.steam_appid = steam_appid
        self.steam_url = steam_url
        self.cover = cover
        self.rating = rating
        self.price = price
        self.tags = tags