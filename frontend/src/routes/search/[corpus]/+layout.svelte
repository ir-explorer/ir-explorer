<script lang="ts">
  import type { LayoutProps } from "./$types";
  import { page } from "$app/state";
  import SearchBar from "$lib/components/SearchBar.svelte";
  import Logo from "$lib/components/Logo.svelte";

  let { data, children }: LayoutProps = $props();
  let searchInit = $derived(page.url.searchParams.get("q"));
</script>

<div
  class="fixed top-0 w-screen max-w-full grid grid-cols-[1fr_1.5fr_1fr] items-center justify-center p-2 border-b border-base-300 bg-base-200/75 backdrop-blur-sm"
>
  <a class="mx-2 p-2 w-fit" href="/">
    <Logo textSize="text-2xl" />
  </a>
  <SearchBar
    corpora={data.corpora}
    {searchInit}
    selectedCorpusNameInit={data.selectedCorpus}
  />
</div>

<div class="mt-16">
  {@render children()}
</div>
