import { getAnswer } from "$lib/server/backend";
import { error } from "@sveltejs/kit";

export async function GET({ url }) {
  const modelName = url.searchParams.get("modelName");
  const question = url.searchParams.get("q");
  const corpusNames = url.searchParams.getAll("corpusName");
  const documentIds = url.searchParams.getAll("documentId");

  if (corpusNames === null || documentIds === null || modelName === null) {
    error(400);
  }

  return getAnswer(modelName, question, corpusNames, documentIds);
}
