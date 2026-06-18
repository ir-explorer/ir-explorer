<script lang="ts">
  interface Props {
    /** Whether to render the small variant of the logo. */
    small?: boolean;
  }
  const { small = false }: Props = $props();
</script>

<!--
@component
Render the logo.
-->
{#if small}
  <img src="/logo-sm.svg" alt="IR explorer" class="h-6 w-auto" />
{:else}
  <img src="/logo.svg" alt="IR explorer" class="h-16 w-auto md:h-20 lg:h-24" />
{/if}
