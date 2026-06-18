<script lang="ts" generics="T">
  import { resolve } from "$app/paths";
  import { listArrowIcon } from "$lib/icons";
  import type { BrowseLink } from "$lib/types";
  import type { Snippet } from "svelte";
  import Fa from "svelte-fa";

  interface Props {
    /** Items to render in the list. */
    listItems: T[];
    /** Render the title in the list head. */
    headTitle: Snippet | null;
    /** Render other items in the list head. */
    headItems: Snippet | null;
    /** Render a single list item. */
    item: Snippet<[T]>;
    /** Return the target for a specific item. */
    getTargetLink: (listItem: T) => BrowseLink;
  }

  const {
    listItems = $bindable(),
    headTitle,
    headItems,
    item,
    getTargetLink,
  }: Props = $props();
</script>

<!--
@component
Render items as a list.
-->
<ul class="list rounded-box border border-base-300 bg-base-100 shadow-sm">
  <li
    class="rounded-t-box border-b border-base-300 bg-base-200 px-4 py-3 md:py-2">
    <div class="flex flex-col gap-3 md:flex-row md:justify-between md:gap-2">
      {#if headTitle != null}
        {@render headTitle()}
      {/if}
      {#if headItems != null}
        {@render headItems()}
      {/if}
    </div>
  </li>

  {#each listItems as listItem (getTargetLink(listItem))}
    <a href={resolve(getTargetLink(listItem) as `/browse/${string}`)}>
      <li class="list-row transition-colors hover:bg-base-200">
        <div class="list-col-grow">
          {@render item(listItem)}
        </div>
        <div class="my-auto text-base-content">
          <Fa icon={listArrowIcon} />
        </div>
      </li>
    </a>
  {/each}
</ul>
