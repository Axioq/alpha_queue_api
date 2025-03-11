import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.tmdb import fetch_episodes_for_season
from app.watch_history import insert_episode

def load_full_show(show_id, show_name, num_seasons):
    for season in range(1, num_seasons + 1):
        print(f"📦 Fetching Season {season}...")
        episodes = fetch_episodes_for_season(show_id, season)
        for ep in episodes:
            episode_number = ep.get("episode_number")
            title = ep.get("name", "")
            air_date = ep.get("air_date")
            insert_episode(show_id, show_name, season, episode_number, title, air_date)

# Example: Load "Suits" which has 9 seasons
load_full_show(show_id=37680, show_name="Suits", num_seasons=9)