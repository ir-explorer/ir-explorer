<script lang="ts">
  import type { PageProps } from "./$types";
  import List from "$lib/components/browse/List.svelte";
  import type { Corpus } from "$lib/types";

  let { data }: PageProps = $props();
</script>

<List listItems={data.corpusList}>
  {#snippet head()}
    Corpora
  {/snippet}
  {#snippet item(c: Corpus)}
    {c.name} ({c.num_datasets} datasets, {c.num_documents_estimate} documents)
  {/snippet}
</List>
