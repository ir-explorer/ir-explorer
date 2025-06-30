<script lang="ts">
  import BusyIndicator from "./BusyIndicator.svelte";

  const { start = null, center = null, end = null } = $props();
</script>

<div
  class="fixed top-0 z-1 navbar gap-2 border-b border-base-300 bg-base-200/75 px-4 backdrop-blur-sm">
  <div class="navbar-start">
    {#if start}
      {@render start()}
    {/if}
  </div>
  <div class="navbar-center grow">
    {#if center !== null}
      {@render center()}
    {/if}
  </div>
  <div class="navbar-end">
    {#if end}
      {@render end()}
    {:else}
      <BusyIndicator />
    {/if}
  </div>
</div>
