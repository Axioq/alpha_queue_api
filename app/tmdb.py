import requests
from config import TMDB_API_KEY

# Search for TV shows
def search_tv_shows(query):
    url=f"https://api.themoviedb.org/3/search/tv"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query
    }

    response = requests.get(url, params=params)
    return response.json()

# Fetch episodes for a season
def fetch_episodes_for_season(show_id, season_number):
    url = f"https://api.themoviedb.org/3/tv/{show_id}/season/{season_number}"
    params = {
        "api_key": TMDB_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch season {season_number}")
        return []

    data = response.json()
    return data.get("episodes", [])