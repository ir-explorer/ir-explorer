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
  class="fixed z-1 top-0 w-full grid grid-cols-[1fr_1.5fr_1fr] items-center px-8 py-2 border-b border-base-300 bg-base-200/75 backdrop-blur-sm"
>
  <a href="/" class="w-fit">
    <Logo />
  </a>
  <SearchBar
    corpora={data.corpora}
    {searchInit}
    selectedCorpusNameInit={data.selectedCorpus}
  />
  <div class="ml-auto scale-150">
    <BusyIndicator />
  </div>
</div>

<div class="max-w-full mt-16 mb-4">
  <div class="max-w-5xl mx-auto">
    {@render children()}
  </div>
</div>
