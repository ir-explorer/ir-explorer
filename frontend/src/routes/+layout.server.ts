import { getAvailableOptions } from "$lib/server/backend";
import type { SelectedOptions } from "$lib/types";
import type { LayoutServerLoad } from "./$types";

const selectedOptions = {
  queryLanguage: "English",
  corpusNames: [],
} as SelectedOptions;

export const load: LayoutServerLoad = async () => {
  return {
    availableOptions: await getAvailableOptions(),
    selectedOptions: selectedOptions,
  };
};
