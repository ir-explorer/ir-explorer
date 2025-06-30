<script lang="ts">
  import BusyIndicator from "$lib/components/BusyIndicator.svelte";
  import Logo from "$lib/components/Logo.svelte";
  import MainMenu from "$lib/components/MainMenu.svelte";
  import SearchBar from "$lib/components/search/SearchBar.svelte";
  import { browseIcon } from "$lib/icons";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();

  let searchSettings = $state(data.searchSettings);
</script>

<div class="fixed top-0 z-1 navbar px-4">
  <div class="navbar-start flex flex-row gap-4">
    <div class="w-fit">
      <MainMenu searchOptions={data.searchOptions} bind:searchSettings />
    </div>

    <a href="/browse" class="flex items-center gap-2 text-sm link-hover">
      <Fa icon={browseIcon} />Browse
    </a>
  </div>
  <div class="navbar-end">
    <BusyIndicator />
  </div>
</div>

<div class="flex h-full flex-col items-center justify-center">
  <div class="mb-8 scale-128 md:mb-12 md:scale-196 lg:mb-16 lg:scale-256">
    <Logo />
  </div>
  <div class="w-4/5 max-w-128">
    <SearchBar bind:searchSettings />
  </div>
</div>
