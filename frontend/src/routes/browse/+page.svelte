<script lang="ts">
  import CardGrid from "$lib/components/browse/CardGrid.svelte";
  import SizeIndicator from "$lib/components/browse/SizeIndicator.svelte";
  import { corpusIcon } from "$lib/icons";
  import type { Corpus } from "$lib/types";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  const { data }: PageProps = $props();
  const totalNumDocs = data.corpusList.reduce(
    (acc, corpus) => acc + corpus.numDocuments,
    0,
  );
</script>

<CardGrid
  gridItems={data.corpusList.sort((a, b) => b.numDocuments - a.numDocuments)}
  getTargetLink={(c: Corpus) => `/browse/${c.name}`}>
  {#snippet item(c: Corpus)}
    <div class="flex items-center justify-between gap-4">
      <div class="flex flex-col gap-2">
        <p class="flex items-center gap-2 text-lg font-thin">
          <Fa icon={corpusIcon} />
          {c.name}
        </p>
        <p>
          <span class="text-xl">{c.numDatasets}</span>
          {c.numDatasets == 1 ? "dataset" : "datasets"}
        </p>
      </div>
      <SizeIndicator
        value={c.numDocuments}
        total={totalNumDocs}
        desc={"documents"} />
    </div>
  {/snippet}
</CardGrid>
