<script lang="ts">
  import { Fa } from "svelte-fa";
  import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";
</script>

<div class="flex font-serif text-2xl select-none">
  <div class="grid items-center justify-items-center mr-1">
    <span class="row-[1] col-[1] bg-primary rounded-xs h-7 w-9"></span>
    <span class="row-[1] col-[1] text-base-100">IR</span>
  </div>
  expl<span class="mt-2 -mr-1 text-primary">
    <Fa icon={faMagnifyingGlass} />
  </span>rer
</div>
