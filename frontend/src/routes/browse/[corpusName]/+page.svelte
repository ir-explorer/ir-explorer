<script lang="ts">
  import type { PageProps } from "./$types";
  import List from "$lib/components/browse/List.svelte";
  import Fa from "svelte-fa";
  import { datasetIcon, documentIcon } from "$lib/icons";
  import type { Dataset } from "$lib/types";
  import { page } from "$app/state";

  let { data }: PageProps = $props();

  const getTargetLink = (d: Dataset) =>
    `/browse/${page.params.corpusName}/${d.name}`;
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
{/if}

{#if data.datasetList !== null}
  <List listItems={data.datasetList} {getTargetLink}>
    {#snippet head()}
      <p class="flex flex-row items-center gap-2">
        <Fa icon={datasetIcon} />Datasets
      </p>
    {/snippet}
    {#snippet item(d: Dataset)}
      {d.name} ({d.num_queries_estimate} queries)
    {/snippet}
  </List>
{/if}
