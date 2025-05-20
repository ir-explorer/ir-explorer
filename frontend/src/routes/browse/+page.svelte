<script lang="ts">
  import CardGrid from "$lib/components/browse/CardGrid.svelte";
  import SizeIndicator from "$lib/components/browse/SizeIndicator.svelte";
  import { corpusIcon } from "$lib/icons";
  import type { Corpus } from "$lib/types";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  const { data }: PageProps = $props();
  const totalNumDocs = data.corpusList.reduce(
    (acc, corpus) => acc + corpus.num_documents_estimate,
    0,
  );
</script>

<CardGrid
  gridItems={data.corpusList.sort(
    (a, b) => b.num_documents_estimate - a.num_documents_estimate,
  )}
  getTargetLink={(c: Corpus) => `/browse/${c.name}`}>
  {#snippet item(c: Corpus)}
    <div class="flex items-center justify-between">
      <div class="flex flex-col gap-2">
        <p class="flex items-center gap-2 text-lg">
          <Fa icon={corpusIcon} />
          {c.name}
        </p>
        <p>
          <span class="text-xl">{c.num_datasets}</span>
          {c.num_datasets == 1 ? "dataset" : "datasets"}
        </p>
      </div>
      <SizeIndicator
        value={c.num_documents_estimate}
        total={totalNumDocs}
        desc={"documents"}
        isEstimate />
    </div>
  {/snippet}
</CardGrid>
