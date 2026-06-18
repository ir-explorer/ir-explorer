<script lang="ts">
  import { toHumanReadable } from "$lib/util";

  interface Props {
    /** The value to display (fraction of the total). */
    value: number;
    /** The total amount. */
    total: number;
    /** A description. */
    desc: string;
    /** Display a tooltip stating that the value is an estimate. */
    isEstimate?: boolean;
  }

  const { value, total, desc, isEstimate = false }: Props = $props();

  // avoid a division by 0
  const pct = $derived(total == 0 ? 100 : (value / total) * 100);
</script>

<!--
@component
A visual indicator of a fraction in relation to the total.
-->
<div
  class={[
    "flex w-24 flex-col text-right",
    isEstimate && "tooltip tooltip-info",
  ]}
  data-tip="estimated value">
  <div>
    <span class="block text-base leading-5 font-semibold text-base-content">
      {toHumanReadable(value)}
    </span>
    <span class="block text-xs leading-3 text-base-content/60">{desc}</span>
  </div>
  <progress
    class="progress mt-2 h-1 w-full bg-base-300 progress-primary"
    value={pct}
    max="100"
    aria-label={`${toHumanReadable(value)} ${desc}`}>
  </progress>
</div>
