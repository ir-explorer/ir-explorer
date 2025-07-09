import { getRelevantQueries } from "$lib/server/backend";
import { error, json } from "@sveltejs/kit";

export async function GET({ url }) {
  const documentId = url.searchParams.get("documentId");
  const corpusName = url.searchParams.get("corpusName");
  const match = url.searchParams.get("match");
  const orderBy = url.searchParams.get("orderBy");
  const desc = url.searchParams.get("desc");
  const numResults = url.searchParams.get("numResults");
  const offset = url.searchParams.get("offset");

  if (documentId === null || corpusName === null) {
    error(400);
  }

  return json(
    await getRelevantQueries(
      documentId,
      corpusName,
      match,
      orderBy,
      desc ? desc === "true" : true,
      numResults ? Number(numResults) : 10,
      offset ? Number(offset) : 0,
    ),
  );
}
