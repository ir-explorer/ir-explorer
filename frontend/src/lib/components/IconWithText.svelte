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
    /** Use the wider icon slot. */
    wide?: boolean;
  }
  const { icon, text, iconRight = false, wide = false }: Props = $props();
</script>

<!--
@component
A fixed-width icon with accompanying text.
-->
<div class="flex items-center gap-2">
  {#if iconRight}
    {text}
  {/if}
  <span class={["flex flex-row justify-center", wide ? "w-6" : "w-4"]}>
    <Fa {icon} />
  </span>
  {#if !iconRight}
    {text}
  {/if}
</div>
