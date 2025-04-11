import { searchDocuments } from "$lib/server/backend";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ url }) => {
  const q = url.searchParams.get("q");
  const corpusName = url.searchParams.get("corpus");
  const language = url.searchParams.get("language");
  if (!q || q.trim().length == 0) {
    redirect(307, "/");
  }

  let pageNum = Number(url.searchParams.get("p"));
  if (!Number.isInteger(pageNum) || pageNum < 1) {
    pageNum = 1;
  }

  const resultsPerPage = 10;
  const result = await searchDocuments(
    q,
    language ?? "english",
    resultsPerPage,
    pageNum,
    corpusName,
  );
  const totalPages = Math.ceil(result.total_num_items / resultsPerPage);

  if (totalPages == 0) {
    return {
      result: result,
      pageNum: pageNum,
      totalPages: totalPages,
      prevPageLink: null,
      nextPageLink: null,
    };
  }

  if (pageNum > totalPages) {
    redirect(307, "/");
  }

  let prevPageLink = null;
  if (pageNum > 1) {
    let prevPageUrl = new URL(url);
    prevPageUrl.searchParams.set("p", (pageNum - 1).toString());
    prevPageLink = prevPageUrl.toString();
  }

  let nextPageLink = null;
  if (pageNum < totalPages) {
    let nextPageUrl = new URL(url);
    nextPageUrl.searchParams.set("p", (pageNum + 1).toString());
    nextPageLink = nextPageUrl.toString();
  }

  return {
    result: result,
    pageNum: pageNum,
    totalPages: totalPages,
    prevPageLink: prevPageLink,
    nextPageLink: nextPageLink,
  };
};
