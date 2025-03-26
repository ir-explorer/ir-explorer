import { autocomplete_query } from "$lib/server/backend";
import { error, json } from "@sveltejs/kit";

export async function GET({ url }) {
  const corpus_name = url.searchParams.get("corpus");
  const dataset_name = url.searchParams.get("dataset");
  const input = url.searchParams.get("input");
  const num_results = url.searchParams.get("num_results");

  if (corpus_name === null || input === null) {
    error(400);
  }

  return json(
    await autocomplete_query(
      input,
      corpus_name,
      dataset_name,
      num_results ? Number(num_results) : null,
    ),
  );
}
