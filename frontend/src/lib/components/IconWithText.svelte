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
    /** Override fixed icon width. */
    iconWidth?: Number | null;
  }
  const { icon, text, iconRight = false, iconWidth = null }: Props = $props();

  const wClass = iconWidth === null ? "w-fit" : `w-${iconWidth}`;
</script>

<!--
@component
A fixed-width icon with accompanying text.
-->
<div class="flex items-center gap-2">
  {#if iconRight}
    {text}
  {/if}
  <span class="{wClass} flex flex-row justify-center">
    <Fa {icon} />
  </span>
  {#if !iconRight}
    {text}
  {/if}
</div>
