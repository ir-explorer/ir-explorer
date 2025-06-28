<script lang="ts">
  import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";
  import { Fa } from "svelte-fa";
</script>

<div class="flex font-serif text-2xl select-none">
  <div class="mr-1 grid items-center justify-items-center">
    <span class="col-[1] row-[1] h-7 w-9 rounded-xs bg-primary"></span>
    <span class="col-[1] row-[1] text-primary-content">IR</span>
  </div>
  expl<span class="mt-2 -mr-1 text-primary">
    <Fa icon={faMagnifyingGlass} />
  </span>rer
</div>
