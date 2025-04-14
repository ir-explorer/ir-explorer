<script lang="ts">
  import type { PageProps } from "./$types";
  import List from "$lib/components/browse/List.svelte";
  import Fa from "svelte-fa";
  import { queryIcon } from "$lib/icons";
  import type { Query } from "$lib/types";
  import { page } from "$app/state";

  let { data }: PageProps = $props();

  const getTargetLink = (q: Query) =>
    `/browse/${page.params.corpusName}/${page.params.datasetName}?${new URLSearchParams({ query_id: q.id })}`;
</script>

{#if data.query !== null}
  <div class="collapse mb-4 border border-base-300 bg-base-200">
    <input type="checkbox" checked />
    <div class="collapse-title flex flex-row items-center gap-2">
      <Fa icon={queryIcon} />
      {data.queryID}
    </div>
    <div class="collapse-content text-sm">
      {data.query.text}
    </div>
  </div>
{/if}

{#if data.queryList !== null}
  <List listItems={data.queryList} {getTargetLink}>
    {#snippet head()}
      <p class="flex flex-row items-center gap-2">
        <Fa icon={queryIcon} />Queries
      </p>
    {/snippet}
    {#snippet item(q: Query)}
      {q.id} ({q.num_relevant_documents} relevant documents)
    {/snippet}
  </List>
{/if}
