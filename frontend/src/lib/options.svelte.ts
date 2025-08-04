import type { SelectedOptions } from "./types";

export const selectedOptions = $state({
  queryLanguage: null,
  corpusNames: [],
  modelName: null,
  itemsPerPage: 10,
  snippetLength: 300,
  ragDocuments: 1,
} as SelectedOptions);
