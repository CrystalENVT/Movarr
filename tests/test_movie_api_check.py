
# Needed to be able to import from functions
import sys
sys.path.append('./functions')

# function to test
import movie_api_check

# additional external libraries
import os
import json

# Test library
import pytest

@pytest.mark.parametrize(
        'given_current_working_dir,given_json_name,given_media_is_anime',
        [
            (
                '{}/testdata/movie_api_check/not_anime',
                'not_anime',
                False
            ),
            (
                '{}/testdata/movie_api_check/is_anime',
                'is_anime',
                True
            ),
        ]
)
def test_movie_api_check(given_current_working_dir: str, given_json_name: str, given_media_is_anime: bool, mocker):
    # Get current working path
    base_path = os.path.dirname(os.path.realpath(__file__))

    mocked_request_json = {}
    with open('{}/{}.json'.format(given_current_working_dir.format(base_path), given_json_name), 'r') as given_json_file:
        mocked_request_json = json.loads(given_json_file.read())

    print(mocked_request_json)

    # Mock move_media_folder function, as we aren't testing that functionality
    mocked_move_media = mocker.patch('movie_api_check.move_media_folder')

    # Mock out the API call to TMDB
    mock_get = mocker.patch('movie_api_check.requests.get')

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mocked_request_json
    mock_get.return_value = mock_response

    movie_api_check.movie_api_check(
        {},
        given_current_working_dir.format(base_path),
        'test',
        debug=True
        )
    mocked_move_media.assert_called_with(given_current_working_dir.format(base_path), 'movie', given_media_is_anime)