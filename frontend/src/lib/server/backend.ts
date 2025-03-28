import { BACKEND_HOST, BACKEND_PORT } from "$env/static/private";
import type { Corpus, Dataset, DocumentSearchHit, Query } from "$lib/types";

const BACKEND_REST_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`;

export async function get_corpora(): Promise<Corpus[]> {
  const res = await fetch(`${BACKEND_REST_URL}/get_corpora`);
  return (await res.json()) as Corpus[];
}

export async function get_datasets(corpus: string): Promise<Dataset[]> {
  const params = new URLSearchParams({ corpus_name: corpus });
  const res = await fetch(`${BACKEND_REST_URL}/get_datasets?${params}`);
  return (await res.json()) as Dataset[];
}

export async function get_query(
  corpus: string,
  dataset: string,
  query_id: string,
): Promise<Query> {
  const searchParams = new URLSearchParams({
    corpus_name: corpus,
    dataset_name: dataset,
    query_id: query_id,
  });
  const res = await fetch(`${BACKEND_REST_URL}/get_query?${searchParams}`);
  return (await res.json()) as Query;
}

export async function get_document(
  corpus: string,
  document_id: string,
): Promise<Document> {
  const searchParams = new URLSearchParams({
    corpus_name: corpus,
    document_id: document_id,
  });
  const res = await fetch(
    `${BACKEND_REST_URL}/get_document_id?${searchParams}`,
  );
  return (await res.json()) as Document;
}

export async function get_queries(
  corpus: string,
  dataset: string,
): Promise<Query[]> {
  const searchParams = new URLSearchParams({
    corpus_name: corpus,
    dataset_name: dataset,
  });
  const res = await fetch(`${BACKEND_REST_URL}/get_queries?${searchParams}`);
  return (await res.json()) as Query[];
}

export async function autocomplete_query(
  input: string,
  corpus_name: string,
  dataset_name: string | null,
  num_results: number | null,
): Promise<Query[]> {
  let searchParams = new URLSearchParams({
    corpus_name: corpus_name,
    search: input,
  });
  if (dataset_name !== null) {
    searchParams.append("dataset_name", dataset_name);
  }
  if (num_results !== null) {
    searchParams.append("num_results", num_results.toString());
  }

  const res = await fetch(`${BACKEND_REST_URL}/search_queries?${searchParams}`);
  return (await res.json()) as Query[];
}

export async function search_documents(
  corpus_name: string,
  search: string,
): Promise<DocumentSearchHit[]> {
  const searchParams = new URLSearchParams({
    corpus_name: corpus_name,
    search: search,
  });
  const res = await fetch(
    `${BACKEND_REST_URL}/search_documents?${searchParams}`,
  );
  return (await res.json()) as DocumentSearchHit[];
}
