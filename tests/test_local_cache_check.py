
# Needed to be able to import from functions
import sys
sys.path.append('./functions')

# function to test
import local_cache_check

# additional external libraries
import os

# Test library
import pytest

@pytest.mark.parametrize(
        'given_current_working_dir,given_media_is_anime,expected',
        [
            (
                '{}/testdata/local_cache_check/uncached',
                True,
                {'is_cached': False, 'is_complete': False},
            ),
            (
                '{}/testdata/local_cache_check/cached_incomplete_1',
                True,
                {'is_cached': True, 'is_complete': False},
            ),
            (
                '{}/testdata/local_cache_check/cached_incomplete_2',
                True,
                {'is_cached': True, 'is_complete': False},
            ),
            (
                '{}/testdata/local_cache_check/cached_incomplete_3',
                True,
                {'is_cached': True, 'is_complete': False},
            ),
            (
                '{}/testdata/local_cache_check/cached_complete_1',
                True,
                {'is_cached': True, 'is_complete': True},
            ),
            (
                '{}/testdata/local_cache_check/cached_complete_2',
                True,
                {'is_cached': True, 'is_complete': True},
            ),
        ]
)
def test_local_cache_check(given_current_working_dir: str, given_media_is_anime: bool, expected: Dict['is_cached':bool, 'is_complete':bool], mocker):
    # Mock move_media_folder function, as we aren't testing that functionality
    mocked_move_media = mocker.patch('local_cache_check.move_media_folder')

    # Get current working path
    base_path = os.path.dirname(os.path.realpath(__file__))
    assert local_cache_check.local_cache_check(
        given_current_working_dir.format(base_path),
        'test',
        debug=True
        ) == expected
    if expected == {'is_cached': True, 'is_complete': True}:
        mocked_move_media.assert_called_with(given_current_working_dir.format(base_path), 'tv', given_media_is_anime)