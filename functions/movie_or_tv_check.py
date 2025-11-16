# Local Imports
from debug_print import debug_print

# External Imports
import requests
import urllib.parse

### Determine if the media folder is related to movies or shows
def movie_or_tv_check(headers: dict, working_dir: str, media_id: str, debug: bool = False) -> str:
    search_uri = "https://api.themoviedb.org/3/search/multi?query={}&include_adult=true"

    # Extract media title for search from the media directory
    media_search_term = working_dir.split('/')[-1].split(' (')[0]

    debug_print('[MOTC] - Search Term: {}'.format(media_search_term), debug)

    # URL-Encode the media title, incase it has special characters
    formatted_search_uri = search_uri.format(urllib.parse.quote(media_search_term))

    debug_print('[MOTC] - Search URI: {}'.format(formatted_search_uri), debug)

    search_response = requests.get(formatted_search_uri, headers=headers).json()
    debug_print('[MOTC] - Search Response: {}'.format(search_response), debug)
    search_response_results = search_response['results']
    debug_print('[MOTC] - Search Response Results: {}'.format(search_response_results), debug)

    if len(search_response_results) == 0:
        return 'No Search Results'

    for i in search_response_results:
        debug_print('[MOTC] - item: {}'.format(i), debug)
        if i['id'] == int(media_id):
            return i['media_type']

    return 'Not Found within First Page of Results'