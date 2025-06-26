import { getQueries } from "$lib/server/backend";
import { error, json } from "@sveltejs/kit";

export async function GET({ url }) {
  const corpusName = url.searchParams.get("corpus_name");
  const datasetName = url.searchParams.get("dataset_name");
  const match = url.searchParams.get("match");
  const orderBy = url.searchParams.get("order_by");
  const desc = url.searchParams.get("desc");
  const numResults = url.searchParams.get("num_results");
  const offset = url.searchParams.get("offset");

  if (corpusName === null) {
    error(400);
  }

  return json(
    await getQueries(
      corpusName,
      datasetName,
      match,
      orderBy,
      desc ? desc === "true" : true,
      numResults ? Number(numResults) : 10,
      offset ? Number(offset) : 0,
    ),
  );
}
