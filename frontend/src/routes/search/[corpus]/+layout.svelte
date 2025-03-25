<script lang="ts">
  import type { LayoutProps } from "./$types";
  import { page } from "$app/state";
  import SearchBar from "$lib/components/SearchBar.svelte";
  import Header from "$lib/components/Header.svelte";

  let { data, children }: LayoutProps = $props();
  let searchInit = $derived(page.url.searchParams.get("q"));
</script>

<Header>
  <div class="w-2xl">
    <SearchBar
      corpora={data.corpora}
      {searchInit}
      selectedCorpusNameInit={data.selectedCorpus}
    />
  </div></Header
>

<div class="max-w-full mt-20 mb-4">
  <div class="max-w-5xl mx-auto">
    {@render children()}
  </div>
</div>
