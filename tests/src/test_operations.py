"""Integration tests for backend operations."""

import pytest
import requests

from util import list_of_dicts_equal


@pytest.fixture(scope="module", autouse=True)
def setup_data(api):
    requests.post(
        f"{api}/create_corpus",
        json={"name": "c1", "language": "English"},
    )
    requests.post(
        f"{api}/create_dataset",
        json={
            "name": "c1-ds1",
            "corpus_name": "c1",
        },
    )
    requests.post(
        f"{api}/create_dataset",
        json={
            "name": "c1-ds2",
            "corpus_name": "c1",
            "min_relevance": 3,
        },
    )

    requests.post(
        f"{api}/create_corpus",
        json={"name": "c2", "language": "English"},
    )
    requests.post(
        f"{api}/create_dataset",
        json={
            "name": "c2-ds1",
            "corpus_name": "c2",
        },
    )


def test_get_corpora(api):
    assert list_of_dicts_equal(
        requests.get(f"{api}/get_corpora").json(),
        [
            {
                "name": "c1",
                "language": "English",
                "num_datasets": 2,
                "num_documents": 0,
            },
            {
                "name": "c2",
                "language": "English",
                "num_datasets": 1,
                "num_documents": 0,
            },
        ],
    )


def test_get_datasets(api):
    assert list_of_dicts_equal(
        requests.get(f"{api}/get_datasets", params={"corpus_name": "c1"}).json(),
        [
            {
                "name": "c1-ds1",
                "corpus_name": "c1",
                "min_relevance": 1,
                "num_queries": 0,
            },
            {
                "name": "c1-ds2",
                "corpus_name": "c1",
                "min_relevance": 3,
                "num_queries": 0,
            },
        ],
    )

    assert list_of_dicts_equal(
        requests.get(f"{api}/get_datasets", params={"corpus_name": "c2"}).json(),
        [
            {
                "name": "c2-ds1",
                "corpus_name": "c2",
                "min_relevance": 1,
                "num_queries": 0,
            },
        ],
    )
