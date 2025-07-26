"""Integration tests for adding and removing data."""

import requests


def test_corpora(api):
    num_corpora = len(requests.get(f"{api}/get_corpora").json())

    assert (
        requests.post(
            f"{api}/create_corpus", json={"name": "test_corpus", "language": "English"}
        ).status_code
        == 201
    )
    assert {
        "name": "test_corpus",
        "language": "English",
        "num_datasets": 0,
        "num_documents": 0,
    } in requests.get(f"{api}/get_corpora").json()

    # name exists, should fail
    assert (
        requests.post(
            f"{api}/create_corpus", json={"name": "test_corpus", "language": "English"}
        ).status_code
        == 409
    )

    # invalid language, should fail
    assert (
        requests.post(
            f"{api}/create_corpus",
            json={"name": "test_corpus", "language": "Gibberish"},
        ).status_code
        == 400
    )

    assert (
        requests.delete(
            f"{api}/remove_corpus", params={"corpus_name": "test_corpus"}
        ).status_code
        == 204
    )
    assert len(requests.get(f"{api}/get_corpora").json()) == num_corpora


def test_datasets(api):
    requests.post(
        f"{api}/create_corpus",
        json={"name": "test_corpus_datasets", "language": "English"},
    )

    assert (
        requests.get(
            f"{api}/get_datasets", params={"corpus_name": "test_corpus_datasets"}
        ).json()
        == []
    )

    assert (
        requests.post(
            f"{api}/create_dataset",
            json={
                "name": "test_dataset",
                "corpus_name": "test_corpus_datasets",
                "min_relevance": 3,
            },
        ).status_code
        == 201
    )
    assert requests.get(
        f"{api}/get_datasets", params={"corpus_name": "test_corpus_datasets"}
    ).json() == [
        {
            "name": "test_dataset",
            "corpus_name": "test_corpus_datasets",
            "min_relevance": 3,
            "num_queries": 0,
        }
    ]

    # name exists, should fail
    assert (
        requests.post(
            f"{api}/create_dataset",
            json={
                "name": "test_dataset",
                "corpus_name": "test_corpus_datasets",
                "min_relevance": 1,
            },
        ).status_code
        == 409
    )

    # corpus does not exist, should fail
    assert (
        requests.post(
            f"{api}/create_dataset",
            json={
                "name": "test_dataset",
                "corpus_name": "invalid_corpus",
                "min_relevance": 1,
            },
        ).status_code
        == 409
    )

    assert (
        requests.delete(
            f"{api}/remove_dataset",
            params={
                "corpus_name": "test_corpus_datasets",
                "dataset_name": "test_dataset",
            },
        ).status_code
        == 204
    )
    assert (
        requests.get(
            f"{api}/get_datasets", params={"corpus_name": "test_corpus_datasets"}
        ).json()
        == []
    )


def test_queries_documents(api):
    requests.post(
        f"{api}/create_corpus",
        json={"name": "test_corpus_queries_documents", "language": "English"},
    )
    requests.post(
        f"{api}/create_dataset",
        json={
            "name": "test_dataset",
            "corpus_name": "test_corpus_queries_documents",
            "min_relevance": 1,
        },
    )
    requests.post(
        f"{api}/add_documents",
        params={"corpus_name": "test_corpus_queries_documents"},
        json=[
            {"id": "d1", "title": "title 1", "text": "text 1"},
            {"id": "d2", "title": "title 2", "text": "text 2"},
        ],
    )
    requests.post(
        f"{api}/add_queries",
        params={
            "corpus_name": "test_corpus_queries_documents",
            "dataset_name": "test_dataset",
        },
        json=[
            {"id": "q1", "text": "text 1", "description": "description 1"},
            {"id": "q2", "text": "text 2", "description": "description 2"},
        ],
    )
    requests.post(
        f"{api}/add_qrels",
        params={
            "corpus_name": "test_corpus_queries_documents",
            "dataset_name": "test_dataset",
        },
        json=[
            {"query_id": "q1", "document_id": "d1", "relevance": 1},
            {"query_id": "q2", "document_id": "d1", "relevance": 3},
        ],
    )
    assert (
        requests.get(
            f"{api}/get_documents",
            params={"corpus_name": "test_corpus_queries_documents"},
        ).json()["total_num_items"]
        == 2
    )
    assert (
        requests.get(
            f"{api}/get_queries",
            params={
                "corpus_name": "test_corpus_queries_documents",
                "dataset_name": "test_dataset",
            },
        ).json()["total_num_items"]
        == 2
    )
    assert (
        requests.get(
            f"{api}/get_qrels",
            params={
                "corpus_name": "test_corpus_queries_documents",
                "dataset_name": "test_dataset",
            },
        ).json()["total_num_items"]
        == 2
    )

    # dataset exists, should fail
    assert (
        requests.delete(
            f"{api}/remove_corpus",
            params={"corpus_name": "test_corpus_queries_documents"},
        ).status_code
        == 409
    )

    requests.delete(
        f"{api}/remove_dataset",
        params={
            "corpus_name": "test_corpus_queries_documents",
            "dataset_name": "test_dataset",
        },
    )
    assert (
        requests.delete(
            f"{api}/remove_corpus",
            params={"corpus_name": "test_corpus_queries_documents"},
        ).status_code
        == 204
    )
    assert (
        requests.get(
            f"{api}/get_documents",
            params={"corpus_name": "test_corpus_queries_documents"},
        ).json()["total_num_items"]
        == 0
    )
    assert (
        requests.get(
            f"{api}/get_queries",
            params={
                "corpus_name": "test_corpus_queries_documents",
                "dataset_name": "test_dataset",
            },
        ).json()["total_num_items"]
        == 0
    )
    assert (
        requests.get(
            f"{api}/get_qrels",
            params={
                "corpus_name": "test_corpus_queries_documents",
                "dataset_name": "test_dataset",
            },
        ).json()["total_num_items"]
        == 0
    )
