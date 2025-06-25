<script lang="ts" generics="T">
  import { filterIcon } from "$lib/icons";
  import type { Paginated } from "$lib/types";
  import { onMount, type Snippet } from "svelte";
  import Fa from "svelte-fa";
  import List from "./List.svelte";

  const {
    getPage,
    head,
    item,
    getTargetLink,
    itemsPerPage,
    loadFirstPage = true,
  }: {
    getPage: (
      match: string | null,
      num_items: number,
      offset: number,
    ) => Promise<Paginated<T>>;
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
  let filter = $state("");
  let filterTrimmed = $derived(filter.trim());

  let promiseNextPage: Promise<Paginated<T>> | null = null;
  let abortToken = { abort: function () {} };

  async function showNextPage(waitTime: number = 0) {
    working = true;

    if (promiseNextPage != null) {
      abortToken.abort();
    }

    promiseNextPage = new Promise<Paginated<T>>(async (resolve, reject) => {
      let aborted = false;
      abortToken.abort = function () {
        reject();
        aborted = true;
      };

      // wait for a specified time so we can abort before fetching the results
      await new Promise((resolve) => setTimeout(resolve, waitTime));
      if (aborted) {
        return;
      }

      const nextPage = await getPage(
        filterTrimmed.length > 0 ? filterTrimmed : null,
        itemsPerPage,
        listItems.length,
      );
      resolve(nextPage);
    });

    promiseNextPage.then((nextPage) => {
      listItems = [...listItems, ...nextPage.items];
      totalNumItems = nextPage.total_num_items;
      working = false;
      loaded = true;
    });
  }

  function reset() {
    listItems = [];
    loaded = false;
  }

  if (loadFirstPage) {
    onMount(showNextPage);
  }
</script>

<div class="relative mb-4">
  <List bind:listItems headBegin={head} {item} {getTargetLink}>
    {#snippet headEnd()}
      <label class="input input-sm w-fit">
        <span class="text-sm">
          <Fa icon={filterIcon} />
        </span>
        <input
          type="text"
          class="w-12 transition-all focus:w-32"
          placeholder="Filter..."
          bind:value={filter}
          oninput={async () => {
            reset();
            await showNextPage(1000);
          }} />
      </label>
    {/snippet}
  </List>

  <div
    class="absolute right-0 -bottom-3 left-0 m-auto mx-auto join w-fit rounded bg-base-300">
    {#if loaded}
      <p class="badge-soft join-item badge h-6 text-sm badge-primary">
        Showing {numItemsDisplayed.toLocaleString()} of {totalNumItems.toLocaleString()}
      </p>
    {/if}
    {#if !loaded || numItemsDisplayed < totalNumItems}
      <button
        class="btn join-item h-6 w-12 btn-sm btn-primary"
        disabled={working}
        onclick={async () => {
          await showNextPage();
        }}
        ><span class={[working && "loading loading-xs"]}>More</span>
      </button>
    {/if}
  </div>
</div>
