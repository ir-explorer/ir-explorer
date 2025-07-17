<script lang="ts">
  import { infoIcon } from "$lib/icons";
  import type { IconDefinition } from "@fortawesome/free-solid-svg-icons";
  import Fa from "svelte-fa";

  interface Props {
    /** The icon to render. */
    icon?: IconDefinition;
    /** The text to display. */
    text: string;
  }
  const { icon = infoIcon, text }: Props = $props();
</script>

<!--
@component
A small alert message with an icon.
-->
<div class="alert-soft mx-auto alert w-fit">
  <span class="text-info">
    <Fa {icon} />
  </span>
  <span>{text}</span>
</div>
