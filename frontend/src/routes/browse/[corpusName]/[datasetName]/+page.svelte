<script lang="ts">
  import { page } from "$app/state";
  import PaginatedList from "$lib/components/browse/PaginatedList.svelte";
  import { documentIcon, queryIcon } from "$lib/icons";
  import type {
    OrderByOption,
    Paginated,
    Query,
    RelevantDocument,
  } from "$lib/types";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();

  // query list
  async function getQueriesPage(
    match: string | null,
    orderBy: string | null,
    desc: boolean,
    numItems: number,
    offset: number,
  ) {
    const searchParams = new URLSearchParams({
      corpusName: page.params.corpusName,
      datasetName: page.params.datasetName,
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
    const searchParams = new URLSearchParams({
      queryId: data.query !== null ? data.query.id : "",
      datasetName: page.params.datasetName,
      corpusName: page.params.corpusName,
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

{#if data.query !== null}
  <!-- display selected query -->
  <div class="collapse border border-base-300 bg-base-200">
    <input type="checkbox" checked />
    <div class="collapse-title flex flex-row items-center gap-2">
      <Fa icon={queryIcon} />
      {data.query.id}
    </div>
    <div class="collapse-content text-sm">
      {data.query.text}
    </div>
  </div>

  {#if data.query.numRelevantDocuments > 0}
    <!-- display relevant documents for selected query -->
    <PaginatedList
      getPage={getDocumentsPage}
      getTargetLink={(d: RelevantDocument) =>
        `/browse/${page.params.corpusName}?${new URLSearchParams({ documentId: d.id })}`}
      orderByOptions={orderRelevantDocumentsOptions}>
      {#snippet headTitle()}
        <p class="flex flex-row items-center gap-2">
          <Fa icon={documentIcon} />Relevant documents
        </p>
      {/snippet}
      {#snippet item(d: RelevantDocument)}
        <div class="flex flex-col gap-2">
          <p>{d.snippet}</p>
          <div class="flex gap-2 font-bold">
            <p class="badge badge-sm badge-primary">ID: {d.id}</p>
            <p class="badge badge-sm badge-secondary">
              relevance: {d.relevance}
            </p>
          </div>
        </div>
      {/snippet}
    </PaginatedList>
  {/if}
{:else}
  <!-- display query list -->
  <PaginatedList
    getPage={getQueriesPage}
    getTargetLink={(q: Query) =>
      `/browse/${page.params.corpusName}/${page.params.datasetName}?${new URLSearchParams({ queryId: q.id })}`}
    orderByOptions={orderQueriesOptions}
    goToTarget={`/browse/${page.params.corpusName}/${page.params.datasetName}`}
    goToName="queryId">
    {#snippet headTitle()}
      <p class="flex flex-row items-center gap-2">
        <Fa icon={queryIcon} />Queries
      </p>
    {/snippet}
    {#snippet item(q: Query)}
      <div class="flex flex-col gap-2">
        <p>{q.text}</p>
        <div class="flex gap-2 font-bold">
          <p class="badge badge-sm badge-primary">ID: {q.id}</p>
          {#if q.numRelevantDocuments > 0}
            <p class="badge badge-sm badge-secondary">
              {q.numRelevantDocuments}
              {q.numRelevantDocuments == 1 ? "document" : "documents"}
            </p>
          {/if}
        </div>
      </div>
    {/snippet}
  </PaginatedList>
{/if}
