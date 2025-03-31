<script lang="ts">
  import type { PageProps } from "./$types";
  import List from "$lib/components/browse/List.svelte";
  import type { Query } from "$lib/types";

  let { data }: PageProps = $props();
</script>

<List listItems={data.queryList}>
  {#snippet head()}
    Queries
  {/snippet}
  {#snippet item(q: Query)}
    {q.id}
  {/snippet}
</List>
