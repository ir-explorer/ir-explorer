import { getCorpora } from "$lib/server/backend";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
  return { corpora: await getCorpora() };
};
