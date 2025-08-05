<script lang="ts">
  import { afterNavigate } from "$app/navigation";
  import { page } from "$app/state";
  import { PUBLIC_MAX_SEARCH_RESULT_PAGES } from "$env/static/public";
  import Alert from "$lib/components/Alert.svelte";
  import BlinkingCursor from "$lib/components/BlinkingCursor.svelte";
  import IconWithText from "$lib/components/IconWithText.svelte";
  import {
    corpusIcon,
    documentIcon,
    nextPageIcon,
    prevPageIcon,
    ragIcon,
  } from "$lib/icons";
  import { selectedOptions } from "$lib/options.svelte";
  import { toHumanReadable } from "$lib/util";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();
  let corpusNames = $derived(page.url.searchParams.getAll("corpus"));

  let generatedAnswer = $state("");
  let answerGenerationStarted = $state(false);
  let answerGenerationBusy = $state(false);

  async function generateAnswer() {
    answerGenerationStarted = true;
    answerGenerationBusy = true;
    if (data.result.items.length == 0 || selectedOptions.modelName === null) {
      throw new Error("Failed to generate answer.");
    }

    const searchParams = new URLSearchParams({
      q: data.q,
      modelName: selectedOptions.modelName,
    });
    for (const hit of data.result.items.slice(
      0,
      selectedOptions.numRagDocuments,
    )) {
      searchParams.append("corpusName", hit.corpusName);
      searchParams.append("documentId", hit.id);
    }
    const res = await fetch("/api/rag?" + searchParams);

    if (res.body === null) {
      return;
    }

    const textStream = res.body.pipeThrough(new TextDecoderStream());
    const reader = textStream.getReader();

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }
      generatedAnswer += value;
    }
    answerGenerationBusy = false;
  }

  afterNavigate(() => {
    generatedAnswer = "";
    answerGenerationStarted = false;
    answerGenerationBusy = false;
  });
</script>

{#if answerGenerationStarted}
  <div
    class="m-4 max-h-128 rounded border border-secondary bg-secondary/10 p-2 text-sm shadow">
    <div class="overflow-y-scroll leading-relaxed whitespace-pre-wrap">
      {generatedAnswer}
      {#if answerGenerationBusy}
        <BlinkingCursor />
      {/if}
    </div>
  </div>
{/if}

{#if data.result.totalNumItems == 0}
  <Alert text={"No results found."} />
{:else}
  <ul class="list">
    <li
      class="list-row flex w-full flex-row items-end justify-between px-4 py-2 text-xs">
      <p>
        <span>
          {toHumanReadable(data.result.totalNumItems)} results for query
          <i><b>{page.url.searchParams.get("q")}</b></i>
        </span>{#if corpusNames.length > 0}<span>
            &nbsp;(corpora: {corpusNames.join(", ")})</span
          >{/if}.
      </p>
      <!-- RAG button only appears on page 1 -->
      {#if data.pageNum == 1 && selectedOptions.modelName !== null && !answerGenerationStarted}
        <p class="tooltip tooltip-left" data-tip="Generate answer">
          <button
            onclick={generateAnswer}
            class="btn btn-square animate-shake btn-sm btn-primary hover:animate-none">
            <Fa icon={ragIcon} />
          </button>
        </p>
      {/if}
    </li>

    {#each data.result.items as hit, index}
      <li class="list-row">
        <div class="flex flex-col gap-2">
          <div class="flex flex-col gap-2">
            <p
              class="tooltip tooltip-right badge badge-soft tooltip-secondary badge-secondary"
              data-tip="Score: {hit.score}">
              #<span class="-ml-1 font-bold">
                {data.result.offset + index + 1}
              </span>
            </p>
            <a href="/browse/{hit.corpusName}?documentId={hit.id}">
              <div class="join max-w-full overflow-auto text-nowrap">
                <div class="join-item badge">
                  <IconWithText icon={documentIcon} text={hit.id} />
                </div>
                <div class="join-item badge">
                  <IconWithText icon={corpusIcon} text={hit.corpusName} />
                </div>
              </div>
            </a>
          </div>
          <p>{@html hit.snippet}</p>
        </div>
      </li>
    {/each}

    {#if data.totalPages > 1}
      <li class="list-row flex w-full justify-center">
        <div class="join">
          {#if data.prevPageLink != null}
            <a
              href={data.prevPageLink}
              class="btn join-item btn-sm btn-primary">
              <Fa icon={prevPageIcon} />
            </a>
          {/if}
          <div
            class="join-item flex items-center border border-base-300 bg-base-200 px-4">
            <p class="text-sm">
              Page {data.pageNum} of {toHumanReadable(data.totalPages)}
            </p>
          </div>
          {#if data.pageNum == Number(PUBLIC_MAX_SEARCH_RESULT_PAGES)}
            <div
              class="tooltip tooltip-info"
              data-tip="Only {PUBLIC_MAX_SEARCH_RESULT_PAGES} pages are shown.">
              <btn disabled class="btn join-item btn-sm btn-primary">
                <Fa icon={nextPageIcon} />
              </btn>
            </div>
          {:else if data.nextPageLink != null}
            <a
              href={data.nextPageLink}
              class="btn join-item btn-sm btn-primary">
              <Fa icon={nextPageIcon} />
            </a>
          {/if}
        </div>
      </li>
    {/if}
  </ul>
{/if}
