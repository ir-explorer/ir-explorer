<script lang="ts">
  import type { PageProps } from "./$types";
  import CardGrid from "$lib/components/browse/CardGrid.svelte";
  import type { Corpus } from "$lib/types";
  import Fa from "svelte-fa";
  import { toHumanReadable } from "$lib/util";
  import { corpusIcon } from "$lib/icons";

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
    {@const fraction = c.num_documents_estimate / totalNumDocs}

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
      <div class="flex flex-col gap-2 text-center">
        <div
          class="radial-progress border-4 border-base-200 bg-base-200 text-primary"
          style=" --size:4em;
                  --value:{fraction * 100};
                  --thickness: 0.25em;">
          <span class="text-lg">
            {toHumanReadable(c.num_documents_estimate)}
          </span>
        </div>
        <span class="text-xs">documents</span>
      </div>
    </div>
  {/snippet}
</CardGrid>
