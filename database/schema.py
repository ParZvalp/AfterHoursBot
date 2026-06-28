from database.db import Database


db = Database()


db.execute("""

CREATE TABLE IF NOT EXISTS games(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    description TEXT,

    genre TEXT,

    players TEXT,

    release_year INTEGER,

    platform TEXT,

    developer TEXT,

    steam_url TEXT,

    cover TEXT

)

""")

print("✅ Database Ready")