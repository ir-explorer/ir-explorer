<script lang="ts">
  import type { PageProps } from "./$types";
  import PaginatedList from "$lib/components/browse/PaginatedList.svelte";
  import CardGrid from "$lib/components/browse/CardGrid.svelte";
  import Fa from "svelte-fa";
  import { corpusIcon, datasetIcon, documentIcon } from "$lib/icons";
  import type { Dataset, Paginated, Document, RelevantQuery } from "$lib/types";
  import { page } from "$app/state";

  let { data }: PageProps = $props();

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

  <div class="divider"></div>

  <PaginatedList
    getPage={getQueriesPage}
    getTargetLink={(q: RelevantQuery) =>
      `/browse/${page.params.corpusName}/${q.dataset_name}?query_id=${q.id}`}
    itemsPerPage={10}>
    {#snippet head()}
      <p class="flex flex-row items-center gap-2">
        <Fa icon={documentIcon} />Relevant queries
      </p>
    {/snippet}
    {#snippet item(q: RelevantQuery)}
      {q.id} (relevance: {q.relevance})
    {/snippet}
  </PaginatedList>
{:else}
  {#if data.datasetList !== null}
    <CardGrid
      gridItems={data.datasetList}
      getTargetLink={(d: Dataset) =>
        `/browse/${page.params.corpusName}/${d.name}`}>
      {#snippet item(d: Dataset)}
        <p class="flex items-center gap-2 text-sm font-thin">
          <Fa icon={corpusIcon} />
          {d.corpus_name}
        </p>
        <p class="flex items-center gap-2 text-lg">
          <Fa icon={datasetIcon} />
          {d.name}
        </p>
        <p>
          <span class="text-xl font-thin">{d.num_queries_estimate}</span> queries
        </p>
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
      {d.id} ({d.num_relevant_queries} relevant queries)
    {/snippet}
  </PaginatedList>
{/if}
