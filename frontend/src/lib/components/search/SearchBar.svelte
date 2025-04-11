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
  <details class="dropdown">
    <summary class="btn btn-circle h-8 w-8">
      <Fa icon={settingsIcon} />
    </summary>
    <div
      class="dropdown-content card-border card mt-4 border-base-300 bg-base-200 shadow">
      <div class="card-body min-w-64">
        <fieldset class="fieldset gap-2">
          <legend class="fieldset-legend">Settings</legend>

          <label class="fieldset-label flex flex-col items-start"
            >Query language
            <select
              class="select w-full select-sm select-primary"
              name="language"
              value={languageInit}>
              {#each languages as language}
                <option value={language}>{language}</option>
              {/each}
            </select>
          </label>

          <label class="fieldset-label flex flex-col items-start"
            >Search only in
            <div
              class="menu w-full gap-2 rounded border border-primary bg-base-100 text-sm">
              {#each corpora as corpus}
                <label>
                  <input
                    type="checkbox"
                    class="checkbox mr-2 checkbox-sm"
                    value={corpus.name}
                    bind:group={selectedCorpora}
                    name="corpus" />
                  {corpus.name}
                </label>
              {/each}
            </div>
          </label>
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
      {#if selectedCorpora.length == 0}
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
