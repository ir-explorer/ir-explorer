<script lang="ts">
  import CardGrid from "$lib/components/browse/CardGrid.svelte";
  import SizeIndicator from "$lib/components/browse/SizeIndicator.svelte";
  import IconWithText from "$lib/components/IconWithText.svelte";
  import { corpusIcon } from "$lib/icons";
  import type { Corpus } from "$lib/types";
  import type { PageProps } from "./$types";

  const { data }: PageProps = $props();
  const totalNumDocs = data.corpusList.reduce(
    (acc, corpus) => acc + corpus.numDocuments,
    0,
  );
</script>

<CardGrid
  gridItems={data.corpusList}
  getTargetLink={(c: Corpus) => `/browse/${c.name}`}>
  {#snippet item(c: Corpus)}
    <div class="flex items-center justify-between gap-4">
      <div class="flex flex-col gap-2">
        <div class="text-lg">
          <IconWithText icon={corpusIcon} text={c.name} iconWidth={6} />
        </div>
        <p>{c.numDatasets} {c.numDatasets == 1 ? "dataset" : "datasets"}</p>
      </div>
      <SizeIndicator
        value={c.numDocuments}
        total={totalNumDocs}
        desc={"documents"} />
    </div>
  {/snippet}
</CardGrid>
