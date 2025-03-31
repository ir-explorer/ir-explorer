import { getQueries, getQuery } from "$lib/server/backend";
import type { ListItem, Query } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  let listItems: ListItem<Query>[] = [];
  let query: Query | null = null;

  // if a query ID is specified, we only return that query. otherwise, return all queries
  const queryID = url.searchParams.get("query_id");
  if (queryID !== null) {
    query = await getQuery(params.corpusName, params.datasetName, queryID);
  } else
    for (const query of await getQueries(
      params.corpusName,
      params.datasetName,
    )) {
      const searchParams = new URLSearchParams({ query_id: query.id });
      listItems.push({
        target: `/browse/${params.corpusName}/${params.datasetName}?${searchParams}`,
        item: query,
      });
    }

  return {
    datasetName: params.datasetName,
    queryList: listItems,
    query: query,
    queryID: queryID,
  };
};
