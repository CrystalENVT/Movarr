# Local Imports
from debug_print import debug_print
from move_media_folder import move_media_folder

# External Imports
import os
import toml

# From Imports
from typing import Dict

### Logic for handling checking directory against local check
def local_cache_check(current_working_dir: str, media_id: str, debug: bool = False) -> Dict['is_cached':bool, 'is_complete':bool]:

    files_in_working_dir = os.listdir('{}'.format(current_working_dir))
    debug_print('Files in Working Directory: {}'.format(files_in_working_dir), debug)

    toml_cache_name = '{}_cache.toml'.format(media_id)

    # Assume not cached, & must be proven it is cached
    is_cached = False
    # Initially assume that since cache does not exist, it is not complete 
    is_complete = False

    if toml_cache_name in files_in_working_dir:
        toml_path = '{}/{}'.format(current_working_dir, toml_cache_name)
        debug_print(toml_path, debug)

        cache_toml_string = ""
        with open('{}/{}_cache.toml'.format(current_working_dir, media_id), 'r') as cache_file:
            cache_toml_string = cache_file.read()

        toml_cache_contents = toml.loads(cache_toml_string)
        debug_print('Toml Cache Contents\n{}'.format(toml_cache_contents), debug)
        is_cached = True

        # Put cache contents in variables to work with
        number_of_seasons = toml_cache_contents['number_of_seasons']     # int
        episodes_per_season = toml_cache_contents['episodes_per_season'] # list of ints
        media_is_anime = toml_cache_contents['media_is_anime']           # bool

        # check if contents of working dir match the cached metadata
        if not (len(files_in_working_dir) - 1) >= number_of_seasons:
            debug_print('Not Enough Season Folders - is_cached: {}; is_complete: {}'.format(is_cached, is_complete), debug)
            return {'is_cached': is_cached, 'is_complete': is_complete}

        debug_print('Enough Season Folders found, continuing to check episode count', debug)

        # We will now assume it is complete,
        #   but will revert to not complete if there is a count mis-match
        is_complete = True
        for i in files_in_working_dir:
            file_name = '{}/{}'.format(current_working_dir, i)
            if os.path.isfile(file_name):
                debug_print('{} is a file, skipping'.format(i), debug)
                continue
            elif os.path.isdir(file_name):
                debug_print('Checking folder: {}'.format(i), debug)

                if len(i.split(' ')) >= 1 and i.split(' ')[1].isdigit():
                    season_number = int(i.split(' ')[1])
                else:
                    # This is for specials. Should be the 'Specials' folder,
                    #   but leaving this generic for flexibility
                    season_number = 0
                debug_print('Parsed Season Number: {}'.format(season_number), debug)

                number_of_episodes = len(os.listdir('{}/{}'.format(current_working_dir, i)))
                debug_print('Number of episodes for Season {}: {}'.format(season_number, number_of_episodes), debug)

                if number_of_episodes == episodes_per_season[str(season_number)]:
                    debug_print('Episode Count matches', debug)
                    continue
                else:
                    debug_print('Episode Count does not match', debug)
                    is_complete = False
                    return {'is_cached': is_cached, 'is_complete': is_complete}
        move_media_folder(current_working_dir, 'tv', media_is_anime)

        return {'is_cached': is_cached, 'is_complete': is_complete}
    else:
        debug_print('No cache file found at {}/{}'.format(current_working_dir, toml_cache_name), True)
        return {'is_cached': is_cached, 'is_complete': is_complete}