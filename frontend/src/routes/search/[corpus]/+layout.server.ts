import { get_corpora } from "$lib/server/backend";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ params }) => {
  return { corpora: await get_corpora(), selectedCorpus: params.corpus };
};
