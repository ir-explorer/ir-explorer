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
  const pct = total == 0 ? 100 : (value / total) * 100;
</script>

<!--
@component
A visual indicator of a fraction in relation to the total.
-->
<div
  class={[
    "flex flex-col gap-1.5 text-center",
    isEstimate && "tooltip tooltip-info",
  ]}
  data-tip="estimated value">
  <div
    class="radial-progress border-3 border-neutral bg-neutral text-primary"
    style="--size:4.5em; --value:{pct}; --thickness: 0.25em;">
    <span class="text-lg">{toHumanReadable(value)}</span>
  </div>
  <span class="text-xs">{desc}</span>
</div>
