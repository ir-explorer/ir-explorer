import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ params, url }) => {
  return {
    corpus_name: params.corpus_name ?? null,
    dataset_name: params.dataset_name ?? null,
    document_id: url.searchParams.get("document_id"),
    query_id: url.searchParams.get("query_id"),
  };
};
