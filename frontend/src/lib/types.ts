export interface Corpus {
  name: string;
  language: string;
}
export interface Dataset {
  name: string;
  corpus_name: string;
  min_relevance: number;
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
  text: string;
  title: string | null;
  corpus_name: string;
}
export interface DocumentSearchHit extends Document {
  score: number;
}
