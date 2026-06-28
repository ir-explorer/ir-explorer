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
    {#each scaleValues as value, index (value)}
      <div
        class:bg-success={value >= relevance.threshold}
        class:bg-error={value < relevance.threshold}
        class:border-r={index === scaleValues.length - 1}
        class="h-1.25 w-4 shrink-0 border-y border-l">
      </div>
    {/each}
  </div>
  <span>{relevance.max}</span>
</div>
