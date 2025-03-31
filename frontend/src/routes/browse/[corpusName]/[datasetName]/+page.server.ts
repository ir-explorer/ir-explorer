import { getQueries } from "$lib/server/backend";
import type { ListItem, Query } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
  let listItems: ListItem<Query>[] = [];
  for (const query of await getQueries(params.corpusName, params.datasetName)) {
    const searchParams = new URLSearchParams({ query_id: query.id });
    listItems.push({
      target: `/browse/${params.corpusName}/${params.datasetName}?${searchParams}`,
      item: query,
    });
  }
  return { datasetName: params.datasetName, queryList: listItems };
};
