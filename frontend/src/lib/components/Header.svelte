<script lang="ts">
  import Menu from "./Menu.svelte";
  import Logo from "./Logo.svelte";
  import BusyIndicator from "./BusyIndicator.svelte";

  let { itemCenter } = $props();
</script>

<div
  class="navbar fixed z-1 top-0 px-8 border-b border-base-300 bg-base-200/75 backdrop-blur-sm"
>
  <div class="navbar-start gap-4">
    <Menu />
    <a href="/">
      <Logo />
    </a>
  </div>
  <div class="navbar-center">
    {@render itemCenter()}
  </div>
  <div class="navbar-end">
    <BusyIndicator />
  </div>
</div>
