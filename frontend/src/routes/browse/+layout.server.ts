import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ params, url }) => {
  return {
    corpus: params.corpus ?? null,
    dataset: params.dataset ?? null,
    doc_id: url.searchParams.get("doc"),
    q_id: url.searchParams.get("query"),
  };
};
