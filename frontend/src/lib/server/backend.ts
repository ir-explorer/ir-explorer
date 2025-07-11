import { BACKEND_HOST, BACKEND_PORT } from "$env/static/private";
import type {
  AvailableOptions,
  Corpus,
  Dataset,
  Document,
  DocumentSearchHit,
  Paginated,
  Query,
  RelevantDocument,
  RelevantQuery,
} from "$lib/types";

const BACKEND_REST_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`;

/**
 * Return a list of natural languages supported by the backend.
 *
 * @returns The supported languages.
 */
export async function getAvailableLanguages(): Promise<string[]> {
  const res = await fetch(`${BACKEND_REST_URL}/get_available_languages`);
  return (await res.json()) as string[];
}

/**
 * Return available options to be set.
 *
 * Includes backend (search) options and frontend display options.
 *
 * @returns All available options.
 */
export async function getAvailableOptions(): Promise<AvailableOptions> {
  const res = await fetch(`${BACKEND_REST_URL}/get_search_options`);
  const resJson = await res.json();

  return {
    queryLanguages: resJson["query_languages"],
    corpusNames: resJson["corpus_names"],
  } as AvailableOptions;
}

/**
 * Return a list of available corpora.
 *
 * @returns The corpora.
 */
export async function getCorpora(): Promise<Corpus[]> {
  const res = await fetch(`${BACKEND_REST_URL}/get_corpora`);
  const resJson = await res.json();

  let corpora: Corpus[] = [];
  for (const item of resJson) {
    corpora.push({
      name: item["name"],
      language: item["language"],
      numDatasets: item["num_datasets"],
      numDocuments: item["num_documents"],
    } as Corpus);
  }
  return corpora;
}

/**
 * Return a list of available datasets for a corpus.
 *
 * @param corpusName - The name of the corpus.
 *
 * @returns The datasets corresponding to the corpus.
 */
export async function getDatasets(corpusName: string): Promise<Dataset[]> {
  const params = new URLSearchParams({ corpus_name: corpusName });
  const res = await fetch(`${BACKEND_REST_URL}/get_datasets?${params}`);
  const resJson = await res.json();

  let datasets: Dataset[] = [];
  for (const item of resJson) {
    datasets.push({
      name: item["name"],
      corpusName: item["corpus_name"],
      minRelevance: item["min_relevance"],
      numQueries: item["num_queries"],
    } as Dataset);
  }
  return datasets;
}

/**
 * Return a single query.
 *
 * @param corpusName - The name of the corpus.
 * @param datasetName - The name of the dataset.
 * @param queryId - The ID of the query.
 *
 * @returns The query.
 */
export async function getQuery(
  corpusName: string,
  datasetName: string,
  queryId: string,
): Promise<Query> {
  const searchParams = new URLSearchParams({
    corpus_name: corpusName,
    dataset_name: datasetName,
    query_id: queryId,
  });
  const res = await fetch(`${BACKEND_REST_URL}/get_query?${searchParams}`);
  const resJson = await res.json();

  return {
    id: resJson["id"],
    text: resJson["text"],
    description: resJson["description"],
    corpusName: resJson["corpus_name"],
    datasetName: resJson["dataset_name"],
    numRelevantDocuments: resJson["num_relevant_documents"],
  } as Query;
}

/**
 * Return a list of queries according to certain criteria.
 *
 * @param corpusName - The name of the corpus.
 * @param datasetName - The name of the dataset.
 * @param match - Return only queries matching this string.
 * @param orderBy - In what way to order the results.
 * @param desc - Whether to order in a descending fashion.
 * @param numResults - How many results to return.
 * @param offset - How many results to skip.
 *
 * @returns The list of queries.
 */
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
  const resJson = await res.json();

  let queries: Query[] = [];
  for (const item of resJson["items"]) {
    queries.push({
      id: item["id"],
      text: item["text"],
      description: item["description"],
      corpusName: item["corpus_name"],
      datasetName: item["dataset_name"],
      numRelevantDocuments: item["num_relevant_documents"],
    } as Query);
  }
  return {
    totalNumItems: resJson["total_num_items"],
    offset: resJson["offset"],
    items: queries,
  } as Paginated<Query>;
}

/**
 * Return a single document.
 *
 * @param corpusName - The name of the corpus.
 * @param documentId - The ID of the document.
 *
 * @returns The document.
 */
export async function getDocument(
  corpusName: string,
  documentId: string,
): Promise<Document> {
  const searchParams = new URLSearchParams({
    corpus_name: corpusName,
    document_id: documentId,
  });
  const res = await fetch(`${BACKEND_REST_URL}/get_document?${searchParams}`);
  const resJson = await res.json();

  return {
    id: resJson["id"],
    title: resJson["title"],
    text: resJson["text"],
    corpusName: resJson["corpus_name"],
    numRelevantQueries: resJson["num_relevant_queries"],
  } as Document;
}

/**
 * Return a list of documents according to certain criteria.
 *
 * @param corpusName - The name of the corpus.
 * @param match - Return only documents matching this string.
 * @param orderBy - In what way to order the results.
 * @param desc - Whether to order in a descending fashion.
 * @param numResults - How many results to return.
 * @param offset - How many results to skip.
 *
 * @returns The list of documents.
 */
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
    num_results: numResults.toString(),
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
  const resJson = await res.json();

  let documents: Document[] = [];
  for (const item of resJson["items"]) {
    documents.push({
      id: item["id"],
      title: item["title"],
      text: item["text"],
      corpusName: item["corpus_name"],
      numRelevantQueries: item["num_relevant_queries"],
    } as Document);
  }
  return {
    totalNumItems: resJson["total_num_items"],
    offset: resJson["offset"],
    items: documents,
  } as Paginated<Document>;
}

/**
 * Search documents in one or more corpora.
 *
 * Results are ordered by scores (descending).
 *
 * @param q - The search query.
 * @param language - The search query language.
 * @param numResults - How many results to return.
 * @param page - Return results for this search page.
 * @param corpusNames - Search only in these corpora.
 *
 * @returns The list of hits.
 */
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
  const resJson = await res.json();

  let hits: DocumentSearchHit[] = [];
  for (const item of resJson["items"]) {
    hits.push({
      score: item["score"],
      id: item["id"],
      snippet: item["snippet"],
      corpusName: item["corpus_name"],
    } as DocumentSearchHit);
  }
  return {
    totalNumItems: resJson["total_num_items"],
    offset: resJson["offset"],
    items: hits,
  } as Paginated<DocumentSearchHit>;
}

/**
 * Return a list of relevant queries for a document.
 *
 * @param documentId - The ID of the document.
 * @param corpusName - The name of the corpus.
 * @param match - Return only queries matching this string.
 * @param orderBy - In what way to order the results.
 * @param desc - Whether to order in a descending fashion.
 * @param numResults - How many results to return.
 * @param offset - How many results to skip.
 *
 * @returns The list of queries.
 */
export async function getRelevantQueries(
  documentId: string,
  corpusName: string,
  match: string | null = null,
  orderBy: string | null = null,
  desc: boolean = true,
  numResults: number,
  offset: number,
): Promise<Paginated<RelevantQuery>> {
  const searchParams = new URLSearchParams({
    document_id: documentId,
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

  const res = await fetch(`${BACKEND_REST_URL}/get_qrels?${searchParams}`);
  const resJson = await res.json();
  let queries: RelevantQuery[] = [];
  for (const item of resJson["items"]) {
    queries.push({
      id: item["query_info"]["id"],
      text: item["query_info"]["text"],
      corpusName: item["corpus_name"],
      datasetName: item["dataset_name"],
      relevance: item["relevance"],
    } as RelevantQuery);
  }
  return {
    totalNumItems: resJson["total_num_items"],
    offset: resJson["offset"],
    items: queries,
  } as Paginated<RelevantQuery>;
}

/**
 * Return a list of relevant documents for a query.
 *
 * @param queryId - The ID of the query.
 * @param datasetName - The name of the dataset.
 * @param corpusName - The name of the corpus.
 * @param match - Return only documents matching this string.
 * @param orderBy - In what way to order the results.
 * @param desc - Whether to order in a descending fashion.
 * @param numResults - How many results to return.
 * @param offset - How many results to skip.
 *
 * @returns The list of documents.
 */
export async function getRelevantDocuments(
  queryId: string,
  datasetName: string,
  corpusName: string,
  match: string | null = null,
  orderBy: string | null = null,
  desc: boolean = true,
  numResults: number,
  offset: number,
): Promise<Paginated<RelevantDocument>> {
  const searchParams = new URLSearchParams({
    query_id: queryId,
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

  const res = await fetch(`${BACKEND_REST_URL}/get_qrels?${searchParams}`);
  const resJson = await res.json();
  let documents: RelevantDocument[] = [];
  for (const item of resJson["items"]) {
    documents.push({
      id: item["document_info"]["id"],
      text: item["document_info"]["text"],
      corpusName: item["corpus_name"],
      relevance: item["relevance"],
    } as RelevantDocument);
  }
  return {
    totalNumItems: resJson["total_num_items"],
    offset: resJson["offset"],
    items: documents,
  } as Paginated<RelevantDocument>;
}
