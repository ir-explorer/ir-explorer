export interface Corpus {
  name: string;
  language: string;
  num_datasets: number;
  num_documents_estimate: number;
}
export interface Dataset {
  name: string;
  corpus_name: string;
  min_relevance: number;
  num_queries_estimate: number;
}
export interface Query {
  id: string;
  text: string;
  description: string | null;
  corpus_name: string;
  dataset_name: string;
}
export interface Document {
  id: string;
  title: string | null;
  text: string;
  corpus_name: string;
}
export interface DocumentSearchHit {
  score: number;
  id: string;
  title: string | null;
  snippet: string;
  corpus_name: string;
}

export interface Paginated<T> {
  total_num_items: number;
  offset: number;
  items: T[];
}

export interface ListItem<T> {
  target: string;
  item: T;
}
