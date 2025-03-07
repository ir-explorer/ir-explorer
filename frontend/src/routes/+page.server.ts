import { get_corpora } from "$lib/server/backend";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
  return { corpora: await get_corpora() };
};
