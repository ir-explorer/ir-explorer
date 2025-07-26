"""Integration tests for miscellaneous functionality."""

import requests


def test_available_languages(api):
    assert requests.get(f"{api}/get_available_languages").json() == ["English"]


def test_search_options(api):
    assert requests.get(f"{api}/get_search_options").json() == {
        "query_languages": ["English"],
        "corpus_names": [],
    }


def test_corpora(api):
    assert requests.get(f"{api}/get_corpora").json() == []
