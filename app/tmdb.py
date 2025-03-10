import requests
from config import TMDB_API_KEY

def search_tv_shows(query):
    url=f"https://api.themoviedb.org/3/search/tv"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query
    }

    response = requests.get(url, params=params)
    return response.json()