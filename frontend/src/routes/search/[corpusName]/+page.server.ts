import { searchDocuments } from "$lib/server/backend";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  const q = url.searchParams.get("q");

  if (!q || q.trim() == "") {
    redirect(307, "/search");
  }

  return { hits: await searchDocuments(params.corpusName, q) };
};
