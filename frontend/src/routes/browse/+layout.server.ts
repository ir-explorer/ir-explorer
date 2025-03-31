import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ params, url }) => {
  return {
    corpusName: params.corpusName ?? null,
    datasetName: params.datasetName ?? null,
    documentID: url.searchParams.get("document_id"),
    queryID: url.searchParams.get("query_id"),
  };
};
