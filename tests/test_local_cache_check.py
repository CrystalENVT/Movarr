
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
        'given_current_working_dir,expected',
        [
            (
                '{}/testdata/cached_incomplete_1',
                {'is_cached': True, 'is_complete': False},
            ),
            (
                '{}/testdata/cached_incomplete_2',
                {'is_cached': True, 'is_complete': False},
            ),
            (
                '{}/testdata/cached_incomplete_3',
                {'is_cached': True, 'is_complete': False},
            ),
            (
                '{}/testdata/cached_complete_1',
                {'is_cached': True, 'is_complete': True},
            ),
            (
                '{}/testdata/cached_complete_2',
                {'is_cached': True, 'is_complete': True},
            ),
        ]
)
def test_local_cache_check(given_current_working_dir: str, expected: str, mocker):
    # Mock move_media_folder function, as we aren't testing that functionality
    mocker.patch('local_cache_check.move_media_folder')

    # Get current working path
    base_path = os.path.dirname(os.path.realpath(__file__))
    assert local_cache_check.local_cache_check(
        given_current_working_dir.format(base_path),
        'test',
        debug=True
        ) == expected