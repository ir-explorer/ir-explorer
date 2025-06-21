<script lang="ts">
  import { corpusIcon, searchIcon, settingsIcon } from "$lib/icons";
  import type { SearchOptions, SearchOptionsInit } from "$lib/types";
  import { Fa } from "svelte-fa";

  let {
    searchOptions,
    searchOptionsInit = null,
    searchInit = null,
  }: {
    searchOptions: SearchOptions;
    searchOptionsInit?: SearchOptionsInit | null;
    searchInit?: string | null;
  } = $props();

  let selectedCorpusNames: string[] = $state([]);
  let languageInit = $state("English");
  if (searchOptionsInit != null) {
    selectedCorpusNames = searchOptionsInit.selected_corpus_names;
    if (searchOptionsInit.query_language != null) {
      languageInit = searchOptionsInit.query_language;
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
              {#each searchOptions.query_languages as language}
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
            {#each searchOptions.corpus_names as corpusName}
              <label>
                <input
                  type="checkbox"
                  class="toggle mr-2 toggle-sm"
                  value={corpusName}
                  bind:group={selectedCorpusNames}
                  name="corpus" />
                {corpusName}
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
      {#if selectedCorpusNames.length == 0 || selectedCorpusNames.length == searchOptions.corpus_names.length}
        all corpora
      {:else if selectedCorpusNames.length == 1}
        {selectedCorpusNames[0]}
      {:else}
        {selectedCorpusNames.length} corpora
      {/if}
    </span>
  </label>

  <button class="btn w-12 btn-primary" type="submit">
    <Fa icon={searchIcon} />
  </button>
</form>
