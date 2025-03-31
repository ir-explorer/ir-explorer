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
        {#if data.query_id}
          <li>
            <a
              href="/browse/{data.corpusName}/{data.datasetName}?query_id={data.query_id}"
              ><Fa icon={queryIcon} />{data.query_id}</a>
          </li>
        {/if}
      {:else if data.document_id}
        <li>
          <a href="/browse/{data.corpusName}?document_id={data.document_id}"
            ><Fa icon={documentIcon} />{data.document_id}</a>
        </li>
      {/if}
    </ul>
  </div>
</Header>
<div class="mx-4 mt-20 mb-4 max-w-full">
  <div class="mx-auto max-w-5xl">
    {@render children()}
  </div>
</div>
