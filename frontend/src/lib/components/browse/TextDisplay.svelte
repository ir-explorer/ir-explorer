<script lang="ts">
  import { summaryIcon, textIcon } from "$lib/icons";
  import Fa from "svelte-fa";
  interface Props {
    /** The title to render. */
    title?: string;
    /** The text to render. */
    text: string;
    /** A function to generate a summary. */
    getSummary?: (() => Promise<ReadableStream<string>>) | null;
  }

  let { title = "Text", text, getSummary = null }: Props = $props();

  let summary = $state("");
  let summaryLoaded = false;
  let summaryBusy = $state(false);

  async function loadSummary() {
    if (!summaryLoaded && getSummary != null) {
      summaryLoaded = true;
      summaryBusy = true;

      const reader = (await getSummary()).getReader();
      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          summaryBusy = false;
          break;
        }
        summary += value;
      }
    }
  }
</script>

<!--
@component
Display a query or document text and (optionally) summary in scrollable components.
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

  {#if getSummary !== null}
    <label class="tab flex flex-row gap-2">
      <input
        type="radio"
        name="tabs-text"
        onclick={async () => {
          await loadSummary();
        }} />
      {#if summaryBusy}
        <span class="loading loading-xs loading-ball"></span>
      {:else}
        <Fa icon={summaryIcon} />
      {/if}
      Summary
    </label>
    <div
      class="tab-content rounded rounded-box border-base-300 p-4 text-sm shadow">
      <div
        class="max-h-128 overflow-y-scroll leading-relaxed whitespace-pre-wrap">
        {summary}
      </div>
    </div>
  {/if}
</div>
