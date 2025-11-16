
# Needed to be able to import from functions
import sys
sys.path.append('./functions')

# function to test
import move_media_folder

# additional external libraries
import os

# Test library
import pytest

@pytest.mark.parametrize(
        'given_media_type,given_media_is_anime',
        [
            (
                'movie',
                False
            ),
            (
                'tv',
                False
            ),
            (
                'movie',
                True
            ),
            (
                'tv',
                True
            ),
        ]
)
def test_move_media_folder(given_media_type: str, given_media_is_anime: bool, mocker):

    # Load fake paths into environment variables
    os.environ['anime_{}_output_directory'.format(given_media_type)] = 'shutil'
    os.environ['{}_output_directory'.format(given_media_type)] = 'shutil'

    # mock shutil
    mocked_shutil = mocker.patch('move_media_folder.shutil.move')

    move_media_folder.move_media_folder(
        given_media_type,
        given_media_type,
        given_media_is_anime
        )
    mocked_shutil.assert_called_with(given_media_type, 'shutil/{}'.format(given_media_type))