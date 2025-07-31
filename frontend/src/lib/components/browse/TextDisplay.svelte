<script lang="ts">
  import { PUBLIC_MIN_DOCUMENT_LENGTH_SUMMARY } from "$env/static/public";
  import { summaryIcon, textIcon } from "$lib/icons";
  import { selectedOptions } from "$lib/options.svelte";
  import IconWithText from "../IconWithText.svelte";

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
<div class="tabs-border tabs text-sm">
  <label class="tab flex flex-row gap-2">
    <input type="radio" name="tabs-text" checked={true} />
    <IconWithText icon={textIcon} text={title} />
  </label>
  <div class="tab-content rounded rounded-box border-base-300 p-4 shadow">
    <div
      class="max-h-128 overflow-y-scroll leading-relaxed whitespace-pre-wrap">
      {text}
    </div>
  </div>

  {#if getSummary !== null && text.length >= Number(PUBLIC_MIN_DOCUMENT_LENGTH_SUMMARY) && selectedOptions.modelName !== null}
    <label class="tab flex flex-row gap-2">
      <input
        type="radio"
        name="tabs-text"
        onclick={async () => {
          await loadSummary();
        }} />
      <div
        class={[
          summaryBusy && // hacky way of replacing the icon (inside the span)
            "[&_div_span]:loading [&_div_span]:loading-xs [&_div_span]:loading-ball",
        ]}>
        <IconWithText icon={summaryIcon} text="Summary" />
      </div>
    </label>
    <div class="tab-content rounded rounded-box border-base-300 p-4 shadow">
      <div
        class="max-h-128 overflow-y-scroll leading-relaxed whitespace-pre-wrap">
        {summary}
        {#if summaryBusy}
          <div class="inline-block animate-blink font-bold text-primary">_</div>
        {/if}
      </div>
    </div>
  {/if}
</div>
