<script lang="ts">
  import BusyIndicator from "$lib/components/BusyIndicator.svelte";
  import Logo from "$lib/components/Logo.svelte";
  import SearchBar from "$lib/components/search/SearchBar.svelte";
  import { browseIcon } from "$lib/icons";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();
</script>

<div class="fixed top-0 z-1 navbar px-8">
  <div class="navbar-start">
    <a href="/browse" class="flex items-center gap-2 text-sm link-hover">
      <Fa icon={browseIcon} />Browse
    </a>
  </div>
  <div class="navbar-end">
    <BusyIndicator />
  </div>
</div>
<div class="flex h-full flex-col items-center justify-center">
  <div class="mb-16 scale-250">
    <Logo />
  </div>
  <div class="w-1/3 min-w-128">
    <SearchBar searchOptions={data.searchOptions} />
  </div>
</div>
