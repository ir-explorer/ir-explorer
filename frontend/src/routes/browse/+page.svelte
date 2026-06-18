<script lang="ts">
  import CardGrid from "$lib/components/browse/CardGrid.svelte";
  import SizeIndicator from "$lib/components/browse/SizeIndicator.svelte";
  import IconWithText from "$lib/components/IconWithText.svelte";
  import { corpusIcon } from "$lib/icons";
  import type { Corpus } from "$lib/types";
  import type { PageProps } from "./$types";

  const { data }: PageProps = $props();
  const totalNumDocs = $derived(
    data.corpusList.reduce((acc, corpus) => acc + corpus.numDocuments, 0),
  );
</script>

<CardGrid
  gridItems={data.corpusList}
  getTargetLink={(c: Corpus) => `/browse/${c.name}` as const}>
  {#snippet item(c: Corpus)}
    <div class="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3">
      <div class="flex min-w-0 flex-col gap-1">
        <div class="text-lg">
          <IconWithText icon={corpusIcon} text={c.name} />
        </div>
        <p class="text-sm text-base-content/60">
          {c.numDatasets}
          {c.numDatasets == 1 ? "dataset" : "datasets"}
        </p>
      </div>
      <SizeIndicator
        value={c.numDocuments}
        total={totalNumDocs}
        desc="documents" />
    </div>
  {/snippet}
</CardGrid>
