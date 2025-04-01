<script lang="ts" generics="T">
  import Fa from "svelte-fa";
  import { listArrowIcon } from "$lib/icons";
  import type { ListItem } from "$lib/types";
  import type { Snippet } from "svelte";

  let {
    listItems,
    head,
    item,
  }: { listItems: ListItem<T>[]; head: Snippet; item: Snippet<[T]> } = $props();
</script>

<ul class="list rounded-box bg-base-100 shadow-md">
  <li class="p-4 text-xs">{@render head()}</li>

  {#each listItems as listItem}
    <a href={listItem.target}>
      <li class="list-row hover:bg-base-300">
        <div class="list-col-grow">
          {@render item(listItem.item)}
        </div>
        <div class="my-auto">
          <Fa icon={listArrowIcon} />
        </div>
      </li>
    </a>
  {/each}
</ul>
