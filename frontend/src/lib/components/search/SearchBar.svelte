<script lang="ts">
  import { corpusIcon, searchIcon } from "$lib/icons";
  import type { SearchSettings } from "$lib/types";
  import { Fa } from "svelte-fa";

  let {
    searchSettings = $bindable(),
    searchInit = null,
  }: {
    searchSettings: SearchSettings;
    searchInit?: string | null;
  } = $props();
</script>

<form
  class="flex w-full flex-row items-center gap-2"
  action="/search"
  method="get">
  <div class="join grow">
    <label class="input join-item grow input-primary">
      <input
        type="text"
        placeholder="Type a query..."
        value={searchInit ? searchInit : ""}
        name="q" />
      <span class="label"
        ><Fa icon={corpusIcon} />
        {#if searchSettings.corpusNames.length == 0}
          all corpora
        {:else if searchSettings.corpusNames.length == 1}
          {searchSettings.corpusNames[0]}
        {:else}
          {searchSettings.corpusNames.length} corpora
        {/if}
      </span>
      {#each searchSettings.corpusNames as corpusName}
        <input type="hidden" name="corpus" value={corpusName} />
      {/each}
    </label>

    <button class="btn join-item w-12 btn-primary" type="submit">
      <Fa icon={searchIcon} />
    </button>
  </div>
</form>
