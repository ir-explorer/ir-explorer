<script lang="ts">
  import type { PageProps } from "./$types";
  import List from "$lib/components/browse/List.svelte";
  import Fa from "svelte-fa";
  import { queryIcon } from "$lib/icons";
  import type { Query } from "$lib/types";

  let { data }: PageProps = $props();
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

{#if data.queryList.length > 0}
  <List listItems={data.queryList}>
    {#snippet head()}
      <p class="flex flex-row items-center gap-2">
        <Fa icon={queryIcon} /> Queries
      </p>
    {/snippet}
    {#snippet item(q: Query)}
      {q.id}
    {/snippet}
  </List>
{/if}
