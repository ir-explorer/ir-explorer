"""Integration tests for miscellaneous functionality."""

import requests


def test_available_languages(api):
    assert requests.get(f"{api}/get_available_languages").json() == ["English"]


def test_no_corpora(api):
    assert requests.get(f"{api}/get_corpora").json() == []
