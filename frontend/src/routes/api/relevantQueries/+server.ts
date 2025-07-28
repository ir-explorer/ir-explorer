import { PUBLIC_MAX_ITEMS_PER_PAGE } from "$env/static/public";
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

  const descParsed = desc ? desc === "true" : true;
  const numResultsParsed = numResults ? Number(numResults) : 1;
  const offsetParsed = offset ? Number(offset) : 0;

  if (numResultsParsed > PUBLIC_MAX_ITEMS_PER_PAGE) {
    error(413);
  }

  return json(
    await getRelevantQueries(
      documentId,
      corpusName,
      match,
      orderBy,
      descParsed,
      numResultsParsed,
      offsetParsed,
    ),
  );
}
