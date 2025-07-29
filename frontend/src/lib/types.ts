export interface AvailableOptions {
  queryLanguages: string[];
  corpusNames: string[];
  modelNames: string[];
}
export interface SelectedOptions {
  queryLanguage: string | null;
  corpusNames: string[];
  modelName: string | null;
  itemsPerPage: number;
  snippetLength: number;
}

export interface Corpus {
  name: string;
  language: string;
  numDatasets: number;
  numDocuments: number;
}
export interface Dataset {
  name: string;
  corpusName: string;
  minRelevance: number;
  numQueries: number;
}

export interface Query {
  id: string;
  text: string;
  description: string | null;
  corpusName: string;
  datasetName: string;
  numRelevantDocuments: number;
}
export interface RelevantQuery {
  id: string;
  text: string;
  corpusName: string;
  datasetName: string;
  relevance: number;
}

export interface Document {
  id: string;
  title: string | null;
  text: string;
  corpusName: string;
  numRelevantQueries: number;
}
export interface RelevantDocument {
  id: string;
  text: string;
  corpusName: string;
  relevance: number;
}
export interface DocumentSearchHit {
  score: number;
  id: string;
  snippet: string;
  corpusName: string;
}

export interface Paginated<T> {
  totalNumItems: number;
  offset: number;
  items: T[];
}

export interface OrderByOption {
  name: string;
  option: string;
}
