import { getSearchOptions } from "$lib/server/backend";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
  return { searchOptions: await getSearchOptions() };
};
