import { getQuery } from "$lib/server/backend";
import type { Query } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  let query: Query | null = null;

  // if a query ID is specified, return that query
  const queryId = url.searchParams.get("queryId");
  if (queryId !== null) {
    try {
      query = await getQuery(params.corpusName, params.datasetName, queryId);
    } catch {
      query = null;
    }
  }

  return { datasetName: params.datasetName, query: query };
};
