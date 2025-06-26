<script lang="ts">
  import { page } from "$app/state";
  import CardGrid from "$lib/components/browse/CardGrid.svelte";
  import PaginatedList from "$lib/components/browse/PaginatedList.svelte";
  import SizeIndicator from "$lib/components/browse/SizeIndicator.svelte";
  import { corpusIcon, datasetIcon, documentIcon, queryIcon } from "$lib/icons";
  import type {
    Dataset,
    Document,
    OrderByOption,
    Paginated,
    RelevantQuery,
  } from "$lib/types";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  const { data }: PageProps = $props();

  // document list
  async function getDocumentsPage(
    match: string | null,
    order_by: string | null,
    desc: boolean,
    num_items: number,
    offset: number,
  ) {
    const searchParams = new URLSearchParams({
      corpus_name: page.params.corpusName,
      desc: desc.toString(),
      num_results: num_items.toString(),
      offset: offset.toString(),
    });
    if (match !== null) {
      searchParams.append("match", match);
    }
    if (order_by !== null) {
      searchParams.append("order_by", order_by);
    }

    const res = await fetch("/api/documents?" + searchParams);
    return (await res.json()) as Paginated<Document>;
  }
  const orderDocumentsOptions = [
    { name: "Relevant queries", option: "relevant_queries" },
    { name: "Length", option: "length" },
    { name: "Filter", option: "match_score" },
  ] as OrderByOption[];

  // relevent queries list
  async function getQueriesPage(
    match: string | null,
    order_by: string | null,
    desc: boolean,
    num_items: number,
    offset: number,
  ) {
    const searchParams = new URLSearchParams({
      corpus_name: page.params.corpusName,
      document_id: data.document !== null ? data.document.id : "",
      num_results: num_items.toString(),
      offset: offset.toString(),
      desc: desc.toString(),
    });
    if (match !== null) {
      searchParams.append("match", match);
    }
    if (order_by !== null) {
      searchParams.append("order_by", order_by);
    }

    const res = await fetch("/api/relevant_queries?" + searchParams);
    return (await res.json()) as Paginated<RelevantQuery>;
  }
  const orderRelevantQueriesOptions = [
    { name: "Relevance", option: "relevance" },
    { name: "Length", option: "query_length" },
    { name: "Filter", option: "query_match_score" },
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

  {#if data.document.num_relevant_queries > 0}
    <!-- display relevant queries for selected document -->
    <PaginatedList
      getPage={getQueriesPage}
      getTargetLink={(q: RelevantQuery) =>
        `/browse/${page.params.corpusName}/${q.dataset_name}?query_id=${q.id}`}
      itemsPerPage={10}
      orderByOptions={orderRelevantQueriesOptions}>
      {#snippet head()}
        <p class="flex flex-row items-center gap-2">
          <Fa icon={queryIcon} />Relevant queries
        </p>
      {/snippet}
      {#snippet item(q: RelevantQuery)}
        <div class="flex flex-col gap-2">
          <p>{q.snippet}</p>
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
      (acc, dataset) => acc + dataset.num_queries,
      0,
    )}
    <CardGrid
      gridItems={data.datasetList.sort((a, b) => b.num_queries - a.num_queries)}
      getTargetLink={(d: Dataset) =>
        `/browse/${page.params.corpusName}/${d.name}`}>
      {#snippet item(d: Dataset)}
        {@const fraction = d.num_queries / totalNumQueries}
        <div class="flex items-center justify-between gap-4">
          <div class="flex flex-col gap-2">
            <p class="flex items-center gap-2 text-sm font-thin">
              <Fa icon={corpusIcon} />
              {d.corpus_name}
            </p>
            <p class="flex items-center gap-2 text-lg">
              <Fa icon={datasetIcon} />
              {d.name}
            </p>
          </div>
          <SizeIndicator
            value={d.num_queries}
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
      `/browse/${page.params.corpusName}?document_id=${d.id}`}
    itemsPerPage={10}
    orderByOptions={orderDocumentsOptions}>
    {#snippet head()}
      <p class="flex flex-row items-center gap-2">
        <Fa icon={documentIcon} />Documents
      </p>
    {/snippet}

    {#snippet item(d: Document)}
      <div class="flex flex-col gap-2">
        {#if d.title !== null}
          <p class="font-bold">{d.title}</p>
        {/if}
        {#if d.text.length > 500}
          <p>{d.text.substring(0, 500)}...</p>
        {:else}
          <p>{d.text}</p>
        {/if}
        <div class="flex gap-2 font-bold">
          <p class="badge badge-sm badge-primary">ID: {d.id}</p>
          {#if d.num_relevant_queries > 0}
            <p class="badge badge-sm badge-secondary">
              {d.num_relevant_queries}
              {d.num_relevant_queries == 1 ? "query" : "queries"}
            </p>
          {/if}
        </div>
      </div>
    {/snippet}
  </PaginatedList>
{/if}
