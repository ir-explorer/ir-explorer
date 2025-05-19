<script lang="ts" generics="T">
  import List from "./List.svelte";
  import { onMount, type Snippet } from "svelte";
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
  <div class="relative">
    <List bind:listItems headBegin={head} {item} {getTargetLink}>
      {#snippet headEnd()}
        <p class="badge-soft badge badge-primary">
          Showing {numItemsDisplayed} of {totalNumItems}
        </p>
      {/snippet}
    </List>
    {#if numItemsDisplayed < totalNumItems}
      <div class="absolute -bottom-4 flex w-full justify-center">
        <div class="bg-base-100">
          <button
            class="btn w-24 shadow btn-soft btn-sm btn-primary"
            disabled={working}
            onclick={async () => {
              await showNextPage();
            }}
            ><span class={[working && "loading loading-sm"]}>Show more</span>
          </button>
        </div>
      </div>
    {/if}
  </div>
{/await}
