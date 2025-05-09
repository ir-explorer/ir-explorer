<script lang="ts">
  import { toHumanReadable } from "$lib/util";
  let {
    value,
    total,
    desc,
  }: {
    value: number;
    total: number;
    desc: string;
  } = $props();
</script>

<div class="flex flex-col gap-1 text-center">
  <div
    class="radial-progress border-4 border-base-200 bg-base-200 text-primary"
    style=" --size:4em;
                  --value:{(value / total) * 100};
                  --thickness: 0.25em;">
    <span class="text-lg">
      {toHumanReadable(value)}
    </span>
  </div>
  <span class="text-xs">{desc}</span>
</div>
