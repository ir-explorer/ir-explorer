<script lang="ts">
  import { page } from "$app/state";
  import Header from "$lib/components/Header.svelte";
  import Logo from "$lib/components/Logo.svelte";
  import MainMenu from "$lib/components/MainMenu.svelte";
  import SearchBar from "$lib/components/search/SearchBar.svelte";
  import type { LayoutProps } from "./$types";

  let { data, children }: LayoutProps = $props();
  let searchSettings = $state(data.searchSettings);
  let searchInit = page.url.searchParams.get("q");
</script>

<Header>
  {#snippet start()}
    <div class="flex flex-row gap-4">
      <MainMenu searchOptions={data.searchOptions} bind:searchSettings />
      <a class="hidden lg:block" href="/"><Logo /></a>
    </div>
  {/snippet}

  {#snippet center()}
    <div class="w-160">
      <SearchBar bind:searchSettings {searchInit} />
    </div>
  {/snippet}
</Header>

<div class="mx-auto mt-20 mb-4 max-w-5xl">
  <div class="mx-4">
    {@render children()}
  </div>
</div>
