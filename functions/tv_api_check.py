# Local Imports
from debug_print import debug_print

# External Imports
import os
import requests

### Logic for checking tv api
def tv_api_check(headers, current_working_dir, media_id, debug=False):

    # To be formatted with the tv series name
    tv_details_uri = "https://api.themoviedb.org/3/tv/{}"
    tv_keywords_uri = "https://api.themoviedb.org/3/tv/{}/keywords"

    tv_details_response = requests.get(tv_details_uri.format(media_id), headers=headers).json()
    # This below one might be too beefy for general debug logs
    # debug_print('TV_details_Response: {}'.format(tv_details_response), debug)

    seasons_array = tv_details_response['seasons']

    # Prep to cache media details for next run
    number_of_seasons = tv_details_response['number_of_seasons']
    
    episodes_per_season = {}
    for season in seasons_array:
        if (season['season_number'] != 0) or ('include_specials' in os.environ and os.getenv('include_specials') == "true"):
            episodes_per_season[str(season['season_number'])] = season['episode_count']
    debug_print(episodes_per_season, debug)

    tv_response = requests.get(tv_keywords_uri.format(media_id), headers=headers).json()

    # TV api uses `results` as the array containing all of the keywords
    #   https://developer.themoviedb.org/reference/tv-series-keywords
    tv_response_keywords = tv_response['results']
    tv_keywords = [keywords['name'] for keywords in tv_response_keywords]

    media_is_anime = False
    if 'anime' in tv_keywords:
        media_is_anime = True

    debug_print("ID {} - TV Keywords: {}".format(media_id, tv_keywords), debug)
    debug_print("ID {} is Anime (After TV): {}".format(media_id, media_is_anime), debug)

    new_cache_data = {'number_of_seasons': number_of_seasons, 'episodes_per_season': episodes_per_season, 'media_is_anime': media_is_anime}
    debug_print(new_cache_data, debug)

    cache_toml_string = toml.dumps(new_cache_data)
    debug_print(cache_toml_string, debug)

    with open('{}/{}_cache.toml'.format(current_working_dir, media_id), 'w') as cache_file:
        cache_file.write(cache_toml_string)

    # We'll go ahead & run the cache check, instead of re-writing logic
    cache_response = local_cache_check(current_working_dir, media_id, debug)

    if cache_response.get('is_complete') == True:
        return # This directory has now been moved, so no need to do further checks
    elif cache_response.get('is_cached') == True:
        print('Media Metadata has been cached, will monitor for completion')
        return