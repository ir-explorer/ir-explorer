import type { SelectedOptions } from "./types";

export const selectedOptions = $state({
  queryLanguage: "English",
  corpusNames: [],
  itemsPerPage: 10,
} as SelectedOptions);
