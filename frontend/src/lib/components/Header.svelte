<script lang="ts">
  import type { Snippet } from "svelte";
  import BusyIndicator from "./BusyIndicator.svelte";

  interface Props {
    /** Item(s) to render at the start of the header. */
    start?: Snippet | null;
    /** Item(s) to render in the center of the header. */
    center?: Snippet | null;
    /** Item(s) to render at the end of the header. */
    end?: Snippet | null;
  }

  const { start = null, center = null, end = null }: Props = $props();
</script>

<!--
@component
A fixed full-width header bar.

If `end` is not provided, a `BusyIndicator` is is rendered.
-->
<div
  class="fixed top-0 z-1 navbar border-b border-base-300 bg-base-200/75 px-4 backdrop-blur-sm">
  <div class="navbar-start w-1/6">
    {#if start}
      {@render start()}
    {/if}
  </div>
  <div class="navbar-center flex max-w-2/3 min-w-0 grow justify-center">
    {#if center !== null}
      {@render center()}
    {/if}
  </div>
  <div class="navbar-end w-1/6">
    {#if end}
      {@render end()}
    {:else}
      <BusyIndicator />
    {/if}
  </div>
</div>
