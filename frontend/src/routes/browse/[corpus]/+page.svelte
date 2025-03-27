<script lang="ts">
  import type { PageProps } from "./$types";
  import List from "$lib/components/browse/List.svelte";
  import type { Dataset } from "$lib/types";

  let { data }: PageProps = $props();
</script>

<List listItems={data.datasetList}>
  {#snippet head()}
    Available datasets
  {/snippet}
  {#snippet item(d: Dataset)}
    {d.name}
  {/snippet}
</List>
