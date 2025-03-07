import { BACKEND_REST_URL } from "$lib/server/backend";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch }) => {
  const response = await fetch(BACKEND_REST_URL + "/get_corpora");
  return { corpora: await response.json() };
};
