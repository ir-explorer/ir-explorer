import { getSearchOptions } from "$lib/server/backend";
import type { SearchSettings } from "$lib/types";
import type { LayoutServerLoad } from "./$types";

const searchSettings = {
  queryLanguage: "English",
  corpusNames: [],
} as SearchSettings;

export const load: LayoutServerLoad = async () => {
  return {
    searchOptions: await getSearchOptions(),
    searchSettings: searchSettings,
  };
};
