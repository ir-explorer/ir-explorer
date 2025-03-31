import { getDatasets, getDocument } from "$lib/server/backend";
import type { Dataset, Document, ListItem } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  let listItems: ListItem<Dataset>[] = [];
  for (const dataset of await getDatasets(params.corpusName)) {
    listItems.push({
      target: "/browse/" + params.corpusName + "/" + dataset.name,
      item: dataset,
    });
  }

  let document: Document | null = null;
  const documentID = url.searchParams.get("document_id");
  if (documentID !== null) {
    document = await getDocument(params.corpusName, documentID);
  }

  return { datasetList: listItems, document: document };
};
