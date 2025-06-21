export interface SearchOptions {
  query_languages: string[];
  corpus_names: string[];
}
export interface SearchOptionsInit {
  query_language: string | null;
  selected_corpus_names: string[];
}

export interface Corpus {
  name: string;
  language: string;
  num_datasets: number;
  num_documents: number;
}
export interface Dataset {
  name: string;
  corpus_name: string;
  min_relevance: number;
  num_queries: number;
}

export interface Query {
  id: string;
  text: string;
  description: string | null;
  corpus_name: string;
  dataset_name: string;
  num_relevant_documents: number;
}
export interface RelevantQuery {
  id: string;
  snippet: string;
  corpus_name: string;
  dataset_name: string;
  relevance: number;
}

export interface Document {
  id: string;
  title: string | null;
  text: string;
  corpus_name: string;
  num_relevant_queries: number;
}
export interface RelevantDocument {
  id: string;
  snippet: string;
  corpus_name: string;
  relevance: number;
}
export interface DocumentSearchHit {
  score: number;
  id: string;
  snippet: string;
  corpus_name: string;
}

export interface Paginated<T> {
  total_num_items: number;
  offset: number;
  items: T[];
}
