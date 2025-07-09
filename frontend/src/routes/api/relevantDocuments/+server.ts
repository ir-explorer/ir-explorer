import { getRelevantDocuments } from "$lib/server/backend";
import { error, json } from "@sveltejs/kit";

export async function GET({ url }) {
  const queryId = url.searchParams.get("queryId");
  const datasetName = url.searchParams.get("datasetName");
  const corpusName = url.searchParams.get("corpusName");
  const match = url.searchParams.get("match");
  const orderBy = url.searchParams.get("orderBy");
  const desc = url.searchParams.get("desc");
  const numResults = url.searchParams.get("numResults");
  const offset = url.searchParams.get("offset");

  if (queryId === null || datasetName === null || corpusName === null) {
    error(400);
  }

  return json(
    await getRelevantDocuments(
      queryId,
      datasetName,
      corpusName,
      match,
      orderBy,
      desc ? desc === "true" : true,
      numResults ? Number(numResults) : 10,
      offset ? Number(offset) : 0,
    ),
  );
}
