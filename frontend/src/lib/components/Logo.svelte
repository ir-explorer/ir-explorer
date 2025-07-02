<script lang="ts">
  const { small = false } = $props();
</script>

{#if small}
  <img src="/logo-sm.svg" alt="IR explorer" class="h-6" />
{:else}
  <img src="/logo.svg" alt="IR explorer" class="h-16 md:h-20 lg:h-24" />
{/if}
