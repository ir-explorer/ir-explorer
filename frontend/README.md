# IR Explorer Frontend

The frontend is based on [SvelteKit](https://svelte.dev/), [Tailwind CSS](https://tailwindcss.com/), [daisyUI](https://daisyui.com/), and [Font Awesome](https://fontawesome.com/).

In order to run the frontend locally, install [node.js](https://nodejs.org) and run:

- `npm install`
- `npm run dev`

The app can be configured with the following environment variables. Defaults are used when they are not set:

- `BACKEND_HOST` (`localhost`)
- `BACKEND_PORT` (`8000`)
- `PUBLIC_SEARCH_RESULTS_PER_PAGE` (`10`): How many search results to display per page.
- `PUBLIC_MAX_SEARCH_RESULT_PAGES` (`100`): How many pages of search results to provide for a query.
- `PUBLIC_MAX_ITEMS_PER_PAGE` (`200`): Maximum number of items that can be loaded at once when browsing.
- `PUBLIC_MAX_SNIPPET_LENGTH` (`1000`): Maximum configurable snippet length when browsing.
- `PUBLIC_MIN_DOCUMENT_LENGTH_SUMMARY` (`500`): The minimum length of a document for the summary button to be displayed.
- `PUBLIC_MAX_QUERY_LENGTH` (`200`): Maximum query length.
- `PUBLIC_MAX_RAG_DOCUMENTS` (`5`): Maximum number of documents that can be used as context for RAG.
