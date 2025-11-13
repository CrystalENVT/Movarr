# Local Imports
from debug_print import debug_print

# External Imports
import os
import toml

# From Imports
from typing import Dict

### Logic for handling checking directory against local check
def local_cache_check(current_working_dir: str, media_id: str, debug: bool = False) -> Dict['is_cached':bool, 'is_complete':bool]:

    files_in_working_dir = os.listdir('{}'.format(current_working_dir))

    toml_cache_name = '{}_cache.toml'.format(media_id)

    is_cached = False
    is_complete = False

    if toml_cache_name in files_in_working_dir:
        toml_path = '{}/{}'.format(current_working_dir, toml_cache_name)
        debug_print(toml_path, debug)

        cache_toml_string = ""
        with open('{}/{}_cache.toml'.format(current_working_dir, media_id), 'r') as cache_file:
            cache_toml_string = cache_file.read()

        toml_cache_contents = toml.loads(cache_toml_string)
        is_cached = True

        # Put cache contents in variables to work with
        number_of_seasons = toml_cache_contents['number_of_seasons']     # int
        episodes_per_season = toml_cache_contents['episodes_per_season'] # list of ints
        media_is_anime = toml_cache_contents['media_is_anime']           # bool

        # check if contents of working dir match the cached metadata
        if not (len(files_in_working_dir) - 1) == number_of_seasons:
            return {'is_cached': is_cached, 'is_complete': is_complete}
        
        for i in files_in_working_dir:
            if os.path.isfile(i):
                continue
            elif os.path.isdir(i):
                # default to "Season 0" for the specials
                season_number = 0
                # get the number at the end of the string
                if i.split(' ')[1].isdigit():
                    season_number = int(i.split(' ')[1])
                number_of_episodes = len(os.listdir('{}/{}'.format(current_working_dir, i)))
                if number_of_episodes == episodes_per_season[str(season_number)]:
                    continue
                else:
                    return {'is_cached': is_cached, 'is_complete': is_complete}
                is_complete = True

        move_media_folder(current_working_dir, 'tv', media_is_anime)

        return {'is_cached': is_cached, 'is_complete': is_complete}
    else:
        debug_print('No cache file found at {}/{}'.format(current_working_dir, toml_cache_name), debug)
        return {'is_cached': is_cached, 'is_complete': is_complete}