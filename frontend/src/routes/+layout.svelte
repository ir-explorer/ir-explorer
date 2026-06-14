<script lang="ts">
  import NavProgress from "$lib/components/NavProgress.svelte";
  import { selectedOptions } from "$lib/options.svelte";
  import { untrack } from "svelte";
  import "../app.css";
  import type { LayoutProps } from "./$types";

  const { data, children }: LayoutProps = $props();
  const defaultOptions = untrack(() => data.defaultOptions);

  // if values are missing, fall back to defaults
  if (selectedOptions.queryLanguage === null) {
    selectedOptions.queryLanguage = defaultOptions.queryLanguage;
  }
  if (selectedOptions.modelName === null) {
    selectedOptions.modelName = defaultOptions.modelName;
  }
</script>

<svelte:head>
  <title>IR explorer</title>
</svelte:head>

<NavProgress />
<div class="grid max-h-full min-h-screen w-screen max-w-full grid-rows-[1fr]">
  <div>
    {@render children()}
  </div>
</div>
