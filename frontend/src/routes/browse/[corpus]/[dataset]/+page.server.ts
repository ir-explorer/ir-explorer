import { get_queries } from "$lib/server/backend";
import type { ListItem, Query } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
  let listItems: ListItem<Query>[] = [];
  for (const query of await get_queries(params.corpus, params.dataset)) {
    const searchParams = new URLSearchParams({ query: query.id });
    listItems.push({
      target: `/browse/${params.corpus}/${params.dataset}?${searchParams}`,
      item: query,
    });
  }
  return { dataset_name: params.dataset, queryList: listItems };
};
