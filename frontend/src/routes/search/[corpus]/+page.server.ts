import { BACKEND_REST_URL } from "$lib/util.js";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch, params, url }) => {
  const query_string = url.searchParams.get("q");

  if (query_string === null) {
    redirect(307, "/search");
  }

  const request =
    BACKEND_REST_URL +
    "/search_documents?" +
    new URLSearchParams({
      corpus_name: params.corpus,
      search: query_string,
    });

  const response = await fetch(request);
  return { hits: await response.json() };
};
