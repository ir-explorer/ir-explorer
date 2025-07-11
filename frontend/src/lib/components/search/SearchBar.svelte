<script lang="ts">
  import { corpusIcon, searchIcon } from "$lib/icons";
  import type { SelectedOptions } from "$lib/types";
  import { Fa } from "svelte-fa";

  interface Props {
    /** The bindable selected options. */
    selectedOptions: SelectedOptions;
    /** Initial value for the search query field. */
    searchInit?: string | null;
  }

  let { selectedOptions = $bindable(), searchInit = null }: Props = $props();
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
        <span class="badge badge-ghost text-xs">
          <Fa icon={corpusIcon} />
          {selectedOptions.corpusNames.length}
        </span>
      {/if}
      {#each selectedOptions.corpusNames as corpusName}
        <input type="hidden" name="corpus" value={corpusName} />
      {/each}
    </label>

    <button class="btn join-item w-12 btn-primary" type="submit">
      <Fa icon={searchIcon} />
    </button>
  </div>
</form>
