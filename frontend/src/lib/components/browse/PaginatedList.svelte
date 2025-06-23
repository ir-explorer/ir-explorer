<script lang="ts" generics="T">
  import type { Paginated } from "$lib/types";
  import { onMount, type Snippet } from "svelte";
  import List from "./List.svelte";

  const {
    getPage,
    head,
    item,
    getTargetLink,
    itemsPerPage,
    loadFirstPage = true,
  }: {
    getPage: (num_items: number, offset: number) => Promise<Paginated<T>>;
    head: Snippet;
    item: Snippet<[T]>;
    getTargetLink: (listItem: T) => string;
    itemsPerPage: number;
    loadFirstPage?: boolean;
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

  if (loadFirstPage) {
    onMount(showNextPage);
  }
</script>

<div class="relative mb-4">
  <List bind:listItems headBegin={head} headEnd={null} {item} {getTargetLink} />
  <div
    class="absolute right-0 -bottom-3 left-0 m-auto mx-auto join w-fit rounded-full bg-base-300">
    {#if loaded}
      <p class="badge-soft join-item badge h-6 text-sm badge-primary">
        Showing {numItemsDisplayed.toLocaleString()} of {totalNumItems.toLocaleString()}
      </p>
    {/if}
    {#if numItemsDisplayed < totalNumItems}
      <button
        class="btn join-item h-6 w-12 btn-sm btn-primary"
        disabled={working}
        onclick={async () => {
          await showNextPage();
        }}
        ><span class={[working && "loading loading-sm"]}>More</span>
      </button>
    {/if}
  </div>
</div>
