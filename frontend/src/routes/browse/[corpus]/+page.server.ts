import { BACKEND_REST_URL } from "$lib/util.js";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch, params }) => {
  const response = await fetch(
    BACKEND_REST_URL +
      "/get_datasets?" +
      new URLSearchParams({ corpus_name: params.corpus })
  );
  return { datasets: await response.json() };
};
