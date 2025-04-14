<script lang="ts" generics="T">
  import List from "./List.svelte";
  import { onMount, type Snippet } from "svelte";
  import type { Paginated } from "$lib/types";

  let {
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

  async function showNextPage() {
    working = true;
    const currentPage = await getPage(itemsPerPage, listItems.length);
    listItems = [...listItems, ...currentPage.items];
    totalNumItems = currentPage.total_num_items;
    working = false;
  }

  let initialLoad = $state();
  onMount(() => {
    initialLoad = showNextPage();
  });
</script>

{#await initialLoad}
  <div class="flex w-full justify-center">
    <span class="loading"></span>
  </div>
{:then}
  <List bind:listItems {head} {item} {getTargetLink} />
  <div class="mt-4 join flex h-8 w-full justify-center">
    <div
      class="join-item flex flex-col justify-center border border-base-200 px-2">
      <p class="text-sm">
        Showing {numItemsDisplayed} out of {totalNumItems} items
      </p>
    </div>
    {#if working}
      <div class="btn-disabled btn h-8 w-24">
        <span class="loading loading-sm"></span>
      </div>
    {:else}
      <button
        class="btn join-item h-8 w-24 btn-soft btn-sm btn-primary"
        disabled={numItemsDisplayed >= totalNumItems}
        onclick={async () => {
          await showNextPage();
        }}
        >Show more
      </button>
    {/if}
  </div>
{/await}
