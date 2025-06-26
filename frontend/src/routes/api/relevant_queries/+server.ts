import { getRelevantQueries } from "$lib/server/backend";
import { error, json } from "@sveltejs/kit";

export async function GET({ url }) {
  const documentID = url.searchParams.get("document_id");
  const corpusName = url.searchParams.get("corpus_name");
  const match = url.searchParams.get("match");
  const orderBy = url.searchParams.get("order_by");
  const desc = url.searchParams.get("desc");
  const numResults = url.searchParams.get("num_results");
  const offset = url.searchParams.get("offset");

  if (documentID === null || corpusName === null) {
    error(400);
  }

  return json(
    await getRelevantQueries(
      documentID,
      corpusName,
      match,
      orderBy,
      desc ? desc === "true" : true,
      numResults ? Number(numResults) : 10,
      offset ? Number(offset) : 0,
    ),
  );
}
