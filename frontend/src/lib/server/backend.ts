import { BACKEND_HOST, BACKEND_PORT } from "$env/static/private";
import type {
  Corpus,
  Dataset,
  Document,
  DocumentSearchHit,
  Paginated,
  Query,
} from "$lib/types";

const BACKEND_REST_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`;

export async function getCorpora(): Promise<Corpus[]> {
  const res = await fetch(`${BACKEND_REST_URL}/get_corpora`);
  return (await res.json()) as Corpus[];
}

export async function getDatasets(corpusName: string): Promise<Dataset[]> {
  const params = new URLSearchParams({ corpus_name: corpusName });
  const res = await fetch(`${BACKEND_REST_URL}/get_datasets?${params}`);
  return (await res.json()) as Dataset[];
}

export async function getQuery(
  corpusName: string,
  datasetName: string,
  queryID: string,
): Promise<Query> {
  const searchParams = new URLSearchParams({
    corpus_name: corpusName,
    dataset_name: datasetName,
    query_id: queryID,
  });
  const res = await fetch(`${BACKEND_REST_URL}/get_query?${searchParams}`);
  return (await res.json()) as Query;
}

export async function getDocument(
  corpusName: string,
  documentID: string,
): Promise<Document> {
  const searchParams = new URLSearchParams({
    corpus_name: corpusName,
    document_id: documentID,
  });
  const res = await fetch(`${BACKEND_REST_URL}/get_document?${searchParams}`);
  return (await res.json()) as Document;
}

export async function getQueries(
  corpusName: string,
  datasetName: string,
): Promise<Query[]> {
  const searchParams = new URLSearchParams({
    corpus_name: corpusName,
    dataset_name: datasetName,
  });
  const res = await fetch(`${BACKEND_REST_URL}/get_queries?${searchParams}`);
  return (await res.json()) as Query[];
}

export async function autocompleteQuery(
  input: string,
  corpusName: string,
  datasetName: string | null,
  numResults: number | null,
): Promise<Query[]> {
  let searchParams = new URLSearchParams({
    corpus_name: corpusName,
    search: input,
  });
  if (datasetName !== null) {
    searchParams.append("dataset_name", datasetName);
  }
  if (numResults !== null) {
    searchParams.append("num_results", numResults.toString());
  }

  const res = await fetch(`${BACKEND_REST_URL}/search_queries?${searchParams}`);
  return (await res.json()) as Query[];
}

export async function searchDocuments(
  corpusName: string,
  search: string,
  numResults: number,
  page: number,
): Promise<Paginated<DocumentSearchHit>> {
  const offset = (page - 1) * numResults;
  const searchParams = new URLSearchParams({
    corpus_name: corpusName,
    search: search,
    num_results: numResults.toString(),
    offset: offset.toString(),
  });
  const res = await fetch(
    `${BACKEND_REST_URL}/search_documents?${searchParams}`,
  );
  return (await res.json()) as Paginated<DocumentSearchHit>;
}
