<script lang="ts" generics="T">
  import { listArrowIcon } from "$lib/icons";
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
    getTargetLink: (listItem: T) => string;
  }

  let {
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
