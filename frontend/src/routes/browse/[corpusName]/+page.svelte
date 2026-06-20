<script lang="ts">
  import { page } from "$app/state";
  import Alert from "$lib/components/Alert.svelte";
  import CardGrid from "$lib/components/browse/CardGrid.svelte";
  import MetaDisplay from "$lib/components/browse/MetaDisplay.svelte";
  import type { PaginatedListSnapshot } from "$lib/components/browse/PaginatedList.svelte";
  import PaginatedList from "$lib/components/browse/PaginatedList.svelte";
  import SizeIndicator from "$lib/components/browse/SizeIndicator.svelte";
  import TextDisplay from "$lib/components/browse/TextDisplay.svelte";
  import IconWithText from "$lib/components/IconWithText.svelte";
  import {
    datasetIcon,
    documentIcon,
    queryIcon,
    relevanceIcon,
  } from "$lib/icons";
  import { selectedOptions } from "$lib/options.svelte";
  import type {
    Dataset,
    Document,
    OrderByOption,
    Paginated,
    RelevantQuery,
  } from "$lib/types";
  import { truncate } from "$lib/util";
  import { SvelteURLSearchParams } from "svelte/reactivity";
  import type { PageProps, Snapshot } from "./$types";

  type PaginatedListHandle<T> = {
    capture: () => PaginatedListSnapshot<T>;
    restore: (snapshot: PaginatedListSnapshot<T>) => void;
  };

  const { data }: PageProps = $props();
  let documentList = $state<PaginatedListHandle<Document>>();
  let relevantQueryList = $state<PaginatedListHandle<RelevantQuery>>();

  export const snapshot: Snapshot = {
    capture: () => ({
      documentList: documentList?.capture(),
      relevantQueryList: relevantQueryList?.capture(),
    }),
    restore: (state) => {
      if (state.documentList) documentList?.restore(state.documentList);
      if (state.relevantQueryList) {
        relevantQueryList?.restore(state.relevantQueryList);
      }
    },
  };

  async function getDocumentSummary() {
    if (data.document === null || selectedOptions.modelName === null) {
      throw new Error("Failed to summarize document.");
    }

    const searchParams = new SvelteURLSearchParams({
      corpusName: String(page.params.corpusName),
      documentId: data.document.id,
      modelName: selectedOptions.modelName,
    });
    const res = await fetch("/api/documentSummary?" + searchParams);
    if (res.body === null) {
      return new ReadableStream();
    }
    return res.body.pipeThrough(new TextDecoderStream());
  }

  // document list
  async function getDocumentsPage(
    match: string | null,
    orderBy: string | null,
    desc: boolean,
    numItems: number,
    offset: number,
  ) {
    const searchParams = new SvelteURLSearchParams({
      corpusName: String(page.params.corpusName),
      desc: desc.toString(),
      numResults: numItems.toString(),
      offset: offset.toString(),
    });
    if (match !== null) {
      searchParams.append("match", match);
    }
    if (orderBy !== null) {
      searchParams.append("orderBy", orderBy);
    }

    const res = await fetch("/api/documents?" + searchParams);
    return (await res.json()) as Paginated<Document>;
  }
  const orderDocumentsOptions = [
    { name: "Relevant queries", option: "relevant_queries" },
    { name: "Length", option: "length" },
    { name: "Match", option: "match_score" },
  ] as OrderByOption[];

  // relevant queries list
  async function getQueriesPage(
    match: string | null,
    orderBy: string | null,
    desc: boolean,
    numItems: number,
    offset: number,
  ) {
    const searchParams = new SvelteURLSearchParams({
      corpusName: String(page.params.corpusName),
      documentId: data.document !== null ? data.document.id : "",
      numResults: numItems.toString(),
      offset: offset.toString(),
      desc: desc.toString(),
    });
    if (match !== null) {
      searchParams.append("match", match);
    }
    if (orderBy !== null) {
      searchParams.append("orderBy", orderBy);
    }

    const res = await fetch("/api/relevantQueries?" + searchParams);
    return (await res.json()) as Paginated<RelevantQuery>;
  }
  const orderRelevantQueriesOptions = [
    { name: "Relevance", option: "relevance" },
    { name: "Length", option: "query_length" },
    { name: "Match", option: "query_match_score" },
  ] as OrderByOption[];
