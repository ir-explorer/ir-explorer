import { getDatasets, getDocument } from "$lib/server/backend";
import type { Dataset, Document, ListItem } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  let listItems: ListItem<Dataset>[] = [];
  let document: Document | null = null;

  // if a document ID is specified, we only return that query. otherwise, return all documents
  const documentID = url.searchParams.get("document_id");
  if (documentID !== null) {
    document = await getDocument(params.corpusName, documentID);
  } else
    for (const dataset of await getDatasets(params.corpusName)) {
      listItems.push({
        target: "/browse/" + params.corpusName + "/" + dataset.name,
        item: dataset,
      });
    }

  return { datasetList: listItems, document: document, documentID: documentID };
};
