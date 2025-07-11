<script lang="ts">
  import { page } from "$app/state";
  import CardGrid from "$lib/components/browse/CardGrid.svelte";
  import PaginatedList from "$lib/components/browse/PaginatedList.svelte";
  import SizeIndicator from "$lib/components/browse/SizeIndicator.svelte";
  import { corpusIcon, datasetIcon, documentIcon, queryIcon } from "$lib/icons";
  import { selectedOptions } from "$lib/options.svelte";
  import type {
    Dataset,
    Document,
    OrderByOption,
    Paginated,
    RelevantQuery,
  } from "$lib/types";
  import { truncate } from "$lib/util";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  const { data }: PageProps = $props();

  // document list
  async function getDocumentsPage(
    match: string | null,
    orderBy: string | null,
    desc: boolean,
    numItems: number,
    offset: number,
  ) {
    const searchParams = new URLSearchParams({
      corpusName: page.params.corpusName,
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

  // relevent queries list
  async function getQueriesPage(
    match: string | null,
    orderBy: string | null,
    desc: boolean,
    numItems: number,
    offset: number,
  ) {
    const searchParams = new URLSearchParams({
      corpusName: page.params.corpusName,
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

{#if data.document !== null}
  <!-- display selected document -->
  <div class="collapse border border-base-300 bg-base-200">
    <input type="checkbox" checked />
    <div class="collapse-title flex flex-row items-center gap-2">
      <Fa icon={documentIcon} />
      {data.document.id}
    </div>
    <div class="collapse-content text-sm">
      {data.document.text}
    </div>
  </div>

  {#if data.document.numRelevantQueries > 0}
    <!-- display relevant queries for selected document -->
    <PaginatedList
      getPage={getQueriesPage}
      getTargetLink={(q: RelevantQuery) =>
        `/browse/${page.params.corpusName}/${q.datasetName}?queryId=${q.id}`}
      orderByOptions={orderRelevantQueriesOptions}>
      {#snippet headTitle()}
        <p class="flex flex-row items-center gap-2">
          <Fa icon={queryIcon} />Relevant queries
        </p>
      {/snippet}
      {#snippet item(q: RelevantQuery)}
        <div class="flex flex-col gap-2">
          <p>{truncate(q.snippet, selectedOptions.snippetLength)}</p>
          <div class="flex gap-2 font-bold">
            <p class="badge badge-sm badge-primary">ID: {q.id}</p>
            <p class="badge badge-sm badge-secondary">
              relevance: {q.relevance}
            </p>
          </div>
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
      gridItems={data.datasetList.sort((a, b) => b.numQueries - a.numQueries)}
      getTargetLink={(d: Dataset) =>
        `/browse/${page.params.corpusName}/${d.name}`}>
      {#snippet item(d: Dataset)}
        <div class="flex items-center justify-between gap-4">
          <div class="flex flex-col gap-2">
            <p class="flex items-center gap-2 text-sm font-thin">
              <Fa icon={corpusIcon} />
              {d.corpusName}
            </p>
            <p class="flex items-center gap-2 text-lg">
              <Fa icon={datasetIcon} />
              {d.name}
            </p>
          </div>
          <SizeIndicator
            value={d.numQueries}
            total={totalNumQueries}
            desc={"queries"} />
        </div>
      {/snippet}
    </CardGrid>
  {/if}

  <!-- display document list -->
  <PaginatedList
    getPage={getDocumentsPage}
    getTargetLink={(d: Document) =>
      `/browse/${page.params.corpusName}?documentId=${d.id}`}
    orderByOptions={orderDocumentsOptions}
    goToTarget={`/browse/${page.params.corpusName}`}
    goToName="documentId">
    {#snippet headTitle()}
      <p class="flex flex-row items-center gap-2">
        <Fa icon={documentIcon} />Documents
      </p>
    {/snippet}

    {#snippet item(d: Document)}
      <div class="flex flex-col gap-2">
        {#if d.title !== null}
          <p class="font-bold">
            {truncate(d.title, selectedOptions.snippetLength)}
          </p>
        {/if}
        <p>{truncate(d.text, selectedOptions.snippetLength)}</p>
        <div class="flex gap-2 font-bold">
          <p class="badge badge-sm badge-primary">ID: {d.id}</p>
          {#if d.numRelevantQueries > 0}
            <p class="badge badge-sm badge-secondary">
              {d.numRelevantQueries}
              {d.numRelevantQueries == 1 ? "query" : "queries"}
            </p>
          {/if}
        </div>
      </div>
    {/snippet}
  </PaginatedList>
{/if}
