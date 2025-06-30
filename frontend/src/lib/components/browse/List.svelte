<script lang="ts" generics="T">
  import { listArrowIcon } from "$lib/icons";
  import type { Snippet } from "svelte";
  import Fa from "svelte-fa";

  let {
    listItems = $bindable(),
    headTitle,
    headItems,
    item,
    getTargetLink,
  }: {
    listItems: T[];
    headTitle: Snippet | null;
    headItems: Snippet | null;
    item: Snippet<[T]>;
    getTargetLink: (listItem: T) => string;
  } = $props();
</script>

<ul class="list rounded-box bg-base-100 shadow">
  <li class="rounded-box bg-base-200 px-4 py-4 md:py-2">
    <div class="flex flex-col gap-4 md:flex-row md:justify-between md:gap-2">
      {#if headTitle != null}
        {@render headTitle()}
      {/if}
      {#if headItems != null}
        {@render headItems()}
      {/if}
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
