<script lang="ts">
  import type { Corpus } from "$lib/types";
  import { Fa } from "svelte-fa";
  import { corpusIcon, settingsIcon, searchIcon } from "$lib/icons";

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
    selectedCorpusNameInit ? selectedCorpusNameInit : corpora[0].name,
  );
  let action: string = $derived("/search/" + selectedCorpusName);
</script>

<form class="flex w-full flex-row items-center gap-2" {action} method="get">
  <div class="dropdown">
    <div tabindex="0" role="button" class="btn btn-circle h-8 w-8">
      <Fa icon={settingsIcon} />
    </div>
    <div class="dropdown-content card-border card mt-2 bg-base-200 shadow">
      <div class="card-body">
        <fieldset class="fieldset">
          <legend class="fieldset-legend">Settings</legend>
          <label class="fieldset-label flex flex-col items-start"
            >Corpus
            <select
              class="select w-48 select-sm select-primary"
              name="corpora"
              id="corpora"
              bind:value={selectedCorpusName}>
              {#each corpora as corpus}
                <option value={corpus.name}>{corpus.name}</option>
              {/each}
            </select>
          </label>
        </fieldset>
      </div>
    </div>
  </div>
  <label class="input grow input-primary">
    <input
      type="text"
      placeholder="Type a query..."
      value={searchInit ? searchInit : ""}
      name="q" />
    <span class="label"><Fa icon={corpusIcon} />{selectedCorpusName}</span>
  </label>
  <button class="btn w-12 btn-primary" type="submit">
    <Fa icon={searchIcon} />
  </button>
</form>
