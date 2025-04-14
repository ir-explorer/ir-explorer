<script lang="ts">
  import type { PageProps } from "./$types";
  import List from "$lib/components/browse/List.svelte";
  import type { Corpus } from "$lib/types";
  import Fa from "svelte-fa";
  import { corpusIcon } from "$lib/icons";

  let { data }: PageProps = $props();

  const getTargetLink = (c: Corpus) => `/browse/${c.name}`;
</script>

<List listItems={data.corpusList} {getTargetLink}>
  {#snippet head()}
    <div class="flex flex-row items-center gap-2">
      <Fa icon={corpusIcon} />Corpora
    </div>
  {/snippet}
  {#snippet item(c: Corpus)}
    {c.name} ({c.num_datasets} datasets, {c.num_documents_estimate} documents)
  {/snippet}
</List>
