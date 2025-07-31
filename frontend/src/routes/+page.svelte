<script lang="ts">
  import BusyIndicator from "$lib/components/BusyIndicator.svelte";
  import IconWithText from "$lib/components/IconWithText.svelte";
  import Logo from "$lib/components/Logo.svelte";
  import MainMenu from "$lib/components/MainMenu.svelte";
  import SearchBar from "$lib/components/search/SearchBar.svelte";
  import { browseIcon } from "$lib/icons";
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();
</script>

<div class="fixed top-0 z-1 navbar px-4">
  <div class="navbar-start flex flex-row gap-4">
    <div class="w-fit">
      <MainMenu availableOptions={data.availableOptions} />
    </div>
    <a href="/browse" class="text-sm link-hover">
      <IconWithText icon={browseIcon} text={"Browse"} />
    </a>
  </div>
  <div class="navbar-end">
    <BusyIndicator />
  </div>
</div>

<div class="flex h-full flex-col items-center justify-center">
  <div class="w-4/5 max-w-128">
    <div class="mb-4">
      <Logo />
    </div>
    <div class="w-full">
      <SearchBar />
    </div>
  </div>
</div>
