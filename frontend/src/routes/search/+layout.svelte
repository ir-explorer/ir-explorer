<script lang="ts">
  import { page } from "$app/state";
  import Header from "$lib/components/Header.svelte";
  import SearchBar from "$lib/components/search/SearchBar.svelte";
  import type { SearchOptionsInit } from "$lib/types";
  import type { LayoutProps } from "./$types";

  let { data, children }: LayoutProps = $props();
  let searchInit = page.url.searchParams.get("q");
  let searchOptionsInit = {
    query_language: page.url.searchParams.get("language"),
    selected_corpus_names: page.url.searchParams.getAll("corpus"),
  } as SearchOptionsInit;
</script>

<Header>
  {#snippet center()}
    <div class="w-2xl">
      <SearchBar
        searchOptions={data.searchOptions}
        {searchInit}
        {searchOptionsInit} />
    </div>
  {/snippet}
</Header>

<div class="mx-4 mt-20 mb-4 max-w-full">
  <div class="mx-auto max-w-5xl">
    {@render children()}
  </div>
</div>
