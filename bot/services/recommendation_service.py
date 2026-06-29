import json
import random
from datetime import datetime, timezone

from bot.services.game_service import GameService

from core.database.bot_state_repository import BotStateRepository
from core.importers.game_sync import GameSync


# --------------------------------------------------
# How many days to remember recently featured games
# --------------------------------------------------
RECENT_HISTORY_DAYS = 7

# --------------------------------------------------
# How many recent game IDs to keep in history
# --------------------------------------------------
RECENT_HISTORY_LIMIT = 30

# --------------------------------------------------
# Top percentage of scored games to pick from.
# 0.20 = pick randomly from the top 20% of scores.
# --------------------------------------------------
TOP_POOL_FRACTION = 0.30

# --------------------------------------------------
# Minimum pool size even if 20% is a small number
# --------------------------------------------------
MIN_POOL_SIZE = 5

# --------------------------------------------------
# Scoring weights
# --------------------------------------------------
WEIGHT_RATING     = 5.0   # RAWG rating is 0–5
WEIGHT_METACRITIC = 5.0   # Normalized from 0–100
WEIGHT_RECENCY    = 3.0   # Newer games score higher
WEIGHT_REPEAT     = -20.0 # Heavy penalty for recently featured games


class RecommendationService:

    def __init__(self):

        self.sync  = GameSync()
        self.games = GameService()
        self.state = BotStateRepository()

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def generate_today(self):
        """
        Sync latest games from RAWG, pick today's featured
        game using the weighted scorer, and persist the choice.
        """

        imported = self.sync.sync_popular()

        game = self._pick_weighted()

        self._save_featured(game)

        return imported, game

    def current_game(self):
        """
        Return today's featured game.
        If none is set yet, generate one.
        """

        featured_id = self.state.get("featured_game_id")

        if featured_id is None:
            _, game = self.generate_today()
            return game

        return self.games.game_by_id(int(featured_id))

    def refresh_today(self):
        """
        Force-pick a new featured game without syncing RAWG.
        Used by /updatepanel and the daily scheduler.
        """

        game = self._pick_weighted()

        self._save_featured(game)

        return game

    # --------------------------------------------------
    # Weighted scoring
    # --------------------------------------------------

    def _pick_weighted(self):
        """
        Score every game in the database and pick randomly
        from the top pool so results feel varied but quality.
        """

        all_games = self.games.repo.all_games()

        if not all_games:
            raise Exception("No games found in the database.")

        recent_ids = self._load_recent_ids()

        # Always exclude the current featured game outright
        current_id = self.state.get("featured_game_id")
        if current_id:
            all_games = [g for g in all_games if g["id"] != int(current_id)]

        if not all_games:
            raise Exception("No eligible games found.")

        scored = []

        for game in all_games:
            score = self._score_game(game, recent_ids)
            scored.append((score, game))

        scored.sort(key=lambda x: x[0], reverse=True)

        pool_size = max(
            MIN_POOL_SIZE,
            int(len(scored) * TOP_POOL_FRACTION)
        )

        top_pool = scored[:pool_size]

        _, chosen = random.choice(top_pool)

        return chosen

    def _score_game(self, game, recent_ids):
        """
        Compute a weighted score for a single game.

        Scoring components:
          - Rating:     RAWG community rating (0–5)
          - Metacritic: Critic score normalized to 0–5
          - Recency:    How recently the game was released
          - Repeat:     Heavy penalty if recently featured
        """

        score = 0.0

        # ---- Rating (0–5) ----
        rating = game["rating"]
        if rating:
            score += (float(rating) / 5.0) * WEIGHT_RATING

        # ---- Metacritic (0–100 → 0–5) ----
        metacritic = game["metacritic"]
        if metacritic:
            score += (float(metacritic) / 100.0) * WEIGHT_METACRITIC

        # ---- Recency: released date ----
        released = game["released"]
        if released:
            try:
                release_year = int(str(released)[:4])
                current_year = datetime.now(timezone.utc).year

                # Scale: games from this year score full points,
                # games older than 10+ years score near zero.
                age = max(0, current_year - release_year)
                recency = max(0.0, 1.0 - (age / 10.0))

                score += recency * WEIGHT_RECENCY

            except (ValueError, TypeError):
                pass

        # ---- Anti-repeat penalty ----
        if game["id"] in recent_ids:
            score += WEIGHT_REPEAT

        return score

    # --------------------------------------------------
    # Recent history helpers
    # --------------------------------------------------

    def _load_recent_ids(self):
        """
        Load the set of recently featured game IDs from bot_state.
        Returns a set of integers.
        """

        raw = self.state.get("featured_game_history")

        if raw is None:
            return set()

        try:
            return set(json.loads(raw))
        except (json.JSONDecodeError, TypeError):
            return set()

    def _save_featured(self, game):
        """
        Persist the chosen game as today's featured game and
        append its ID to the recent history log.
        """

        game_id = game["id"]

        # Save current featured game
        self.state.set("featured_game_id", game_id)

        # Update history
        recent = list(self._load_recent_ids())

        if game_id not in recent:
            recent.append(game_id)

        # Keep history capped at the limit
        if len(recent) > RECENT_HISTORY_LIMIT:
            recent = recent[-RECENT_HISTORY_LIMIT:]

        self.state.set(
            "featured_game_history",
            json.dumps(recent)
        )