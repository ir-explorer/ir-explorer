import { searchDocuments } from "$lib/server/backend";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  const q = url.searchParams.get("q");
  if (!q || q.trim().length == 0) {
    redirect(307, "/search");
  }

  let page = Number(url.searchParams.get("p"));
  if (isNaN(page) || page < 1) {
    page = 1;
  }

  return {
    result: await searchDocuments(params.corpusName, q, 10, page),
    page: page,
  };
};
