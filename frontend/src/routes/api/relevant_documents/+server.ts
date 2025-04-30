import { getRelevantDocuments } from "$lib/server/backend";
import { error, json } from "@sveltejs/kit";

export async function GET({ url }) {
  const queryID = url.searchParams.get("query_id");
  const datasetName = url.searchParams.get("dataset_name");
  const corpusName = url.searchParams.get("corpus_name");
  const numResults = url.searchParams.get("num_results");
  const offset = url.searchParams.get("offset");

  if (queryID === null || datasetName === null || corpusName === null) {
    error(400);
  }

  return json(
    await getRelevantDocuments(
      queryID,
      datasetName,
      corpusName,
      numResults ? Number(numResults) : null,
      offset ? Number(offset) : null,
    ),
  );
}
