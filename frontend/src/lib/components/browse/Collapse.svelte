<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    /** Render the head. */
    head: Snippet | null;
    /** Render the collapsible item. */
    item: Snippet;
  }

  let { head, item }: Props = $props();
</script>

<!--
@component
A collapsible item.
-->
<div class="collapse-arrow collapse z-0 border border-base-300 shadow">
  <input type="checkbox" checked />
  <div
    class="collapse-title flex flex-col justify-center rounded-box bg-base-200">
    {#if head !== null}
      {@render head()}
    {/if}
  </div>
  <div class="collapse-content">
    <div
      class="mt-4 max-h-128 overflow-scroll text-sm leading-relaxed whitespace-pre-line">
      {@render item()}
    </div>
  </div>
</div>
