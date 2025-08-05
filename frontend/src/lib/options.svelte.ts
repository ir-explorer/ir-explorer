import type { SelectedOptions } from "./types";

export const selectedOptions = $state({
  queryLanguage: null,
  corpusNames: [],
  modelName: null,
  itemsPerPage: 10,
  snippetLength: 300,
  numRagDocuments: 2,
} as SelectedOptions);
