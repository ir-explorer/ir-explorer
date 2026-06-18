<script lang="ts">
  import { filterIcon, searchIcon } from "$lib/icons";
  import { selectedOptions } from "$lib/options.svelte";
  import { Fa } from "svelte-fa";

  interface Props {
    /** Initial value for the search query field. */
    searchInit?: string | null;
  }

  const { searchInit = null }: Props = $props();
</script>

<!--
@component
A search bar.
-->
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
      {#if selectedOptions.corpusNames.length > 0}
        <span
          class="tooltip tooltip-left text-base-content/50"
          data-tip={selectedOptions.corpusNames.join(", ")}>
          <Fa icon={filterIcon} />
        </span>
      {/if}
      {#each selectedOptions.corpusNames as corpusName (corpusName)}
        <input type="hidden" name="corpus" value={corpusName} />
      {/each}
      <input
        type="hidden"
        name="language"
        value={selectedOptions.queryLanguage} />
    </label>

    <button class="btn join-item w-12 btn-primary" type="submit">
      <Fa icon={searchIcon} />
    </button>
  </div>
</form>
