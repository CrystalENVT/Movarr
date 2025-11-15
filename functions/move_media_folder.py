import os
import shutil

def move_media_folder(current_working_dir: str, media_type: str, media_is_anime: bool):
    output_directory = ''
    if media_is_anime == True:
        output_directory = os.getenv('anime_{}_output_directory'.format(media_type)).replace('~',os.getenv('HOME'))
    else:
        output_directory = os.getenv('{}_output_directory'.format(media_type)).replace('~',os.getenv('HOME'))
    shutil.move(current_working_dir, output_directory)