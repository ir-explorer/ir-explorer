import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch, params }) => {
  const response = await fetch(
    "http://127.0.0.1:8000/get_datasets?" +
      new URLSearchParams({ corpus_name: params.corpus })
  );
  return { datasets: await response.json() };
};
