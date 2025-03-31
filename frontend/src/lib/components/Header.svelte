<script lang="ts">
  import Menu from "./Menu.svelte";
  import Logo from "./Logo.svelte";
  import BusyIndicator from "./BusyIndicator.svelte";

  let { children } = $props();
</script>

<div
  class="fixed top-0 px-8 border-b navbar z-1 border-base-300 bg-base-200/75 backdrop-blur-sm"
>
  <div class="gap-4 navbar-start">
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
