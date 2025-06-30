<script lang="ts">
  import BusyIndicator from "./BusyIndicator.svelte";

  const { start = null, center = null, end = null } = $props();
</script>

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
