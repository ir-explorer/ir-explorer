<script lang="ts">
  import type { LayoutProps } from "./$types";
  import { page } from "$app/state";
  import SearchBar from "$lib/components/SearchBar.svelte";
  import Logo from "$lib/components/Logo.svelte";
  import BusyIndicator from "$lib/components/BusyIndicator.svelte";

  let { data, children }: LayoutProps = $props();
  let searchInit = $derived(page.url.searchParams.get("q"));
</script>

<div
  class="navbar fixed z-1 top-0 px-8 border-b border-base-300 bg-base-200/75 backdrop-blur-sm"
>
  <div class="navbar-start">
    <a href="/">
      <Logo />
    </a>
  </div>
  <div class="navbar-center w-2xl">
    <SearchBar
      corpora={data.corpora}
      {searchInit}
      selectedCorpusNameInit={data.selectedCorpus}
    />
  </div>
  <div class="navbar-end">
    <BusyIndicator />
  </div>
</div>

<div class="max-w-full mt-16 mb-4">
  <div class="max-w-5xl mx-auto">
    {@render children()}
  </div>
</div>
