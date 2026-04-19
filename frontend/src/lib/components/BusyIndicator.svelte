<script lang="ts">
  import { navigating } from "$app/state";

  const busy: boolean = $derived(Boolean(navigating.to));
</script>

<!--
@component
A loading indicator displayed when the app navigates.
-->
<div class={[busy && "loading", "loading-xl loading-ring text-primary"]}></div>
