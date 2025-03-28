import { get_datasets, get_document } from "$lib/server/backend";
import type { Dataset, Document, ListItem } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  let listItems: ListItem<Dataset>[] = [];
  for (const dataset of await get_datasets(params.corpus_name)) {
    listItems.push({
      target: "/browse/" + params.corpus_name + "/" + dataset.name,
      item: dataset,
    });
  }

  let document: Document | null = null;
  const documentID = url.searchParams.get("document_id");
  if (documentID !== null) {
    document = await get_document(params.corpus_name, documentID);
  }

  return { datasetList: listItems, document: document };
};
