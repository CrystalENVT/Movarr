
# Needed to be able to import from functions
import sys
sys.path.append('./functions')

# function to test
import movie_or_tv_check

# additional external libraries
import os
import json

# Test library
import pytest

@pytest.mark.parametrize(
        # Using real API data, but changing the media_id to 1 for simplicity of testing
        'given_current_working_dir,expected',
        [
            (
                '{}/testdata/movie_or_tv_check/movie (year) [tmdbid-1]',
                'movie'
            ),
            (
                '{}/testdata/movie_or_tv_check/tv (year) [tmdbid-1]',
                'tv'
            ),
            (
                '{}/testdata/movie_or_tv_check/not_found_within_first_page (year) [tmdbid-1]',
                'Not Found within First Page of Results'
            ),
            (
                '{}/testdata/movie_or_tv_check/no_results (year) [tmdbid-1]',
                'No Search Results'
            ),
        ]
)
def test_movie_or_tv_check(given_current_working_dir: str, expected: str, mocker):
    # Get current working path
    base_path = os.path.dirname(os.path.realpath(__file__))

    mocked_request_json = {}
    with open('{}/response.json'.format(given_current_working_dir.format(base_path)), 'r') as given_json_file:
        mocked_request_json = json.loads(given_json_file.read())

    # Mock out the API call to TMDB
    mock_get = mocker.patch('movie_or_tv_check.requests.get')

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mocked_request_json
    mock_get.return_value = mock_response

    movie_or_tv_check.movie_or_tv_check(
        {},
        given_current_working_dir.format(base_path),
        '1',
        debug=True
        ) == expected