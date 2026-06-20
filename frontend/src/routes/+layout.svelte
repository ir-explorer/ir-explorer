<script lang="ts">
  import NavProgress from "$lib/components/NavProgress.svelte";
  import { selectedOptions } from "$lib/options.svelte";
  import { untrack } from "svelte";
  import "../app.css";
  import type { LayoutProps, Snapshot } from "./$types";

  const { data, children }: LayoutProps = $props();
  const defaultOptions = untrack(() => data.defaultOptions);

  // if values are missing, fall back to defaults
  if (selectedOptions.queryLanguage === null) {
    selectedOptions.queryLanguage = defaultOptions.queryLanguage;
  }
  if (selectedOptions.modelName === null) {
    selectedOptions.modelName = defaultOptions.modelName;
  }

  export const snapshot: Snapshot<{ scrollX: number; scrollY: number }> = {
    capture: () => ({ scrollX: window.scrollX, scrollY: window.scrollY }),
    restore: ({ scrollX, scrollY }) => {
      // wait until list snapshots have rendered their saved items
      requestAnimationFrame(() => {
        window.scrollTo(scrollX, scrollY);
      });
    },
  };
</script>

<svelte:head>
  <title>IR explorer</title>
</svelte:head>

<NavProgress />
<div class="min-h-screen w-screen max-w-full">
  <div class="min-h-screen">
    {@render children()}
  </div>
</div>
