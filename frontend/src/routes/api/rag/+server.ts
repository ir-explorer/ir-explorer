import { PUBLIC_MAX_RAG_DOCUMENTS } from "$env/static/public";
import { getAnswer } from "$lib/server/backend";
import { error } from "@sveltejs/kit";

export async function GET({ url }) {
  const modelName = url.searchParams.get("modelName");
  const question = url.searchParams.get("q");
  const corpusNames: string[] = url.searchParams.getAll("corpusName");
  const documentIds: string[] = url.searchParams.getAll("documentId");

  if (corpusNames === null || documentIds === null || modelName === null) {
    error(400);
  }
  if (
    corpusNames.length != documentIds.length ||
    documentIds.length == 0 ||
    documentIds.length > Number(PUBLIC_MAX_RAG_DOCUMENTS)
  ) {
    error(400);
  }

  return getAnswer(modelName, question, corpusNames, documentIds);
}
