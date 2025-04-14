import { getQueries } from "$lib/server/backend";
import { error, json } from "@sveltejs/kit";

export async function GET({ url }) {
  const corpusName = url.searchParams.get("corpus_name");
  const datasetName = url.searchParams.get("dataset_name");
  const input = url.searchParams.get("input");
  const numResults = url.searchParams.get("num_results");
  const offset = url.searchParams.get("offset");

  if (corpusName === null) {
    error(400);
  }

  return json(
    await getQueries(
      corpusName,
      datasetName,
      input,
      numResults ? Number(numResults) : null,
      offset ? Number(offset) : null,
    ),
  );
}
