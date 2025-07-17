<script lang="ts">
  import Header from "$lib/components/Header.svelte";
  import Logo from "$lib/components/Logo.svelte";
  import MainMenu from "$lib/components/MainMenu.svelte";
  import {
    browseIcon,
    corpusIcon,
    datasetIcon,
    documentIcon,
    queryIcon,
  } from "$lib/icons.js";
  import Fa from "svelte-fa";

  let { data, children } = $props();
</script>

<Header>
  {#snippet start()}
    <div class="flex flex-row items-center gap-4">
      <MainMenu availableOptions={data.availableOptions} />
      <a class="hidden md:block" href="/"><Logo small /></a>
    </div>
  {/snippet}
  {#snippet center()}
    <div class="max-w-full rounded-box border border-base-300 bg-neutral px-4">
      <div class="breadcrumbs text-sm">
        <ul>
          <li><a href="/browse"><Fa icon={browseIcon} />Browse</a></li>
          {#if data.corpusName}
            <li>
              <a href="/browse/{data.corpusName}"
                ><Fa icon={corpusIcon} />{data.corpusName}
              </a>
            </li>
          {/if}

          {#if data.datasetName}
            <li>
              <a href="/browse/{data.corpusName}/{data.datasetName}"
                ><Fa icon={datasetIcon} />{data.datasetName}
              </a>
            </li>
            {#if data.queryId}
              <li>
                <a
                  href="/browse/{data.corpusName}/{data.datasetName}?queryId={data.queryId}"
                  ><Fa icon={queryIcon} />{data.queryId}</a>
              </li>
            {/if}
          {:else if data.documentId}
            <li>
              <a href="/browse/{data.corpusName}?documentId={data.documentId}"
                ><Fa icon={documentIcon} />{data.documentId}</a>
            </li>
          {/if}
        </ul>
      </div>
    </div>
  {/snippet}
</Header>

<div class="mx-auto mt-20 mb-4 max-w-5xl">
  <div class="mx-4 flex flex-col gap-8">
    {@render children()}
  </div>
</div>
