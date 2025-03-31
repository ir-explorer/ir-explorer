import { getCorpora } from "$lib/server/backend";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ params }) => {
  return {
    corpora: await getCorpora(),
    selectedCorpusName: params.corpus_name,
  };
};
