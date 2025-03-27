<script lang="ts">
  import type { PageProps } from "./$types";
  import List from "$lib/components/browse/List.svelte";
  import type { Corpus } from "$lib/types";

  let { data }: PageProps = $props();
</script>

<List listItems={data.corpusList}>
  {#snippet head()}
    Available corpora
  {/snippet}
  {#snippet item(c: Corpus)}
    {c.name}
  {/snippet}
</List>
