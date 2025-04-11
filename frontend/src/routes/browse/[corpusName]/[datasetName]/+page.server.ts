import { getQueries, getQuery } from "$lib/server/backend";
import type { Query } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  // if a query ID is specified, return only that query
  let query: Query | null = null;
  let queryList: Query[] | null = null;

  const queryID = url.searchParams.get("query_id");
  if (queryID !== null) {
    query = await getQuery(params.corpusName, params.datasetName, queryID);
  } else {
    queryList = (await getQueries(params.corpusName, params.datasetName)).items;
  }

  return {
    datasetName: params.datasetName,
    queryList: queryList,
    query: query,
    queryID: queryID,
  };
};
