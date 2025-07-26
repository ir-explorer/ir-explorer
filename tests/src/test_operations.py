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
        f"{api}/add_documents",
        params={"corpus_name": "c1"},
        json=[
            {"id": "c1-d1", "title": "title 1", "text": "c1 abc def"},
            {"id": "c1-d2", "title": "title 2", "text": "c1 def ghi"},
            {"id": "c1-d3", "title": "title 3", "text": "c1 ghi jkl"},
            {"id": "c1-d4", "title": "title 4", "text": "c1 jkl mno"},
        ],
    )
    requests.post(
        f"{api}/create_dataset",
        json={
            "name": "c1-ds1",
            "corpus_name": "c1",
        },
    )
    requests.post(
        f"{api}/add_queries",
        params={"corpus_name": "c1", "dataset_name": "c1-ds1"},
        json=[
            {"id": "c1-ds1-q1", "text": "c1 ds1 abc def", "description": "desc 1"},
            {"id": "c1-ds1-q2", "text": "c1 ds1 def ghi", "description": "desc 2"},
            {"id": "c1-ds1-q3", "text": "c1 ds1 ghi jkl", "description": "desc 3"},
            {"id": "c1-ds1-q4", "text": "c1 ds1 jkl mno", "description": "desc 4"},
        ],
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
        f"{api}/add_queries",
        params={"corpus_name": "c1", "dataset_name": "c1-ds2"},
        json=[
            {"id": "c1-ds2-q1", "text": "c1 ds2 abc def", "description": "desc 1"},
            {"id": "c1-ds2-q2", "text": "c1 ds2 def ghi", "description": "desc 2"},
            {"id": "c1-ds2-q3", "text": "c1 ds2 ghi jkl", "description": "desc 3"},
            {"id": "c1-ds2-q4", "text": "c1 ds2 jkl mno", "description": "desc 4"},
        ],
    )

    requests.post(
        f"{api}/create_corpus",
        json={"name": "c2", "language": "English"},
    )
    requests.post(
        f"{api}/add_documents",
        params={"corpus_name": "c2"},
        json=[
            {"id": "c2-d1", "title": "title 1", "text": "c2 abc def"},
            {"id": "c2-d2", "title": "title 2", "text": "c2 def ghi"},
        ],
    )
    requests.post(
        f"{api}/create_dataset",
        json={
            "name": "c2-ds1",
            "corpus_name": "c2",
        },
    )
    requests.post(
        f"{api}/add_queries",
        params={"corpus_name": "c2", "dataset_name": "c2-ds1"},
        json=[
            {"id": "c2-ds1-q1", "text": "c2 ds1 abc def", "description": "desc 1"},
            {"id": "c2-ds1-q2", "text": "c2 ds1 def ghi", "description": "desc 2"},
        ],
    )


def test_get_corpora(api):
    assert list_of_dicts_equal(
        requests.get(f"{api}/get_corpora").json(),
        [
            {
                "name": "c1",
                "language": "English",
                "num_datasets": 2,
                "num_documents": 4,
            },
            {
                "name": "c2",
                "language": "English",
                "num_datasets": 1,
                "num_documents": 2,
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
                "num_queries": 4,
            },
            {
                "name": "c1-ds2",
                "corpus_name": "c1",
                "min_relevance": 3,
                "num_queries": 4,
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
                "num_queries": 2,
            },
        ],
    )


def test_get_document(api):
    assert requests.get(
        f"{api}/get_document", params={"corpus_name": "c1", "document_id": "c1-d1"}
    ).json() == {
        "id": "c1-d1",
        "title": "title 1",
        "text": "c1 abc def",
        "corpus_name": "c1",
        "num_relevant_queries": 0,
    }

    # document does not exist, should fail
    assert (
        requests.get(
            f"{api}/get_document", params={"corpus_name": "c1", "document_id": "c1-dx"}
        ).status_code
        == 404
    )


def test_get_documents(api):
    pass


def test_get_query(api):
    assert requests.get(
        f"{api}/get_query",
        params={"corpus_name": "c1", "dataset_name": "c1-ds1", "query_id": "c1-ds1-q1"},
    ).json() == {
        "id": "c1-ds1-q1",
        "text": "c1 ds1 abc def",
        "description": "desc 1",
        "corpus_name": "c1",
        "dataset_name": "c1-ds1",
        "num_relevant_documents": 0,
    }

    # query does not exist, should fail
    assert (
        requests.get(
            f"{api}/get_query",
            params={
                "corpus_name": "c1",
                "dataset_name": "c1-ds1",
                "query_id": "c1-ds1-qx",
            },
        ).status_code
        == 404
    )


def test_get_queries(api):
    pass


def test_get_qrels(api):
    pass


def test_search_documents(api):
    results_all_corpora = requests.get(
        f"{api}/search_documents",
        params={
            "q": "abc def",
            "num_results": 4,
        },
    ).json()

    # first 2 hits should have the same score
    assert (
        results_all_corpora["items"][0]["score"]
        == results_all_corpora["items"][1]["score"]
    )
    assert list_of_dicts_equal(
        results_all_corpora["items"][:2],
        [
            {
                "id": "c1-d1",
                "corpus_name": "c1",
            },
            {
                "id": "c2-d1",
                "corpus_name": "c2",
            },
        ],
        ignore_keys={"score", "snippet"},
    )

    # second 2 hits should have the same score as well
    assert (
        results_all_corpora["items"][2]["score"]
        == results_all_corpora["items"][3]["score"]
    )
    assert list_of_dicts_equal(
        results_all_corpora["items"][2:],
        [
            {
                "id": "c1-d2",
                "corpus_name": "c1",
            },
            {
                "id": "c2-d2",
                "corpus_name": "c2",
            },
        ],
        ignore_keys={"score", "snippet"},
    )

    results_single_corpus = requests.get(
        f"{api}/search_documents",
        params={
            "q": "abc def",
            "corpus_name": ["c1"],
            "num_results": 2,
        },
    ).json()
    assert list_of_dicts_equal(
        results_single_corpus["items"],
        [
            {
                "id": "c1-d1",
                "corpus_name": "c1",
            },
            {
                "id": "c1-d2",
                "corpus_name": "c1",
            },
        ],
        ignore_keys={"score", "snippet"},
    )
