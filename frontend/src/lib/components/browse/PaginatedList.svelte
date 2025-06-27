<script lang="ts" generics="T">
  import { filterIcon, orderAscIcon, orderDescIcon } from "$lib/icons";
  import type { OrderByOption, Paginated } from "$lib/types";
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
    orderByOptions = [],
  }: {
    getPage: (
      match: string | null,
      order_by: string | null,
      desc: boolean,
      num_items: number,
      offset: number,
    ) => Promise<Paginated<T>>;
    head: Snippet;
    item: Snippet<[T]>;
    getTargetLink: (listItem: T) => string;
    itemsPerPage: number;
    loadFirstPage?: boolean;
    orderByOptions?: OrderByOption[];
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

  let orderByValue = $state(null);
  let desc = $state(true);

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
        orderByValue,
        desc,
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

  async function reset(waitTime: number = 0) {
    listItems = [];
    loaded = false;
    await showNextPage(waitTime);
  }

  if (loadFirstPage) {
    onMount(showNextPage);
  }
</script>

<div class="relative mb-4">
  <List bind:listItems headBegin={head} {item} {getTargetLink}>
    {#snippet headEnd()}
      <div class="flex flex-row gap-2">
        <!-- filter -->
        <label class="input input-sm w-fit">
          <span class="text-sm">
            <Fa icon={filterIcon} />
          </span>
          <input
            type="text"
            class="w-32 transition-all"
            placeholder="Filter..."
            bind:value={filter}
            oninput={async () => {
              await reset(1000);
            }} />
        </label>

        <!-- order by -->
        <div class="join">
          <!-- hide select if there are no options to order by -->
          {#if orderByOptions.length > 0}
            <select
              class="select join-item w-fit select-sm"
              bind:value={orderByValue}
              onchange={async () => {
                await reset();
              }}>
              <option value={null} selected>Order by...</option>
              {#each orderByOptions as orderByOption}
                <option value={orderByOption.option}
                  >{orderByOption.name}</option>
              {/each}
            </select>
          {/if}

          <!-- hide desc\asc selection if nothing is selected -->
          {#if orderByValue != null}
            <label
              for="order-desc"
              class="btn join-item gap-0 btn-sm has-checked:btn-primary">
              <input
                class="w-0 opacity-0"
                type="radio"
                id="order-desc"
                name="radio-order"
                value={true}
                onclick={async () => {
                  await reset();
                }}
                bind:group={desc}
                checked />
              <Fa icon={orderDescIcon} />
            </label>
            <label
              for="order-asc"
              class="btn join-item gap-0 btn-sm has-checked:btn-primary">
              <input
                class="w-0 opacity-0"
                type="radio"
                id="order-asc"
                name="radio-order"
                value={false}
                onclick={async () => {
                  await reset();
                }}
                bind:group={desc} />
              <Fa icon={orderAscIcon} />
            </label>
          {/if}
        </div>
      </div>
    {/snippet}
  </List>

  <!-- number of items and "more" button -->
  <div
    class="absolute right-0 -bottom-3 left-0 m-auto mx-auto join w-fit rounded-box">
    {#if loaded}
      <p class="badge-soft join-item badge h-6 text-sm badge-primary">
        Showing {numItemsDisplayed.toLocaleString()} of {totalNumItems.toLocaleString()}
      </p>
    {/if}
    {#if !working && numItemsDisplayed < totalNumItems}
      <button
        class="btn join-item h-6 w-12 btn-sm btn-primary"
        disabled={working}
        onclick={async () => {
          await showNextPage();
        }}
        >More
      </button>
    {/if}
    {#if working}
      <div
        class="join-item flex h-6 w-12 items-center justify-center bg-base-300">
        <span class={[working && "loading loading-xs"]}></span>
      </div>
    {/if}
  </div>
</div>
