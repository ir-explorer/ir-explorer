import { getDocumentSummary } from "$lib/server/backend";
import { error } from "@sveltejs/kit";

export async function GET({ url }) {
  const corpusName = url.searchParams.get("corpusName");
  const documentId = url.searchParams.get("documentId");
  const modelName = url.searchParams.get("modelName");

  if (corpusName === null || documentId === null || modelName === null) {
    error(400);
  }

  return getDocumentSummary(corpusName, documentId, modelName);
}
