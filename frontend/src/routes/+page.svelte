<script lang="ts">
  import type { PageProps } from "./$types";
  import Logo from "$lib/components/Logo.svelte";
  import SearchBar from "$lib/components/SearchBar.svelte";
  import BusyIndicator from "$lib/components/BusyIndicator.svelte";
  import Menu from "$lib/components/Menu.svelte";

  let { data }: PageProps = $props();
</script>

<div class="fixed top-0 px-8 navbar z-1">
  <div class="navbar-start"><Menu /></div>
  <div class="navbar-end">
    <BusyIndicator />
  </div>
</div>
<div class="flex flex-col items-center justify-center h-full">
  <div class="mb-16 scale-250">
    <Logo />
  </div>
  <div class="w-1/3 min-w-128">
    <SearchBar corpora={data.corpora} />
  </div>
</div>
