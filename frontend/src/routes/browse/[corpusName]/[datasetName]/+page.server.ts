import { getQuery } from "$lib/server/backend";
import type { Query } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  // if a query ID is specified, return that query
  let query: Query | null = null;

  const queryID = url.searchParams.get("query_id");
  if (queryID !== null) {
    query = await getQuery(params.corpusName, params.datasetName, queryID);
  }

  return {
    datasetName: params.datasetName,
    query: query,
  };
};
