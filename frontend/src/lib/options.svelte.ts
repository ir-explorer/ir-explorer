import type { SelectedOptions } from "./types";

export const selectedOptions = $state({
  queryLanguage: "English",
  corpusNames: [],
} as SelectedOptions);
