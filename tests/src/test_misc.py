"""Integration tests for miscellaneous functionality."""

import requests


def test_available_languages(api):
    assert requests.get(f"{api}/get_available_languages").json() == ["English"]


def test_available_options(api):
    assert requests.get(f"{api}/get_available_options").json() == {
        "query_languages": ["English"],
        "corpus_names": [],
        "model_names": [],
    }


def test_corpora(api):
    assert requests.get(f"{api}/get_corpora").json() == []
