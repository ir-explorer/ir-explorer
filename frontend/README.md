# IR Explorer Frontend

The frontend is based on [SvelteKit](https://svelte.dev/) and [Tailwind CSS](https://tailwindcss.com/).

In order to run the frontend locally, install [node.js](https://nodejs.org) and run:

- `npm install`
- `npm run dev`

The app reads the following environment variables:

- `BACKEND_HOST`
- `BACKEND_PORT`
- `PUBLIC_SEARCH_RESULTS_PER_PAGE`
- `PUBLIC_MAX_SEARCH_RESULT_PAGES`
- `PUBLIC_MAX_ITEMS_PER_PAGE`
- `PUBLIC_MAX_SNIPPET_LENGTH`
