import { BACKEND_HOST, BACKEND_PORT } from "$env/static/private";
import type { Corpus, Dataset, DocumentSearchHit, Query } from "$lib/types";

const BACKEND_REST_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`;

export async function get_corpora(): Promise<Corpus[]> {
  const res = await fetch(BACKEND_REST_URL + "/get_corpora");
  return (await res.json()) as Corpus[];
}

export async function get_datasets(corpus: string): Promise<Dataset[]> {
  const res = await fetch(
    BACKEND_REST_URL +
      "/get_datasets?" +
      new URLSearchParams({ corpus_name: corpus })
  );
  return (await res.json()) as Dataset[];
}

export async function autocomplete_query(
  input: string,
  corpus_name: string,
  dataset_name: string | null,
  num_results: number | null
): Promise<Query[]> {
  var params = new URLSearchParams({
    corpus_name: corpus_name,
    search: input,
  });
  if (dataset_name !== null) {
    params.append("dataset_name", dataset_name);
  }
  if (num_results !== null) {
    params.append("num_results", num_results.toString());
  }

  const res = await fetch(BACKEND_REST_URL + "/search_queries?" + params);
  return (await res.json()) as Query[];
}

export async function search_documents(
  corpus_name: string,
  search: string
): Promise<DocumentSearchHit[]> {
  const res = await fetch(
    BACKEND_REST_URL +
      "/search_documents?" +
      new URLSearchParams({
        corpus_name: corpus_name,
        search: search,
      })
  );
  return (await res.json()) as DocumentSearchHit[];
}
