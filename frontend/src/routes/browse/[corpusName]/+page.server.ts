import { getDatasets, getDocument } from "$lib/server/backend";
import type { Dataset, Document } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  // if a document ID is specified, return only that document
  let document: Document | null = null;
  let datasetList: Dataset[] | null = null;

  // if a document ID is specified, return that document. otherwise, return a list of datasets
  const documentID = url.searchParams.get("document_id");
  if (documentID !== null) {
    document = await getDocument(params.corpusName, documentID);
  } else {
    datasetList = await getDatasets(params.corpusName);
  }

  return {
    datasetList: datasetList,
    document: document,
    documentID: documentID,
  };
};
