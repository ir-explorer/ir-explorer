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
<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
  {#each gridItems as gridItem (getTargetLink(gridItem))}
    <div class="card border border-base-300 shadow hover:bg-base-300">
      <a href={resolve(getTargetLink(gridItem) as `/browse/${string}`)}>
        <div class="card-body">
          {@render item(gridItem)}
        </div>
      </a>
    </div>
  {/each}
</div>
