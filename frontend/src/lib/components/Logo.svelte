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
  <img src="/logo-sm.svg" alt="IR explorer" class="irx-logo h-6" />
{:else}
  <img
    src="/logo.svg"
    alt="IR explorer"
    class="irx-logo h-16 md:h-20 lg:h-24" />
{/if}

<style>
  :global(html[data-theme="irx-dark"]) .irx-logo {
    filter: invert(1) hue-rotate(180deg);
  }

  @media (prefers-color-scheme: dark) {
    :global(html:not([data-theme])) .irx-logo {
      filter: invert(1) hue-rotate(180deg);
    }
  }
</style>