</script>

{#if page.url.searchParams.get("documentId") !== null && data.document === null}
  <Alert text="Document not found." />
{:else if data.document !== null}
  <!-- display selected document -->
  <MetaDisplay
    items={new Map([
      ["Corpus", data.document.corpusName],
      ["Document ID", data.document.id],
      ["Title", data.document.title],
      ["Relevant queries", data.document.numRelevantQueries.toString()],
    ])} />
  <TextDisplay text={data.document.text} getSummary={getDocumentSummary} />

  {#if data.document.numRelevantQueries > 0}
    <!-- display relevant queries for selected document -->
    <PaginatedList
      bind:this={relevantQueryList}
      getPage={getQueriesPage}
      getTargetLink={(q: RelevantQuery) =>
        `/browse/${page.params.corpusName}/${q.datasetName}?queryId=${q.id}` as const}
      orderByOptions={orderRelevantQueriesOptions}
      matchDependentOrderByOptions={["query_match_score"]}>
      {#snippet headTitle()}
        <p class="my-auto">Relevant queries</p>
      {/snippet}
      {#snippet item(q: RelevantQuery)}
        <div class="min-w-0">
          <div class="flex min-w-0 items-center gap-x-3">
            <p class="min-w-0 text-sm font-medium text-secondary">
              <IconWithText icon={queryIcon} text={q.id} />
            </p>
            <p class="min-w-0 text-xs text-base-content/60">
              <IconWithText icon={datasetIcon} text={q.datasetName} />
            </p>
            <p class="shrink-0 text-xs text-base-content/60">
              <IconWithText
                icon={relevanceIcon}
                text={q.relevance.toString()} />
            </p>
          </div>
          <p class="mt-1 text-sm leading-relaxed">
            {truncate(q.text, selectedOptions.snippetLength)}
          </p>
        </div>
      {/snippet}
    </PaginatedList>
  {/if}
{:else}
  <!-- display datasets -->
  {#if data.datasetList !== null}
    {@const totalNumQueries = data.datasetList.reduce(
      (acc, dataset) => acc + dataset.numQueries,
      0,
    )}
    <CardGrid
      gridItems={data.datasetList}
      getTargetLink={(d: Dataset) =>
        `/browse/${page.params.corpusName}/${d.name}` as const}>
      {#snippet item(d: Dataset)}
        <div class="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3">
          <div class="min-w-0 text-lg">
            <IconWithText icon={datasetIcon} text={d.name} />
          </div>
          <SizeIndicator
            value={d.numQueries}
            total={totalNumQueries}
            desc="queries" />
        </div>
      {/snippet}
    </CardGrid>
  {/if}

  <!-- display document list -->
  <PaginatedList
    bind:this={documentList}
    getPage={getDocumentsPage}
    getTargetLink={(d: Document) =>
      `/browse/${page.params.corpusName}?documentId=${d.id}` as const}
    orderByOptions={orderDocumentsOptions}
    matchDependentOrderByOptions={["match_score"]}
    goToTarget={`/browse/${page.params.corpusName}`}
    goToName="documentId">
    {#snippet headTitle()}
      <p class="my-auto">Documents</p>
    {/snippet}

    {#snippet item(d: Document)}
      <div class="min-w-0">
        <div class="flex min-w-0 items-center gap-x-3">
          <p class="min-w-0 text-sm font-medium text-secondary">
            <IconWithText icon={documentIcon} text={d.id} />
          </p>
          {#if d.numRelevantQueries > 0}
            <p class="shrink-0 text-xs text-base-content/60">
              {d.numRelevantQueries}
              {d.numRelevantQueries === 1 ? "query" : "queries"}
            </p>
          {/if}
        </div>
        {#if d.title !== null}
          <p class="mt-1 font-bold">
            {truncate(d.title, selectedOptions.snippetLength)}
          </p>
        {/if}
        <p class="mt-1 text-sm">
          {truncate(d.text, selectedOptions.snippetLength)}
        </p>
      </div>
    {/snippet}
  </PaginatedList>
{/if}
