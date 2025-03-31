<script lang="ts">
  import type { PageProps } from "./$types";
  import List from "$lib/components/browse/List.svelte";
  import Fa from "svelte-fa";
  import { datasetIcon, documentIcon } from "$lib/icons";
  import type { Dataset } from "$lib/types";

  let { data }: PageProps = $props();
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

<List listItems={data.datasetList}>
  {#snippet head()}
    <p class="flex flex-row items-center gap-2">
      <Fa icon={datasetIcon} /> Datasets
    </p>
  {/snippet}
  {#snippet item(d: Dataset)}
    {d.name}
  {/snippet}
</List>
