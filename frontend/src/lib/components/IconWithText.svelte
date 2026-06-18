<script lang="ts">
  import type { IconDefinition } from "@fortawesome/free-solid-svg-icons";
  import Fa from "svelte-fa";

  interface Props {
    /** The icon to render. */
    icon: IconDefinition;
    /** The text to display. */
    text: string;
    /** Whether to display the icon on the right of the text. */
    iconRight?: boolean;
  }
  const { icon, text, iconRight = false }: Props = $props();
</script>

<!--
@component
A fixed-width icon with accompanying text.
-->
<div class="flex min-w-0 items-center gap-[0.5em]">
  {#if iconRight}
    <span class="min-w-0 truncate">{text}</span>
  {/if}
  <span class="flex w-[1em] flex-row justify-center">
    <Fa {icon} />
  </span>
  {#if !iconRight}
    <span class="min-w-0 truncate">{text}</span>
  {/if}
</div>
