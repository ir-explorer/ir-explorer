<script lang="ts" generics="T">
  import { resolve } from "$app/paths";
  import type { BrowseLink } from "$lib/types";
  import type { Snippet } from "svelte";

  interface Props {
    /** Items to render in the grid. */
    gridItems: T[];
    /** Render a single grid item. */
    item: Snippet<[T]>;
    /** Return the target for a specific item. */
    getTargetLink: (gridItem: T) => BrowseLink;
  }

  const { gridItems, item, getTargetLink }: Props = $props();
</script>

<!--
@component
Render items as cards in a grid.
-->
<div class="grid grid-cols-1 gap-3 md:grid-cols-2">
  {#each gridItems as gridItem (getTargetLink(gridItem))}
    <a
      href={resolve(getTargetLink(gridItem) as `/browse/${string}`)}
      class="block rounded-box border border-base-300 bg-base-100 px-4 py-3 shadow-sm hover:border-primary hover:bg-base-200">
      <div class="min-w-0">
        {@render item(gridItem)}
      </div>
    </a>
  {/each}
</div>
