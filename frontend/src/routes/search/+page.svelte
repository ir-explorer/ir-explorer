<script lang="ts">
  import { page } from "$app/state";
  import {
    corpusIcon,
    documentIcon,
    infoIcon,
    nextPageIcon,
    prevPageIcon,
  } from "$lib/icons";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();
  let corpusNames = $derived(page.url.searchParams.getAll("corpus"));
</script>

{#if data.result.totalNumItems == 0}
  <div class="alert-soft mx-auto alert w-fit">
    <span class="text-primary">
      <Fa icon={infoIcon} />
    </span>
    <span>No results found.</span>
  </div>
{:else}
  <ul class="list">
    <li class="list-row p-2 text-xs">
      <p>
        <span>
          {data.result.totalNumItems} results for query
          <i><b>{page.url.searchParams.get("q")}</b></i>
        </span>{#if corpusNames.length > 0}<span>
            &nbsp;(corpora: {corpusNames.join(", ")})</span
          >{/if}.
      </p>
    </li>

    {#each data.result.items as hit, index}
      <li class="list-row">
        <div>
          <div class="flex flex-row flex-wrap gap-2">
            <p
              class="badge-soft tooltip badge badge-primary tooltip-info"
              data-tip="Score: {hit.score}">
              #<span class="-ml-1 font-bold">
                {data.result.offset + index + 1}
              </span>
            </p>
            <a
              class="badge-soft badge hover:text-primary"
              href="/browse/{hit.corpusName}?documentId={hit.id}">
              <Fa icon={documentIcon} />
              {hit.id}
            </a>
            <a
              class="badge-soft badge hover:text-primary"
              href="/browse/{hit.corpusName}">
              <Fa icon={corpusIcon} />
              {hit.corpusName}
            </a>
          </div>
          <p class="my-2">{@html hit.snippet}</p>
        </div>
      </li>
    {/each}

    {#if data.totalPages > 1}
      <li class="list-row flex w-full justify-center">
        <div class="join">
          {#if data.prevPageLink != null}
            <a href={data.prevPageLink} class="btn join-item btn-sm btn-primary"
              ><Fa icon={prevPageIcon} /></a>
          {/if}
          <div
            class="join-item flex items-center border border-base-300 bg-base-200 px-4">
            <p class="text-sm">
              Page {data.pageNum} of {data.totalPages}
            </p>
          </div>
          {#if data.nextPageLink != null}
            <a href={data.nextPageLink} class="btn join-item btn-sm btn-primary"
              ><Fa icon={nextPageIcon} /></a>
          {/if}
        </div>
      </li>
    {/if}
  </ul>
{/if}
