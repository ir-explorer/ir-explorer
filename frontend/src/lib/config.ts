import { env } from "$env/dynamic/public";

/**
 * Read a public numeric environment variable, falling back to a default when it
 * is missing, empty, or cannot be parsed.
 *
 * @param name - The public environment variable name to read.
 * @param defaultValue - The value to use when the environment variable is unset or invalid.
 *
 * @returns The parsed numeric environment value, or the default value.
 */
function numberEnv(name: `PUBLIC_${string}`, defaultValue: number): number {
  const value = env[name];
  if (value === undefined || value.trim() === "") {
    return defaultValue;
  }

  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : defaultValue;
}

export const SEARCH_RESULTS_PER_PAGE = numberEnv(
  "PUBLIC_SEARCH_RESULTS_PER_PAGE",
  10,
);
export const MAX_SEARCH_RESULT_PAGES = numberEnv(
  "PUBLIC_MAX_SEARCH_RESULT_PAGES",
  100,
);
export const MAX_ITEMS_PER_PAGE = numberEnv("PUBLIC_MAX_ITEMS_PER_PAGE", 200);
export const MAX_SNIPPET_LENGTH = numberEnv("PUBLIC_MAX_SNIPPET_LENGTH", 1000);
export const MIN_DOCUMENT_LENGTH_SUMMARY = numberEnv(
  "PUBLIC_MIN_DOCUMENT_LENGTH_SUMMARY",
  500,
);
export const MAX_QUERY_LENGTH = numberEnv("PUBLIC_MAX_QUERY_LENGTH", 200);
export const MAX_RAG_DOCUMENTS = numberEnv("PUBLIC_MAX_RAG_DOCUMENTS", 5);
