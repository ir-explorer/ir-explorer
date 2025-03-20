<script lang="ts">
  import "../../app.css";
  import SearchBar from "$lib/components/SearchBar.svelte";
  import type { LayoutProps } from "./$types";
  import Logo from "$lib/components/Logo.svelte";

  let { data, children }: LayoutProps = $props();
</script>

<div
  class="sticky top-0 w-screen max-w-full grid grid-cols-[1fr_1.5fr_1fr] items-center justify-center p-2 border-b border-base-300 bg-base-200/75 backdrop-blur-sm"
>
  <a class="px-4 w-fit" href="/">
    <Logo textSize="text-md" />
  </a>
  <SearchBar corpora={data.corpora} />
</div>

{@render children()}
