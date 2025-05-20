<script lang="ts">
  import { page } from "$app/state";
  import CardGrid from "$lib/components/browse/CardGrid.svelte";
  import PaginatedList from "$lib/components/browse/PaginatedList.svelte";
  import SizeIndicator from "$lib/components/browse/SizeIndicator.svelte";
  import { corpusIcon, datasetIcon, documentIcon, queryIcon } from "$lib/icons";
  import type { Dataset, Document, Paginated, RelevantQuery } from "$lib/types";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  const { data }: PageProps = $props();

  // document list
  async function getDocumentsPage(num_items: number, offset: number) {
    const searchParams = new URLSearchParams({
      corpus_name: page.params.corpusName,
      num_results: num_items.toString(),
      offset: offset.toString(),
    });
    const res = await fetch("/api/documents?" + searchParams);
    return (await res.json()) as Paginated<Document>;
  }

  // relevent queries list
  async function getQueriesPage(num_items: number, offset: number) {
    const searchParams = new URLSearchParams({
      corpus_name: page.params.corpusName,
      document_id: data.document !== null ? data.document.id : "",
      num_results: num_items.toString(),
      offset: offset.toString(),
    });
    const res = await fetch("/api/relevant_queries?" + searchParams);
    return (await res.json()) as Paginated<RelevantQuery>;
  }
</script>

{#if data.document !== null}
  <div class="collapse mb-4 border border-base-300 bg-base-200">
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
    <PaginatedList
      getPage={getQueriesPage}
      getTargetLink={(q: RelevantQuery) =>
        `/browse/${page.params.corpusName}/${q.dataset_name}?query_id=${q.id}`}
      itemsPerPage={10}>
      {#snippet head()}
        <p class="flex flex-row items-center gap-2">
          <Fa icon={queryIcon} />Relevant queries
        </p>
      {/snippet}
      {#snippet item(q: RelevantQuery)}
        <div class="flex flex-col gap-2">
          <div class="flex gap-2">
            <p class="badge badge-primary">ID: {q.id}</p>
            <p class="badge badge-secondary">Relevance: {q.relevance}</p>
          </div>
          <p>{q.snippet}</p>
        </div>
      {/snippet}
    </PaginatedList>
  {/if}
{:else}
  {#if data.datasetList !== null}
    {@const totalNumQueries = data.datasetList.reduce(
      (acc, dataset) => acc + dataset.num_queries_estimate,
      0,
    )}
    <CardGrid
      gridItems={data.datasetList.sort(
        (a, b) => b.num_queries_estimate - a.num_queries_estimate,
      )}
      getTargetLink={(d: Dataset) =>
        `/browse/${page.params.corpusName}/${d.name}`}>
      {#snippet item(d: Dataset)}
        {@const fraction = d.num_queries_estimate / totalNumQueries}
        <div class="flex items-center justify-between">
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
            value={d.num_queries_estimate}
            total={totalNumQueries}
            desc={"queries"}
            isEstimate />
        </div>
      {/snippet}
    </CardGrid>
  {/if}

  <PaginatedList
    getPage={getDocumentsPage}
    getTargetLink={(d: Document) =>
      `/browse/${page.params.corpusName}?document_id=${d.id}`}
    itemsPerPage={10}>
    {#snippet head()}
      <p class="flex flex-row items-center gap-2">
        <Fa icon={documentIcon} />Documents
      </p>
    {/snippet}

    {#snippet item(d: Document)}
      <div class="flex flex-col gap-2">
        <div class="flex gap-2">
          <p class="badge badge-primary">ID: {d.id}</p>
          {#if d.num_relevant_queries > 0}
            <p class="badge badge-secondary">
              Relevant for {d.num_relevant_queries}
              {d.num_relevant_queries == 1 ? "query" : "queries"}
            </p>
          {/if}
        </div>
        {#if d.title !== null}
          <p class="font-bold">{d.title}</p>
        {/if}
        <p>{d.text}</p>
      </div>
    {/snippet}
  </PaginatedList>
{/if}
