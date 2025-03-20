<script lang="ts">
  import type { Corpus } from "$lib/types";
  import { navigating } from "$app/state";

  let {
    corpora,
    searchInit = null,
    selectedCorpusNameInit = null,
  }: {
    corpora: Corpus[];
    searchInit?: string | null;
    selectedCorpusNameInit?: string | null;
  } = $props();

  // if no initial corpus name is provided, default to the 1st in the list
  let selectedCorpusName: string = $state(
    selectedCorpusNameInit ? selectedCorpusNameInit : corpora[0].name
  );
  let search: string = $state(searchInit ? searchInit : "");
  let target: string = $derived(
    "/search/" + selectedCorpusName + "?" + new URLSearchParams({ q: search })
  );
  let disabled: boolean = $derived(Boolean(navigating.to));
</script>

<form class="flex flex-col gap-2">
  <div class="flex flex-row gap-2 items-center">
    <div class="dropdown">
      <div
        tabindex="0"
        role="button"
        class="btn btn-sm rounded-full h-8 w-8 btn-primary text-lg/tight"
      >
        ⛭
      </div>
      <div class="dropdown-content card card-border mt-4 bg-base-200 shadow">
        <div class="card-body">
          <fieldset class="fieldset">
            <legend class="fieldset-legend">Settings</legend>
            <label class="fieldset-label flex flex-col items-start"
              >Corpus
              <select
                class="select select-primary select-sm w-48"
                name="corpora"
                id="corpora"
                bind:value={selectedCorpusName}
                {disabled}
              >
                {#each corpora as corpus}
                  <option value={corpus.name}>{corpus.name}</option>
                {/each}
              </select>
            </label>
          </fieldset>
        </div>
      </div>
    </div>
    <label class="input input-primary grow">
      <input
        type="text"
        placeholder="Type a query..."
        bind:value={search}
        {disabled}
      />
      <span class="label">{selectedCorpusName}</span>
    </label>
    <a href={target}>
      <button class="btn btn-primary w-16" type="submit" {disabled}>
        <span class={[disabled && "loading loading-infinity loading-sm"]}
          >Go</span
        >
      </button>
    </a>
  </div>
</form>
