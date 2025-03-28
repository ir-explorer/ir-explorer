import { get_datasets } from "$lib/server/backend";

import type { Dataset, ListItem } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
  let listItems: ListItem<Dataset>[] = [];
  for (const dataset of await get_datasets(params.corpus_name)) {
    listItems.push({
      target: "/browse/" + params.corpus_name + "/" + dataset.name,
      item: dataset,
    });
  }
  return { datasetList: listItems };
};
