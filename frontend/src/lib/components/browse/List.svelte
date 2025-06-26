<script lang="ts" generics="T">
  import { listArrowIcon } from "$lib/icons";
  import type { Snippet } from "svelte";
  import Fa from "svelte-fa";

  let {
    listItems = $bindable(),
    headBegin,
    headEnd,
    item,
    getTargetLink,
  }: {
    listItems: T[];
    headBegin: Snippet | null;
    headEnd: Snippet | null;
    item: Snippet<[T]>;
    getTargetLink: (listItem: T) => string;
  } = $props();
</script>

<ul class="list rounded-box bg-base-100 shadow">
  <li class="bg-base-200 px-4 py-2">
    <div class="flex flex-row justify-between">
      {#if headBegin != null}
        {@render headBegin()}
      {/if}
      {#if headEnd != null}
        {@render headEnd()}
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
