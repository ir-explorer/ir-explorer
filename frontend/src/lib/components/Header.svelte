<script lang="ts">
  import Menu from "./Menu.svelte";
  import Logo from "./Logo.svelte";
  import BusyIndicator from "./BusyIndicator.svelte";

  let { start = null, center = null, end = null } = $props();
</script>

<div
  class="fixed top-0 z-1 navbar border-b border-base-300 bg-base-200/75 px-8 backdrop-blur-sm">
  <div class="navbar-start">
    {#if start}
      {@render start()}
    {:else}
      <div class="flex gap-4">
        <Menu />
        <a href="/">
          <Logo />
        </a>
      </div>
    {/if}
  </div>
  <div class="navbar-center">
    {@render center?.()}
  </div>
  <div class="navbar-end">
    {#if end}
      {@render end()}
    {:else}
      <BusyIndicator />
    {/if}
  </div>
</div>
