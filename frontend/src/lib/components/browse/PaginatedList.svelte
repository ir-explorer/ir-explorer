<script lang="ts" generics="T">
  import List from "./List.svelte";
  import { type Snippet } from "svelte";
  import { showMoreIcon } from "$lib/icons";
  import Fa from "svelte-fa";
  import type { Paginated } from "$lib/types";

  const {
    getPage,
    head,
    item,
    getTargetLink,
    itemsPerPage,
  }: {
    getPage: (num_items: number, offset: number) => Promise<Paginated<T>>;
    head: Snippet;
    item: Snippet<[T]>;
    getTargetLink: (listItem: T) => string;
    itemsPerPage: number;
  } = $props();

  let listItems: T[] = $state([]);
  let working = $state(false);
  let numItemsDisplayed = $derived(listItems.length);
  let totalNumItems = $state(0);
  let loaded = $state(false);

  async function showNextPage() {
    working = true;
    const currentPage = await getPage(itemsPerPage, listItems.length);
    listItems = [...listItems, ...currentPage.items];
    totalNumItems = currentPage.total_num_items;
    working = false;
    loaded = true;
  }
</script>

<div class="relative">
  <List bind:listItems headBegin={head} {item} {getTargetLink}>
    {#snippet headEnd()}
      {#if loaded}
        <p class="badge-soft badge badge-primary">
          Showing {numItemsDisplayed} of {totalNumItems}
        </p>
      {/if}
    {/snippet}
  </List>
  {#if !loaded || numItemsDisplayed < totalNumItems}
    <div
      class="absolute right-0 -bottom-4 left-0 m-auto mx-auto w-fit rounded-full bg-base-100">
      <button
        class="btn btn-circle shadow btn-soft btn-sm btn-primary"
        disabled={working}
        onclick={async () => {
          await showNextPage();
        }}
        ><span class={[working && "loading loading-sm"]}>
          <Fa icon={showMoreIcon} />
        </span>
      </button>
    </div>
  {/if}
</div>
