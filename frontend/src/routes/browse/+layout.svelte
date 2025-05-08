<script lang="ts">
  import Header from "$lib/components/Header.svelte";
  import Fa from "svelte-fa";
  import {
    browseIcon,
    datasetIcon,
    corpusIcon,
    documentIcon,
    queryIcon,
  } from "$lib/icons.js";

  let { data, children } = $props();
</script>

<Header>
  {#snippet center()}
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
<div class="mx-4 mt-20 mb-4 max-w-full">
  <div class="mx-auto max-w-5xl">
    {@render children()}
  </div>
</div>
