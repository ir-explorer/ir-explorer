import {
  PUBLIC_MAX_SEARCH_RESULT_PAGES,
  PUBLIC_SEARCH_RESULTS_PER_PAGE,
} from "$env/static/public";
import { getAvailableLanguages, searchDocuments } from "$lib/server/backend";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ url }) => {
  const q = url.searchParams.get("q");
  const corpusNames = url.searchParams.getAll("corpus");
  if (!q || q.trim().length == 0) {
    redirect(307, "/");
  }

  let language = url.searchParams.get("language");
  const availableLanguages = await getAvailableLanguages();

  // ignore unsupported languages
  if (language != null && !availableLanguages.includes(language)) {
    language = null;
  }

  let pageNum = Number(url.searchParams.get("p"));
  if (
    !Number.isInteger(pageNum) ||
    pageNum < 1 ||
    pageNum > PUBLIC_MAX_SEARCH_RESULT_PAGES
  ) {
    pageNum = 1;
  }

  const result = await searchDocuments(
    q,
    language,
    PUBLIC_SEARCH_RESULTS_PER_PAGE,
    pageNum,
    corpusNames,
  );
  const totalPages = Math.ceil(
    result.totalNumItems / PUBLIC_SEARCH_RESULTS_PER_PAGE,
  );

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
