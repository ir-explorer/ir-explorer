<script lang="ts">
  import { clearFilterIcon, filterIcon, searchIcon } from "$lib/icons";
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
        <button
          class="group tooltip btn tooltip-left btn-circle text-base-content/50 btn-ghost btn-xs"
          type="button"
          data-tip={selectedOptions.corpusNames.join(", ")}
          onclick={() => (selectedOptions.corpusNames = [])}>
          <span class="block group-hover:hidden group-focus-visible:hidden">
            <Fa icon={filterIcon} />
          </span>
          <span class="hidden group-hover:block group-focus-visible:block">
            <Fa icon={clearFilterIcon} />
          </span>
        </button>
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
