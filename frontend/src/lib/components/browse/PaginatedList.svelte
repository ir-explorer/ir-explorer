<script module lang="ts">
  export interface PaginatedListSnapshot<T> {
    listItems: T[];
    totalNumItems: number;
    loaded: boolean;
    working: boolean;
    match: string;
    orderByValue: string | null;
    desc: boolean;
  }
</script>

<script lang="ts" generics="T">
  import { goToIcon, matchIcon, orderAscIcon, orderDescIcon } from "$lib/icons";
  import { selectedOptions } from "$lib/options.svelte";
  import type { BrowseLink, OrderByOption, Paginated } from "$lib/types";
  import { toHumanReadable } from "$lib/util";
  import { onMount, type Snippet } from "svelte";
  import Fa from "svelte-fa";
  import List from "./List.svelte";

  interface Props {
    /**
     * Return the items for a single page.
     *
     * @param match - The content of the 'match' text field.
     * @param orderBy - The selected 'order by' option.
     * @param desc - Whether to order in a descending fashion.
     * @param numItems - How many items to return.
     * @param offset - How many items to skip.
     *
     * @returns The items.
     */
    getPage: (
      match: string | null,
      orderBy: string | null,
      desc: boolean,
      numItems: number,
      offset: number,
    ) => Promise<Paginated<T>>;
    /** Render the title in the list head. */
    headTitle: Snippet;
    /** Render a single list item. */
    item: Snippet<[T]>;
    /** Return the target for a specific item. */
    getTargetLink: (listItem: T) => BrowseLink;
    /** A list of options the items can be ordered by. */
    orderByOptions?: OrderByOption[];
    /** Order-by options that require non-empty match text. */
    matchDependentOrderByOptions?: string[];
    /** Target for the 'go to' form. */
    goToTarget?: string | null;
    /** Name for the 'go to' form. */
    goToName?: string | null;
  }

  const {
    getPage,
    headTitle,
    item,
    getTargetLink,
    orderByOptions = [],
    matchDependentOrderByOptions = [],
    goToTarget = null,
    goToName = null,
  }: Props = $props();

  let listItems: T[] = $state([]);
  let working = $state(false);
  const numItemsDisplayed = $derived(listItems.length);
  let totalNumItems = $state(0);
  let loaded = $state(false);
  let match = $state("");
  const matchTrimmed = $derived(match.trim());

  let promiseNextPage: Promise<Paginated<T>> | null = null;
  let abortToken = { abort: function () {} };

  let orderByValue: string | null = $state(null);
  let desc = $state(true);
  const effectiveOrderBy: string | null = $derived(
    orderByValue !== null &&
      matchDependentOrderByOptions.includes(orderByValue) &&
      matchTrimmed.length === 0
      ? null
      : orderByValue,
  );

  /** Capture the user-visible state for SvelteKit's history snapshots. */
  export function capture(): PaginatedListSnapshot<T> {
    return {
      listItems,
      totalNumItems,
      loaded,
      working,
      match,
      orderByValue,
      desc,
    };
  }

  /** Restore a list without requesting data that is already displayed. */
  export function restore(snapshot: PaginatedListSnapshot<T>) {
    abortToken.abort();
    promiseNextPage = null;
    listItems = snapshot.listItems;
    totalNumItems = snapshot.totalNumItems;
    loaded = snapshot.loaded;
    match = snapshot.match;
    orderByValue = snapshot.orderByValue;
    desc = snapshot.desc;
    working = false;

    // snapshot was captured before the next page arrived, resume request
    if (snapshot.working) {
      void showNextPage();
    }
  }

  async function showNextPage(waitTime: number = 0) {
    working = true;

    if (promiseNextPage != null) {
      abortToken.abort();
    }

    promiseNextPage = new Promise<Paginated<T>>((resolve, reject) => {
      let aborted = false;
      abortToken.abort = function () {
        reject();
        aborted = true;
      };

      void (async () => {
        // wait for a specified time so we can abort before fetching the results
        await new Promise((resolve) => setTimeout(resolve, waitTime));
        if (aborted) {
          return;
        }

        const nextPage = await getPage(
          matchTrimmed.length > 0 ? matchTrimmed : null,
          effectiveOrderBy,
          desc,
          selectedOptions.itemsPerPage,
          listItems.length,
        );
        resolve(nextPage);
      })().catch(reject);
    });

    const pendingPage = promiseNextPage;
    pendingPage
      .then((nextPage) => {
        // a reset or history restore may have superseded this request
        if (promiseNextPage !== pendingPage) return;

        listItems = [...listItems, ...nextPage.items];
        totalNumItems = nextPage.totalNumItems;
        working = false;
        loaded = true;
      })
      .catch(() => {
        // handle cancelled/stale requests without stopping a newer request
        if (promiseNextPage === pendingPage) working = false;
      });
  }

  async function reset(waitTime: number = 0) {
    listItems = [];
    loaded = false;
    await showNextPage(waitTime);
  }

  // load first page
  onMount(showNextPage);
