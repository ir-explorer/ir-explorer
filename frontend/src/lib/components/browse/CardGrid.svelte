<script lang="ts" generics="T">
  import type { Snippet } from "svelte";

  let {
    gridItems,
    item,
    getTargetLink,
  }: {
    gridItems: T[];
    item: Snippet<[T]>;
    getTargetLink: (gridItem: T) => string;
  } = $props();
</script>

<div class="grid grid-cols-3 gap-4">
  {#each gridItems as gridItem}
    <div
      class="card border border-base-300 bg-base-100 shadow hover:bg-base-300">
      <a href={getTargetLink(gridItem)}>
        <div class="card-body">
          {@render item(gridItem)}
        </div>
      </a>
    </div>
  {/each}
</div>
