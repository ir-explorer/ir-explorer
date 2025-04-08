<script lang="ts">
  import { navigating } from "$app/state";

  let busy: boolean = $derived(Boolean(navigating.to));
</script>

<div class={[busy && "loading", "loading-xl text-primary loading-ring"]}></div>
