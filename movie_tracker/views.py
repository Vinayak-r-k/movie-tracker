# https://api.themoviedb.org/3/tv/popular?api_key=e06f3aebdca89458f15723bfe3e85ded


from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
import requests

from django.conf import settings
import time
def home(request):

    query = request.GET.get("q")

    movies=None

    if query:
        movies = search_movies(query)
        return render(request, "home.html", {"movies": movies["results"]if movies else [] })

    else:
        movies = todays_trending_movies()
        tv=weekly_trending_movies()

        return render(request, "view_movie.html", {"movies": movies["results"] if movies else [],"tv":tv["results"]if tv else []})
    return None

    # return render(request, "view_movie.html", {"movies": movies})

BASE_URL = "https://api.themoviedb.org/3"


# def search_movies(query):
#     resp = requests.get(f"{BASE_URL}/search/movie", params={
#         "api_key": settings.TMDB_API_KEY, "query": query
#     })
#     data = resp.json()
#
#     for movie in data["results"]:
#         if movie["poster_path"]:
#             movie["poster_url"] = ("https://image.tmdb.org/t/p/w500"+ movie["poster_path"])
#         else:
#             movie["poster_url"] = None
#
#     return data
def search_movies(query):
    cache_key = f"search_{query.lower()}"
    data = cache.get(cache_key)

    if data:
        return data

    try:

        resp = requests.get(f"{BASE_URL}/search/movie",params={"api_key": settings.TMDB_API_KEY,"query": query},timeout=10 )

        resp.raise_for_status()
        data = resp.json()

        for movie in data.get("results", []):
            if movie.get("poster_path"):
                movie["poster_url"] = (
                    "https://image.tmdb.org/t/p/w500" +
                    movie["poster_path"]
                )

            else:
                movie["poster_url"] = None

        cache.set(cache_key, data, 300)
        return data

    except requests.exceptions.RequestException as e:
        print("TMDB Error:", e)
        print("no movie")
        return None

def get_movie_details(tmdb_id):
    resp = requests.get(f"{BASE_URL}/movie/{tmdb_id}", params={
        "api_key": settings.TMDB_API_KEY
    })
    return resp.json()
import requests
from django.conf import settings

BASE_URL = "https://api.themoviedb.org/3"

# def todays_trending_movies():
#     url = f"{BASE_URL}/trending/movie/day"
#
#     params = {
#         "api_key": settings.TMDB_API_KEY
#     }
#
#
#     # response = requests.get(url, params=params)
#     try:
#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print("TMDB Error:", e)
#         return None
#
#     if response.status_code == 200:
#         return response.json()
#
#     return None
trending_cache = None

def todays_trending_movies():
    global trending_cache

    if trending_cache:
        return trending_cache

    url = f"{BASE_URL}/trending/movie/day"

    response = requests.get(
        url,
        params={"api_key": settings.TMDB_API_KEY},
        timeout=10
    )

    response.raise_for_status()
    trending_cache = response.json()
    return trending_cache
tv_cache=None
def weekly_trending_movies():
    global tv_cache

    if tv_cache:
        return tv_cache
    url = f"{BASE_URL}/tv/popular"

    params = {
        "api_key": settings.TMDB_API_KEY
    }

    # response = requests.get(url, params=params)
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        tv_cache = response.json()
        return tv_cache
        # return response.json()
    except requests.exceptions.RequestException as e:
        print("TMDB Error:", e)
        return None

    if response.status_code == 200:
        return response.json()

    return None
from django.shortcuts import render

