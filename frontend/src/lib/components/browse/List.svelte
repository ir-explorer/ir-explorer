<script lang="ts" generics="T">
  import Fa from "svelte-fa";
  import { listArrowIcon } from "$lib/icons";
  import type { Snippet } from "svelte";

  let {
    listItems = $bindable(),
    headBegin,
    headEnd,
    item,
    getTargetLink,
  }: {
    listItems: T[];
    headBegin: Snippet;
    headEnd: Snippet;
    item: Snippet<[T]>;
    getTargetLink: (listItem: T) => string;
  } = $props();
</script>

<ul class="list rounded-box bg-base-100 shadow">
  <li class="bg-base-200 p-4">
    <div class="flex flex-row justify-between">
      {@render headBegin()}
      {@render headEnd()}
    </div>
  </li>

  {#each listItems as listItem}
    <a href={getTargetLink(listItem)}>
      <li class="list-row hover:bg-base-300">
        <div class="list-col-grow">
          {@render item(listItem)}
        </div>
        <div class="my-auto">
          <Fa icon={listArrowIcon} />
        </div>
      </li>
    </a>
  {/each}
</ul>
