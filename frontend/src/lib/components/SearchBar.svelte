<script lang="ts">
  import type { Corpus } from "$lib/types";
  import { navigating } from "$app/state";

  let {
    corpora,
    searchInit = null,
    selectedCorpusInit = null,
  }: {
    corpora: Corpus[];
    searchInit?: string | null;
    selectedCorpusInit?: string | null;
  } = $props();

  // default to 1st corpus in the list
  let selectedCorpus: Corpus = $state(corpora[0]);

  // if there is an initial value for the corpus name, try to find the corpus
  if (selectedCorpusInit !== null) {
    let corpusFound = corpora.find((c) => c.name === selectedCorpusInit);
    if (corpusFound) selectedCorpus = corpusFound;
  }

  let selectedCorpusName: string = $derived(selectedCorpus.name);
  let search: string = $state(searchInit ? searchInit : "");
  let target: string = $derived(
    selectedCorpus
      ? "/search/" +
          selectedCorpus.name +
          "?" +
          new URLSearchParams({ q: search })
      : "/"
  );
  let disabled: boolean = $derived(Boolean(navigating.to));
</script>

<form class="flex flex-col gap-2">
  <div class="flex flex-row gap-2 items-center">
    <div class="dropdown">
      <div
        tabindex="0"
        role="button"
        class="btn text-lg/tight shadow bg-base-300"
      >
        ⛭
      </div>
      <div class="dropdown-content card card-border mt-2 bg-base-200 shadow">
        <div class="card-body">
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Settings</legend>
            <label class="fieldset-label flex flex-col items-start"
              >Corpus
              <select
                class="select select-sm w-48"
                name="corpora"
                id="corpora"
                bind:value={selectedCorpus}
                {disabled}
              >
                {#each corpora as corpus}
                  <option value={corpus}>{corpus.name}</option>
                {/each}
              </select>
            </label>
          </fieldset>
        </div>
      </div>
    </div>
    <label class="input grow shadow">
      <input
        type="text"
        placeholder="Type a query..."
        bind:value={search}
        {disabled}
      />
      <span class="label">{selectedCorpusName}</span>
    </label>
    <a href={target}>
      <button class="btn w-16 bg-base-300 shadow" type="submit" {disabled}>
        <span class={[disabled && "loading loading-infinity loading-sm"]}
          >Go</span
        >
      </button>
    </a>
  </div>
</form>
