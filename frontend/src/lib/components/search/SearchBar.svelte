<script lang="ts">
  import type { Corpus } from "$lib/types";
  import { Fa } from "svelte-fa";
  import { corpusIcon, settingsIcon, searchIcon } from "$lib/icons";

  let {
    corpora,
    searchInit = null,
    languageInit = null,
    selectedCorporaInit = [],
  }: {
    corpora: Corpus[];
    searchInit?: string | null;
    languageInit?: string | null;
    selectedCorporaInit?: string[];
  } = $props();

  let languages = new Set();
  for (const corpus of corpora) {
    languages.add(corpus.language);
  }

  let selectedCorpora = $state(selectedCorporaInit);

  // if no valid language is specified, select english if it exists.
  // otherwise, fall back to a random one
  if (languageInit == null || !languages.has(languageInit)) {
    if (languages.has("english")) {
      languageInit = "english";
    } else {
      languageInit = corpora[0].language;
    }
  }
</script>

<form
  class="flex w-full flex-row items-center gap-2"
  action="/search"
  method="get">
  <details class="dropdown dropdown-start">
    <summary class="btn btn-circle h-8 w-8">
      <Fa icon={settingsIcon} />
    </summary>
    <div
      class="dropdown-content card-border card mt-2 border-base-300 bg-base-200/75 shadow backdrop-blur-sm">
      <div class="card-body min-w-64">
        <fieldset class="fieldset gap-2">
          <legend class="fieldset-legend">Search settings</legend>

          <label class="fieldset-label flex flex-col items-start"
            >Query language
            <select
              class="select w-full select-sm"
              name="language"
              value={languageInit}>
              {#each languages as language}
                <option value={language}>{language}</option>
              {/each}
            </select>
          </label>

          <label
            for="filter-corpora"
            class="fieldset-label flex flex-col items-start">
            Search only in
          </label>
          <div
            id="filter-corpora"
            class="menu w-full gap-2 rounded-box border border-base-300 bg-base-100 text-sm">
            {#each corpora as corpus}
              <label>
                <input
                  type="checkbox"
                  class="toggle mr-2 toggle-sm"
                  value={corpus.name}
                  bind:group={selectedCorpora}
                  name="corpus" />
                {corpus.name}
              </label>
            {/each}
          </div>
        </fieldset>
      </div>
    </div>
  </details>

  <label class="input grow input-primary">
    <input
      type="text"
      placeholder="Type a query..."
      value={searchInit ? searchInit : ""}
      name="q" />
    <span class="label"
      ><Fa icon={corpusIcon} />
      {#if selectedCorpora.length == 0 || selectedCorpora.length == corpora.length}
        all corpora
      {:else if selectedCorpora.length == 1}
        {selectedCorpora[0]}
      {:else}
        {selectedCorpora.length} corpora
      {/if}
    </span>
  </label>

  <button class="btn w-12 btn-primary" type="submit">
    <Fa icon={searchIcon} />
  </button>
</form>
