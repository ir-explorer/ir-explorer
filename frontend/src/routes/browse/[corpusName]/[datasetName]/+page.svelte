<script lang="ts">
  import { page } from "$app/state";
  import Alert from "$lib/components/Alert.svelte";
  import MetaDisplay from "$lib/components/browse/MetaDisplay.svelte";
  import PaginatedList from "$lib/components/browse/PaginatedList.svelte";
  import TextDisplay from "$lib/components/browse/TextDisplay.svelte";
  import { relevanceIcon } from "$lib/icons";
  import { selectedOptions } from "$lib/options.svelte";
  import type {
    OrderByOption,
    Paginated,
    Query,
    RelevantDocument,
  } from "$lib/types";
  import { truncate } from "$lib/util";
  import Fa from "svelte-fa";
  import { SvelteURLSearchParams } from "svelte/reactivity";
  import type { PageProps } from "./$types";

  const { data }: PageProps = $props();

  // query list
  async function getQueriesPage(
    match: string | null,
    orderBy: string | null,
    desc: boolean,
    numItems: number,
    offset: number,
  ) {
    const searchParams = new SvelteURLSearchParams({
      corpusName: String(page.params.corpusName),
      datasetName: String(page.params.datasetName),
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

    const res = await fetch("/api/queries?" + searchParams);
    return (await res.json()) as Paginated<Query>;
  }
  const orderQueriesOptions = [
    { name: "Relevant documents", option: "relevant_documents" },
    { name: "Length", option: "length" },
    { name: "Match", option: "match_score" },
  ] as OrderByOption[];

  // relevant document list
  async function getDocumentsPage(
    match: string | null,
    orderBy: string | null,
    desc: boolean,
    numItems: number,
    offset: number,
  ) {
    const searchParams = new SvelteURLSearchParams({
      queryId: data.query !== null ? data.query.id : "",
      datasetName: String(page.params.datasetName),
      corpusName: String(page.params.corpusName),
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

    const res = await fetch("/api/relevantDocuments?" + searchParams);
    return (await res.json()) as Paginated<RelevantDocument>;
  }
  const orderRelevantDocumentsOptions = [
    { name: "Relevance", option: "relevance" },
    { name: "Length", option: "document_length" },
    { name: "Match", option: "document_match_score" },
  ] as OrderByOption[];
</script>

{#if page.url.searchParams.get("queryId") !== null && data.query === null}
  <Alert text="Query not found." />
{:else if data.query !== null}
  <!-- display selected query -->
  <MetaDisplay
    items={new Map([
      ["Corpus", data.query.corpusName],
      ["Dataset", data.query.datasetName],
      ["Query ID", data.query.id],
      ["Description", data.query.description],
      [
        "Number of relevant documents",
        data.query.numRelevantDocuments.toString(),
      ],
    ])} />
  <TextDisplay text={data.query.text} title="Text" />

  {#if data.query.numRelevantDocuments > 0}
    <!-- display relevant documents for selected query -->
    <PaginatedList
      getPage={getDocumentsPage}
      getTargetLink={(d: RelevantDocument) =>
        `/browse/${page.params.corpusName}?${new URLSearchParams({ documentId: d.id })}` as const}
      orderByOptions={orderRelevantDocumentsOptions}>
      {#snippet headTitle()}
        <p class="my-auto">Relevant documents</p>
      {/snippet}
      {#snippet item(d: RelevantDocument)}
        <div class="min-w-0">
          <div class="flex min-w-0 items-center gap-x-3">
            <p class="min-w-0 text-sm leading-5 font-medium text-secondary">
              {d.id}
            </p>
            <p
              class="flex shrink-0 items-center gap-1 text-xs text-base-content/60">
              <span class="text-success"><Fa icon={relevanceIcon} /></span>
              {d.relevance}
            </p>
          </div>
          <p class="mt-1 text-sm">
            {truncate(d.text, selectedOptions.snippetLength)}
          </p>
        </div>
      {/snippet}
    </PaginatedList>
  {/if}
{:else}
  <!-- display query list -->
  <PaginatedList
    getPage={getQueriesPage}
    getTargetLink={(q: Query) =>
      `/browse/${page.params.corpusName}/${page.params.datasetName}?${new URLSearchParams({ queryId: q.id })}` as const}
    orderByOptions={orderQueriesOptions}
    goToTarget={`/browse/${page.params.corpusName}/${page.params.datasetName}`}
    goToName="queryId">
    {#snippet headTitle()}
      <p class="my-auto">Queries</p>
    {/snippet}
    {#snippet item(q: Query)}
      <div class="min-w-0">
        <p class="text-sm font-medium text-secondary">
          {q.id}
        </p>
        {#if q.numRelevantDocuments > 0}
          <p class="text-xs text-base-content/60">
            {q.numRelevantDocuments} relevant documents
          </p>
        {/if}
        <p class="mt-1 text-sm">
          {truncate(q.text, selectedOptions.snippetLength)}
        </p>
      </div>
    {/snippet}
  </PaginatedList>
{/if}
