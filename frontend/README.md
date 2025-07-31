# IR Explorer Frontend

The frontend is based on [SvelteKit](https://svelte.dev/), [Tailwind CSS](https://tailwindcss.com/), [daisyUI](https://daisyui.com/), and [Font Awesome](https://fontawesome.com/).

In order to run the frontend locally, install [node.js](https://nodejs.org) and run:

- `npm install`
- `npm run dev`

The app requires the following environment variables to be set:

- `BACKEND_HOST`
- `BACKEND_PORT`
- `PUBLIC_SEARCH_RESULTS_PER_PAGE`: How many search results to display per page.
- `PUBLIC_MAX_SEARCH_RESULT_PAGES`: How many pages of search results to provide for a query.
- `PUBLIC_MAX_ITEMS_PER_PAGE`: Maximum number of items that can be loaded at once when browsing.
- `PUBLIC_MAX_SNIPPET_LENGTH`: Maximum configurable snippet length when browsing.
- `PUBLIC_MIN_DOCUMENT_LENGTH_SUMMARY`: The minimum length of a document for the summary button to be displayed.