</script>

<!--
@component
Render items as a list with pagination.
-->
<div class="mb-2 flex flex-col justify-center">
  <List bind:listItems {headTitle} {item} {getTargetLink}>
    {#snippet headItems()}
      <div class="z-0 flex flex-col gap-2 md:flex-row">
        <!-- match -->
        <label class="input input-sm w-full bg-base-100 shadow-sm md:w-fit">
          <span class="text-sm">
            <Fa icon={matchIcon} />
          </span>
          <input
            type="text"
            class="w-full md:w-32"
            placeholder="Match..."
            bind:value={match}
            oninput={async () => {
              await reset(1000);
            }} />
        </label>

        <!-- order by -->
        <div class="join w-full md:w-fit">
          <!-- hide select if there are no options to order by -->
          {#if orderByOptions.length > 0}
            <select
              class="select join-item w-full bg-base-100 select-sm md:w-fit"
              bind:value={orderByValue}
              onchange={async () => {
                await reset();
              }}>
              <option value={null} selected>Order by...</option>
              {#each orderByOptions as orderByOption (orderByOption.name)}
                <option value={orderByOption.option}
                  >{orderByOption.name}</option>
              {/each}
            </select>
          {/if}

          <!-- hide desc\asc selection if nothing is selected -->
          {#if orderByValue != null}
            <label
              for="order-desc"
              class="btn join-item gap-0 border border-base-300 btn-sm has-checked:btn-primary">
              <input
                class="w-0 opacity-0"
                type="radio"
                id="order-desc"
                name="radio-order"
                value={true}
                onchange={async () => {
                  await reset();
                }}
                bind:group={desc}
                checked />
              <Fa icon={orderDescIcon} />
            </label>
            <label
              for="order-asc"
              class="btn join-item gap-0 border border-base-300 btn-sm has-checked:btn-primary">
              <input
                class="w-0 opacity-0"
                type="radio"
                id="order-asc"
                name="radio-order"
                value={false}
                onchange={async () => {
                  await reset();
                }}
                bind:group={desc} />
              <Fa icon={orderAscIcon} />
            </label>
          {/if}
        </div>

        {#if goToTarget !== null && goToName !== null}
          <!-- go to -->
          <form class="join w-full md:w-fit" action={goToTarget}>
            <input
              type="text"
              name={goToName}
              class="input input-sm join-item w-full bg-base-100 md:w-24"
              placeholder="Go to ID..." />
            <button class="btn join-item btn-sm btn-primary" type="submit">
              <Fa icon={goToIcon} />
            </button>
          </form>
        {/if}
      </div>
    {/snippet}
  </List>

  <!-- number of items and "more" button -->
  <div class="join mx-auto rounded-t-none">
    {#if loaded}
      <p
        class="join-item flex h-6 items-center rounded-t-none bg-base-200 px-2 text-sm text-base-content shadow-sm">
        Showing {toHumanReadable(numItemsDisplayed)} of {toHumanReadable(
          totalNumItems,
        )}
      </p>
    {/if}
    {#if !working && numItemsDisplayed < totalNumItems}
      <button
        class="btn join-item h-6 w-12 rounded-t-none shadow-sm btn-sm btn-primary"
        disabled={working}
        onclick={async () => {
          await showNextPage();
        }}
        >More
      </button>
    {/if}
    {#if working}
      <div
        class="join-item flex h-6 w-12 items-center justify-center rounded-t-none bg-base-200 shadow-sm">
        <span class={[working && "loading loading-xs"]}></span>
      </div>
    {/if}
  </div>
</div>
