<script lang="ts">
  import type { PageProps } from "./$types";
  import CardGrid from "$lib/components/browse/CardGrid.svelte";
  import type { Corpus } from "$lib/types";
  import Fa from "svelte-fa";
  import { toHumanReadable } from "$lib/util";
  import { corpusIcon } from "$lib/icons";

  let { data }: PageProps = $props();
</script>

<CardGrid
  gridItems={data.corpusList}
  getTargetLink={(c: Corpus) => `/browse/${c.name}`}>
  {#snippet item(c: Corpus)}
    <p class="flex items-center gap-2 text-lg">
      <Fa icon={corpusIcon} />
      {c.name}
    </p>
    <p>
      <span class="text-xl">
        {toHumanReadable(c.num_documents_estimate)}
      </span> documents
    </p>
    <p>
      <span class="text-xl">{c.num_datasets}</span>
      {c.num_datasets == 1 ? "dataset" : "datasets"}
    </p>
  {/snippet}
</CardGrid>
