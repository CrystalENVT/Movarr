# Local Imports
from debug_print import debug_print

# External Imports
import requests

### Logic for checking movie api
def movie_api_check(headers: dict, working_dir: str, media_id: str, debug: bool = False):
    # To be formatted with the tv series name
    movie_keywords_uri = "https://api.themoviedb.org/3/movie/{}/keywords"

    # Movie api uses `keywords` as the array containing all of the keywords
    #   https://developer.themoviedb.org/reference/movie-keywords
    movie_response = requests.get(movie_keywords_uri.format(media_id), headers=headers).json()
    movie_response_keywords = movie_response['keywords']
    movie_keywords = [keywords['name'] for keywords in movie_response_keywords]

    media_is_anime = False
    if 'anime' in movie_keywords:
        media_is_anime = True

    debug_print("ID {} - Movie Keywords: {}".format(media_id, movie_keywords), DEBUG_FLAG)
    debug_print("ID {} is Anime (After Movie): {}".format(media_id, media_is_anime), DEBUG_FLAG)

    move_media_folder(current_working_dir, 'movie', media_is_anime)