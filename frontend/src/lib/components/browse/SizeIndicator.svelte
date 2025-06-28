<script lang="ts">
  import { toHumanReadable } from "$lib/util";

  const {
    value,
    total,
    desc,
    isEstimate = false,
  }: {
    value: number;
    total: number;
    desc: string;
    isEstimate?: boolean;
  } = $props();
</script>

<div
  class={[
    "flex flex-col gap-1.5 text-center",
    isEstimate && "tooltip tooltip-info",
  ]}
  data-tip="estimated value">
  <div
    class="radial-progress bg-primary-content text-primary"
    style="--size:4.5em; --value:{(value / total) * 100}; --thickness: 0.25em;">
    <span class="text-lg">{toHumanReadable(value)}</span>
  </div>
  <span class="text-xs">{desc}</span>
</div>
