<script lang="ts">
  import type { PageProps } from "./$types";
  import PaginatedList from "$lib/components/browse/PaginatedList.svelte";
  import List from "$lib/components/browse/List.svelte";
  import Fa from "svelte-fa";
  import { datasetIcon, documentIcon } from "$lib/icons";
  import type { Dataset, Paginated, Document } from "$lib/types";
  import { page } from "$app/state";

  let { data }: PageProps = $props();

  const getDatasetTargetLink = (d: Dataset) =>
    `/browse/${page.params.corpusName}/${d.name}`;

  const getDocumentTargetLink = (d: Document) =>
    `/browse/${page.params.corpusName}?document_id=${d.id}`;

  async function getDocumentPage(num_items: number, offset: number) {
    const searchParams = new URLSearchParams({
      corpus_name: page.params.corpusName,
      num_results: num_items.toString(),
      offset: offset.toString(),
    });

    const res = await fetch("/api/documents?" + searchParams);
    return (await res.json()) as Paginated<Document>;
  }
</script>

{#if data.document !== null}
  <div class="collapse mb-4 border border-base-300 bg-base-200">
    <input type="checkbox" checked />
    <div class="collapse-title flex flex-row items-center gap-2">
      <Fa icon={documentIcon} />
      {data.documentID}
    </div>
    <div class="collapse-content text-sm">
      {data.document.text}
    </div>
  </div>
{:else}
  {#if data.datasetList !== null}
    <List listItems={data.datasetList} getTargetLink={getDatasetTargetLink}>
      {#snippet head()}
        <p class="flex flex-row items-center gap-2">
          <Fa icon={datasetIcon} />Datasets
        </p>
      {/snippet}
      {#snippet item(d: Dataset)}
        {d.name} ({d.num_queries_estimate} queries)
      {/snippet}
    </List>

    <div class="divider"></div>
  {/if}

  <PaginatedList
    getPage={getDocumentPage}
    getTargetLink={getDocumentTargetLink}
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
