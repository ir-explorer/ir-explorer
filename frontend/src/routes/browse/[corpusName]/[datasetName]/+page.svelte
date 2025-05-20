<script lang="ts">
  import { page } from "$app/state";
  import PaginatedList from "$lib/components/browse/PaginatedList.svelte";
  import { documentIcon, queryIcon } from "$lib/icons";
  import type { Paginated, Query, RelevantDocument } from "$lib/types";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();

  // query list
  async function getQueriesPage(num_items: number, offset: number) {
    const searchParams = new URLSearchParams({
      corpus_name: page.params.corpusName,
      dataset_name: page.params.datasetName,
      num_results: num_items.toString(),
      offset: offset.toString(),
    });
    const res = await fetch("/api/queries?" + searchParams);
    return (await res.json()) as Paginated<Query>;
  }

  // relevant document list
  async function getDocumentsPage(num_items: number, offset: number) {
    const searchParams = new URLSearchParams({
      query_id: data.query !== null ? data.query.id : "",
      dataset_name: page.params.datasetName,
      corpus_name: page.params.corpusName,
      num_results: num_items.toString(),
      offset: offset.toString(),
    });
    const res = await fetch("/api/relevant_documents?" + searchParams);
    return (await res.json()) as Paginated<RelevantDocument>;
  }
</script>

{#if data.query !== null}
  <div class="collapse mb-4 border border-base-300 bg-base-200">
    <input type="checkbox" checked />
    <div class="collapse-title flex flex-row items-center gap-2">
      <Fa icon={queryIcon} />
      {data.query.id}
    </div>
    <div class="collapse-content text-sm">
      {data.query.text}
    </div>
  </div>

  {#if data.query.num_relevant_documents > 0}
    <PaginatedList
      getPage={getDocumentsPage}
      getTargetLink={(d: RelevantDocument) =>
        `/browse/${page.params.corpusName}?${new URLSearchParams({ document_id: d.id })}`}
      itemsPerPage={10}>
      {#snippet head()}
        <p class="flex flex-row items-center gap-2">
          <Fa icon={documentIcon} />Relevant documents
        </p>
      {/snippet}
      {#snippet item(d: RelevantDocument)}
        <div class="flex flex-col gap-2">
          <div class="flex gap-2">
            <p class="badge badge-primary">ID: {d.id}</p>
            <p class="badge badge-secondary">Relevance: {d.relevance}</p>
          </div>
          <p>{d.snippet}</p>
        </div>
      {/snippet}
    </PaginatedList>
  {/if}
{:else}
  <PaginatedList
    getPage={getQueriesPage}
    getTargetLink={(q: Query) =>
      `/browse/${page.params.corpusName}/${page.params.datasetName}?${new URLSearchParams({ query_id: q.id })}`}
    itemsPerPage={10}>
    {#snippet head()}
      <p class="flex flex-row items-center gap-2">
        <Fa icon={queryIcon} />Queries
      </p>
    {/snippet}
    {#snippet item(q: Query)}
      <div class="flex flex-col gap-2">
        <div class="flex gap-2">
          <p class="badge badge-primary">ID: {q.id}</p>
          {#if q.num_relevant_documents > 0}
            <p class="badge badge-secondary">
              {q.num_relevant_documents} relevant
              {q.num_relevant_documents == 1 ? "document" : "documents"}
            </p>
          {/if}
        </div>
        <p>{q.text}</p>
      </div>
    {/snippet}
  </PaginatedList>
{/if}
