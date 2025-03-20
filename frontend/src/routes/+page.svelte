<script lang="ts">
  import type { PageProps } from "./$types";
  import Logo from "$lib/components/Logo.svelte";
  import SearchBar from "$lib/components/SearchBar.svelte";

  let { data }: PageProps = $props();
</script>

<div class="flex flex-col w-full h-full items-center justify-center">
  <div class="m-8">
    <Logo textSize={"text-6xl"} />
  </div>
  <SearchBar corpora={data.corpora} />
</div>
