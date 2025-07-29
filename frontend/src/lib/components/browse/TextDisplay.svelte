<script lang="ts">
  import { textIcon } from "$lib/icons";
  import Fa from "svelte-fa";
  interface Props {
    /** The title to render. */
    title?: string;
    /** The text to render. */
    text: string;
  }

  let { title = "Text", text }: Props = $props();
</script>

<!--
@component
Display a query or document text in a scrollable component.
-->
<div class="tabs-border tabs">
  <label class="tab flex flex-row gap-2">
    <input type="radio" name="tabs-text" checked={true} />
    <Fa icon={textIcon} />
    {title}
  </label>
  <div
    class="tab-content rounded rounded-box border-base-300 p-4 text-sm shadow">
    <div
      class="max-h-128 overflow-y-scroll leading-relaxed whitespace-pre-wrap">
      {text}
    </div>
  </div>
</div>
