import { BACKEND_HOST, BACKEND_PORT } from "$env/static/private";
import type {
  Corpus,
  Dataset,
  Document,
  DocumentSearchHit,
  Paginated,
  Query,
  RelevantDocument,
  RelevantQuery,
  SearchOptions,
} from "$lib/types";

const BACKEND_REST_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`;

export async function getAvailableLanguages(): Promise<string[]> {
  const res = await fetch(`${BACKEND_REST_URL}/get_available_languages`);
  return (await res.json()) as string[];
}

export async function getSearchOptions(): Promise<SearchOptions> {
  const res = await fetch(`${BACKEND_REST_URL}/get_search_options`);
  const res_json = await res.json();
  return {
    queryLanguages: res_json["query_languages"],
    corpusNames: res_json["corpus_names"],
  } as SearchOptions;
}

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

export async function getQueries(
  corpusName: string,
  datasetName: string | null = null,
  match: string | null = null,
  orderBy: string | null = null,
  desc: boolean = true,
  numResults: number,
  offset: number = 0,
): Promise<Paginated<Query>> {
  let searchParams = new URLSearchParams({
    corpus_name: corpusName,
    num_results: numResults.toString(),
    offset: offset.toString(),
    order_by_desc: desc.toString(),
  });
  if (datasetName !== null) {
    searchParams.append("dataset_name", datasetName);
  }
  if (match !== null) {
    searchParams.append("match", match);
  }
  if (orderBy !== null) {
    searchParams.append("order_by", orderBy);
  }

  const res = await fetch(`${BACKEND_REST_URL}/get_queries?${searchParams}`);
  return (await res.json()) as Paginated<Query>;
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

export async function getDocuments(
  corpusName: string,
  match: string | null = null,
  orderBy: string | null = null,
  desc: boolean = true,
  numResults: number,
  offset: number,
): Promise<Paginated<Document>> {
  let searchParams = new URLSearchParams({
    corpus_name: corpusName,
    numResults: numResults.toString(),
    offset: offset.toString(),
    order_by_desc: desc.toString(),
  });
  if (match !== null) {
    searchParams.append("match", match);
  }
  if (orderBy !== null) {
    searchParams.append("order_by", orderBy);
  }

  const res = await fetch(`${BACKEND_REST_URL}/get_documents?${searchParams}`);
  return (await res.json()) as Paginated<Document>;
}

export async function searchDocuments(
  q: string,
  language: string | null,
  numResults: number,
  page: number,
  corpusNames: string[] | null,
): Promise<Paginated<DocumentSearchHit>> {
  const offset = (page - 1) * numResults;
  const searchParams = new URLSearchParams({
    q: q,
    num_results: numResults.toString(),
    offset: offset.toString(),
  });
  if (language != null) {
    searchParams.append("language", language);
  }
  if (corpusNames !== null) {
    for (const corpusName of corpusNames) {
      searchParams.append("corpus_name", corpusName);
    }
  }

  const res = await fetch(
    `${BACKEND_REST_URL}/search_documents?${searchParams}`,
  );
  return (await res.json()) as Paginated<DocumentSearchHit>;
}

export async function getRelevantDocuments(
  queryID: string,
  datasetName: string,
  corpusName: string,
  match: string | null = null,
  orderBy: string | null = null,
  desc: boolean = true,
  numResults: number,
  offset: number,
): Promise<Paginated<RelevantDocument>> {
  const searchParams = new URLSearchParams({
    query_id: queryID,
    dataset_name: datasetName,
    corpus_name: corpusName,
    num_results: numResults.toString(),
    offset: offset.toString(),
    order_by_desc: desc.toString(),
  });
  if (match !== null) {
    searchParams.append("match_document", match);
  }
  if (orderBy !== null) {
    searchParams.append("order_by", orderBy);
  }

  return new Promise<Paginated<RelevantDocument>>(async (resolve) => {
    const res = await fetch(`${BACKEND_REST_URL}/get_qrels?${searchParams}`);
    const res_json = await res.json();
    let documents: RelevantDocument[] = [];
    for (const item of res_json["items"]) {
      documents.push({
        id: item["document_info"]["id"],
        snippet: item["document_info"]["text"],
        corpus_name: item["corpus_name"],
        relevance: item["relevance"],
      } as RelevantDocument);
    }
    resolve({
      total_num_items: res_json["total_num_items"],
      offset: res_json["offset"],
      items: documents,
    } as Paginated<RelevantDocument>);
  });
}

export async function getRelevantQueries(
  documentID: string,
  corpusName: string,
  match: string | null = null,
  orderBy: string | null = null,
  desc: boolean = true,
  numResults: number,
  offset: number,
): Promise<Paginated<RelevantQuery>> {
  const searchParams = new URLSearchParams({
    document_id: documentID,
    corpus_name: corpusName,
    num_results: numResults.toString(),
    offset: offset.toString(),
    order_by_desc: desc.toString(),
  });
  if (match !== null) {
    searchParams.append("match_query", match);
  }
  if (orderBy !== null) {
    searchParams.append("order_by", orderBy);
  }

  return new Promise<Paginated<RelevantQuery>>(async (resolve) => {
    const res = await fetch(`${BACKEND_REST_URL}/get_qrels?${searchParams}`);
    const res_json = await res.json();
    let queries: RelevantQuery[] = [];
    for (const item of res_json["items"]) {
      queries.push({
        id: item["query_info"]["id"],
        snippet: item["query_info"]["text"],
        corpus_name: item["corpus_name"],
        dataset_name: item["dataset_name"],
        relevance: item["relevance"],
      } as RelevantQuery);
    }
    resolve({
      total_num_items: res_json["total_num_items"],
      offset: res_json["offset"],
      items: queries,
    } as Paginated<RelevantQuery>);
  });
}
