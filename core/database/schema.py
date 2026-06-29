from core.database.db import Database

db = Database()

# =========================
# Games Table
# =========================

db.execute("""
CREATE TABLE IF NOT EXISTS games (

    id SERIAL PRIMARY KEY,

    provider TEXT NOT NULL,
    provider_id INTEGER NOT NULL,

    name TEXT NOT NULL,
    slug TEXT,

    description TEXT,

    released TEXT,

    rating REAL,
    metacritic INTEGER,

    genres TEXT,
    platforms TEXT,

    developers TEXT,
    publishers TEXT,

    website TEXT,

    image TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(provider, provider_id)

)
""")

# =========================
# Bot State Table
# =========================

db.execute("""
CREATE TABLE IF NOT EXISTS bot_state (

    key TEXT PRIMARY KEY,

    value TEXT

)
""")

print("✅ Database Ready")