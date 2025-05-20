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
</script>

{#if data.result.total_num_items == 0}
  <div class="alert-soft mx-auto alert w-fit">
    <span class="text-primary">
      <Fa icon={infoIcon} />
    </span>
    <span>No results found.</span>
  </div>
{:else}
  <ul class="list rounded-box bg-base-100 shadow-md">
    <li class="p-4 text-xs">
      Results {data.result.offset + 1} to {data.result.offset +
        data.result.items.length} (total: {data.result.total_num_items}) for
      query <i><b>{page.url.searchParams.get("q")}</b></i>.
    </li>

    {#each data.result.items as hit, index}
      <li class="list-row">
        <div>
          <div class="flex gap-2">
            <p
              class="badge-soft tooltip badge badge-primary"
              data-tip="Score: {hit.score}">
              #<span class="-ml-1 font-bold">
                {data.result.offset + index + 1}
              </span>
            </p>
            <div class="join">
              <a
                class="badge-soft join-item badge hover:text-primary"
                href="/browse/{hit.corpus_name}">
                <Fa icon={corpusIcon} />
                {hit.corpus_name}
              </a>
              <a
                class="badge-soft join-item badge hover:text-primary"
                href="/browse/{hit.corpus_name}?document_id={hit.id}">
                <Fa icon={documentIcon} />
                {hit.id}
              </a>
            </div>
          </div>
          <p class="my-2">{@html hit.snippet}</p>
        </div>
      </li>
    {/each}
  </ul>

  {#if data.totalPages > 1}
    <div class="mt-4 join flex w-full justify-center">
      {#if data.prevPageLink != null}
        <a
          href={data.prevPageLink}
          class="btn join-item btn-soft btn-sm btn-primary"
          ><Fa icon={prevPageIcon} /></a>
      {/if}
      <div
        class="join-item flex items-center border border-base-300 bg-base-200 px-4">
        <p class="text-sm">
          Page {data.pageNum} of {data.totalPages}
        </p>
      </div>
      {#if data.nextPageLink != null}
        <a
          href={data.nextPageLink}
          class="btn join-item btn-soft btn-sm btn-primary"
          ><Fa icon={nextPageIcon} /></a>
      {/if}
    </div>
  {/if}
{/if}
