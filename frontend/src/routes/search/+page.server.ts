import {
  MAX_QUERY_LENGTH,
  MAX_SEARCH_RESULT_PAGES,
  SEARCH_RESULTS_PER_PAGE,
} from "$lib/config";
import { getAvailableLanguages, searchDocuments } from "$lib/server/backend";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

/**
 * Return a typed, app-relative search page URL with the requested page number.
 *
 * @param url - The current request URL whose search parameters should be kept.
 * @param pageNum - The search result page number to set in the URL.
 * @returns The app-relative search URL.
 */
function pageLink(url: URL, pageNum: number): `/search?${string}` {
  const searchParams = new URLSearchParams(url.searchParams);
  searchParams.set("p", pageNum.toString());
  return `/search?${searchParams}`;
}

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
    pageNum > MAX_SEARCH_RESULT_PAGES
  ) {
    pageNum = 1;
  }

  const result = await searchDocuments(
    q,
    language,
    SEARCH_RESULTS_PER_PAGE,
    pageNum,
    corpusNames,
  );
  const totalPages = Math.ceil(result.totalNumItems / SEARCH_RESULTS_PER_PAGE);

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

  let prevPageLink: `/search?${string}` | null = null;
  if (pageNum > 1) {
    prevPageLink = pageLink(url, pageNum - 1);
  }

  let nextPageLink: `/search?${string}` | null = null;
  if (pageNum < totalPages) {
    nextPageLink = pageLink(url, pageNum + 1);
  }

  return {
    q: q.slice(0, MAX_QUERY_LENGTH),
    corpusNames: corpusNames,
    result: result,
    pageNum: pageNum,
    totalPages: totalPages,
    prevPageLink: prevPageLink,
    nextPageLink: nextPageLink,
  };
};
