import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ params, url }) => {
  return {
    corpusName: params.corpusName ?? null,
    datasetName: params.datasetName ?? null,
    documentId: url.searchParams.get("documentId"),
    queryId: url.searchParams.get("queryId"),
  };
};
