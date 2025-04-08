<script lang="ts">
  import Menu from "./Menu.svelte";
  import Logo from "./Logo.svelte";
  import BusyIndicator from "./BusyIndicator.svelte";

  let { children } = $props();
</script>

<div
  class="fixed top-0 z-1 navbar border-b border-base-300 bg-base-200/75 px-8 backdrop-blur-sm">
  <div class="navbar-start gap-4">
    <Menu />
    <a href="/">
      <Logo />
    </a>
  </div>
  <div class="navbar-center">
    {@render children()}
  </div>
  <div class="navbar-end">
    <BusyIndicator />
  </div>
</div>
