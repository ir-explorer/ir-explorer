"""Integration tests for miscellaneous functionality."""

import pytest
import requests


@pytest.fixture(scope="module", autouse=True)
def setup_data(api):
    requests.post(
        f"{api}/create_corpus",
        json={"name": "test_corpus", "language": "English"},
    )


def test_get_corpora(api):
    assert {
        "name": "test_corpus",
        "language": "English",
        "num_datasets": 0,
        "num_documents": 0,
    } in requests.get(f"{api}/get_corpora").json()
