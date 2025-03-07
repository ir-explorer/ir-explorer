import { BACKEND_REST_URL } from "$lib/server/backend";
import { error } from "@sveltejs/kit";

export async function GET({ url }) {
  const corpus = url.searchParams.get("corpus");
  const dataset = url.searchParams.get("dataset");
  const input = url.searchParams.get("input");
  const num_results = url.searchParams.get("num_results");

  if (corpus === null || input === null) {
    error(400);
  }

  var params = new URLSearchParams({
    corpus_name: corpus,
    search: input,
  });
  if (dataset !== null) {
    params.append("dataset_name", dataset);
  }
  if (num_results !== null) {
    params.append("num_results", num_results);
  }

  const response = await fetch(BACKEND_REST_URL + "/search_queries?" + params);
  return response;
}
