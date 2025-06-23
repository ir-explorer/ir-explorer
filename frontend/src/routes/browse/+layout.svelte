<script lang="ts">
  import Header from "$lib/components/Header.svelte";
  import Logo from "$lib/components/Logo.svelte";
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
    <div class="breadcrumbs text-sm">
      <ul>
        <li><a href="/"><Logo /></a></li>
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
          {#if data.queryID}
            <li>
              <a
                href="/browse/{data.corpusName}/{data.datasetName}?query_id={data.queryID}"
                ><Fa icon={queryIcon} />{data.queryID}</a>
            </li>
          {/if}
        {:else if data.documentID}
          <li>
            <a href="/browse/{data.corpusName}?document_id={data.documentID}"
              ><Fa icon={documentIcon} />{data.documentID}</a>
          </li>
        {/if}
      </ul>
    </div>
  {/snippet}
</Header>

<div class="mx-auto mt-20 mb-4 flex max-w-5xl flex-col gap-8">
  {@render children()}
</div>
