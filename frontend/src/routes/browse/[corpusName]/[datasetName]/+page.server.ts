import { getQuery } from "$lib/server/backend";
import type { Query } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  // if a query ID is specified, return that query
  let query: Query | null = null;

  const queryId = url.searchParams.get("queryId");
  if (queryId !== null) {
    query = await getQuery(params.corpusName, params.datasetName, queryId);
  }

  return { datasetName: params.datasetName, query: query };
};
