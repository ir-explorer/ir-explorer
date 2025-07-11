import type { SelectedOptions } from "./types";

export const selectedOptions = $state({
  queryLanguage: "English",
  corpusNames: [],
  itemsPerPage: 10,
  snippetLength: 300,
} as SelectedOptions);
