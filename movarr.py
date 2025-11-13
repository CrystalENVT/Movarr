# Needed to be able to import from functions
import sys
sys.path.append('./functions')

# Local Imports
from debug_print import debug_print
from local_cache_check import local_cache_check
from movie_api_check import movie_api_check
from movie_or_show_check import movie_or_show_check
from tv_api_check import tv_api_check
from debug_print import debug_print

# External Imports
import os

# From Imports
from dotenv import load_dotenv

# Primary functional flow for processing the media
#   Calls the other functions
def process_media(headers: dict, current_input_dir: str, subdir: str, debug: bool = False):
    # string format for jellyfin is [tmdbid-####]
    #  so splits ensure we get exactly the appropriate id
    media_id = i.split('tmdbid-')[1].split(']')[0]
    debug_print('media_id: {}'.format(media_id), debug)

    # working dir = input_dir/media_dir
    current_working_dir = '{}/{}'.format(current_input_dir, i)

    cache_response = local_cache_check(current_working_dir, media_id, debug)

    if cache_response.get('is_complete') == True:
        return # This directory has now been moved, so no need to do further checks
    elif cache_response.get('is_cached') == True:
        print('Directory is cached but not yet complete: {}'.format(i))
        return # This directory has a cache file, so we don't need to do another API call

    media_type_response = movie_or_show_check(headers, current_working_dir, media_id, debug)

    if media_type_response == 'movie':
        movie_api_check(headers, current_working_dir, media_id, debug)
    elif media_type_response == 'tv':
        tv_api_check(headers, current_working_dir, media_id, debug)
    else:
        print('Media Type for {} not found - Message: {}'.format(current_working_dir, media_type_response))

#################################
### MAIN FUNCTION STARTS HERE ###
#################################

# key-value pairs from .env get loaded into the os environment
load_dotenv()

# DEBUG_FLAG will be used for debug prints
DEBUG_FLAG = False
if 'DEBUG' in os.environ and os.getenv('DEBUG') == "true":
    DEBUG_FLAG = True

# setup headers for tmdb api calls
headers = {"Authorization": "Bearer {}".format(os.getenv('tmdb_v4_read_access_token'))}

input_directories = os.getenv('input_directories').replace('~',os.getenv('HOME')).split(';')
debug_print("Input Directories: {}".format(input_directories), DEBUG_FLAG)

for current_input_dir in input_directories:
    subdirectories = os.listdir(current_input_dir)
    for i in subdirectories:
        if not 'tmdbid' in i:
            continue
        process_media(headers, current_input_dir, i, DEBUG_FLAG)