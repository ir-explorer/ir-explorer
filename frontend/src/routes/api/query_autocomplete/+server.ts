import { autocompleteQuery } from "$lib/server/backend";
import { error, json } from "@sveltejs/kit";

export async function GET({ url }) {
  const corpusName = url.searchParams.get("corpus");
  const datasetName = url.searchParams.get("dataset");
  const input = url.searchParams.get("input");
  const numResults = url.searchParams.get("num_results");

  if (corpusName === null || input === null) {
    error(400);
  }

  return json(
    await autocompleteQuery(
      input,
      corpusName,
      datasetName,
      numResults ? Number(numResults) : null,
    ),
  );
}
