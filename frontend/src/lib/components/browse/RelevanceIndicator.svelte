<script lang="ts">
  import type { RelevanceInfo } from "$lib/types";
  import { faCaretDown } from "@fortawesome/free-solid-svg-icons";
  import Fa from "svelte-fa";

  interface Props {
    relevance: RelevanceInfo;
  }

  const { relevance }: Props = $props();

  const scaleValues = $derived(
    Array.from(
      { length: relevance.max - relevance.min + 1 },
      (_, index) => relevance.min + index,
    ),
  );

  const columnPosition = $derived(
    ((relevance.score - relevance.min + 0.5) / scaleValues.length) * 100,
  );
</script>

<!--
@component
Display a relevance score in the context of its dataset's observed range and binary relevance threshold.
-->
<div
  class="flex h-4 w-fit shrink-0 items-center gap-2 text-xs text-base-content/60">
  <span>{relevance.min}</span>
  <div class="relative flex">
    <div
      class="absolute bottom-full flex -translate-x-1/2 items-start justify-center"
      style={`left: ${columnPosition}%`}>
      <Fa icon={faCaretDown} />
    </div>
    <div class="flex gap-px">
      {#each scaleValues as value (value)}
        <div
          class:bg-success={value >= relevance.threshold}
          class:bg-error={value < relevance.threshold}
          class="h-1.5 w-4 shrink-0">
        </div>
      {/each}
    </div>
  </div>
  <span>{relevance.max}</span>
</div>
