
# Needed to be able to import from functions
import sys
sys.path.append('./functions')

# function to test
import tv_api_check

# additional external libraries
import os
import json

# Test library
import pytest

@pytest.mark.parametrize(
        'given_current_working_dir,given_media_is_anime',
        [
            (
                '{}/testdata/tv_api_check/not_anime',
                False
            ),
            (
                '{}/testdata/tv_api_check/is_anime',
                True
            ),
        ]
)
def test_tv_api_check(given_current_working_dir: str, given_media_is_anime: bool, mocker):
    # Get current working path
    base_path = os.path.dirname(os.path.realpath(__file__))

    # Mock local_cache_check function, as we aren't testing that functionality
    mocked_local_cache_check = mocker.patch('tv_api_check.local_cache_check', return_value={'is_cached': False, 'is_complete': False})

    # Mock out the API call to TMDB
    # details api call
    mocked_details_json = {}
    with open('{}/details.json'.format(given_current_working_dir.format(base_path)), 'r') as given_details_json_file:
        mocked_details_json = json.loads(given_details_json_file.read())

    mock_details_response = mocker.Mock()
    mock_details_response.status_code = 200
    mock_details_response.json.return_value = mocked_details_json

    # keywords api call
    mocked_keywords_json = {}
    with open('{}/keywords.json'.format(given_current_working_dir.format(base_path)), 'r') as given_keywords_json_file:
        mocked_keywords_json = json.loads(given_keywords_json_file.read())

    mock_keywords_response = mocker.Mock()
    mock_keywords_response.status_code = 200
    mock_keywords_response.json.return_value = mocked_keywords_json

    # wire in the responses into the Mock API call.
    #   Side effects allows for the value of the return to change per execution
    mock_get = mocker.patch('tv_api_check.requests.get', return_value={})
    mock_get.side_effect=[mock_details_response,mock_keywords_response]

    # Mock opening the cache file that would be written to
    #   This mock needs to happen after the `with open` statements above
    mocker.patch('builtins.open')

    tv_api_check.tv_api_check(
        {},
        given_current_working_dir.format(base_path),
        str(mocked_keywords_json['id']),
        debug=True
        )
    mocked_local_cache_check.assert_called_with(given_current_working_dir.format(base_path), str(mocked_keywords_json['id']), True)