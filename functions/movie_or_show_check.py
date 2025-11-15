# Local Imports
from debug_print import debug_print

# External Imports
import requests
import urllib.parse

### Determine if the media folder is related to movies or shows
def movie_or_show_check(headers: dict, working_dir: str, media_id: str, debug: bool = False) -> str:
    search_uri = "https://api.themoviedb.org/3/search/multi?query={}&include_adult=true"

    # Extract media title for search from the media directory
    media_search_term = working_dir.split('/')[-1].split(' (')[0]

    # URL-Encode the media title, incase it has special characters
    formatted_search_uri = search_uri.format(urllib.parse.quote(media_search_term))

    search_response = requests.get(movie_keywords_uri.format(media_id), headers=headers).json()
    debug_print('Search Response: {}'.format(search_response), debug)
    search_response_results = search_response['results']
    debug_print('Search Response Results: {}'.format(search_response_results), debug)

    if len(search_response_results) == 0:
        return 'No Search Results'

    for i in search_response_results:
        debug_print('item: {}'.format(i), debug)
        if i['id'] == int(media_id):
            return i['media_type']

    return 'Not Found within First Page of Results'