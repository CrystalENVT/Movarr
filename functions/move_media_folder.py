import os
import shutil

def move_media_folder(current_working_dir: str, media_type: str, media_is_anime: bool):
    output_directory = ''
    if media_is_anime == True:
        output_directory = os.environ('anime_{}_output_directory').replace('~',os.getenv('HOME'))
    else:
        output_directory = os.environ('{}_output_directory').replace('~',os.getenv('HOME'))
    shutil.move(current_working_dir, output_directory)