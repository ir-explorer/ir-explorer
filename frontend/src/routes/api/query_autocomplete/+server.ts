import { error } from "@sveltejs/kit";

export async function GET({ url }) {
  const corpus = url.searchParams.get("corpus");
  const dataset = url.searchParams.get("dataset");
  const input = url.searchParams.get("input");
  const num_results = url.searchParams.get("num_results");

  if (corpus === null || dataset === null || input === null) {
    error(400);
  }

  const response = await fetch(
    "http://127.0.0.1:8000/search_queries?" +
      new URLSearchParams({
        corpus_name: corpus,
        dataset_name: dataset,
        search: input,
        num_results: num_results === null ? "5" : num_results,
      })
  );
  return response;
}
