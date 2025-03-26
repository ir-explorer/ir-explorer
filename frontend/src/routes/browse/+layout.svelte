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
      {#if data.corpus}
        <li>
          <a href="/browse/{data.corpus}"
            ><Fa icon={corpusIcon} />{data.corpus}
          </a>
        </li>
      {/if}

      {#if data.dataset}
        <li>
          <a href="/browse/{data.corpus}/{data.dataset}"
            ><Fa icon={datasetIcon} />{data.dataset}
          </a>
        </li>
        {#if data.q_id}
          <li>
            <a href="/browse/{data.corpus}/{data.dataset}?query={data.q_id}"
              ><Fa icon={queryIcon} />{data.q_id}</a>
          </li>
        {/if}
      {:else if data.doc_id}
        <li>
          <a href="/browse/{data.corpus}?doc={data.doc_id}"
            ><Fa icon={documentIcon} />{data.doc_id}</a>
        </li>
      {/if}
    </ul>
  </div>
</Header>
<div class="mt-20 mb-4 max-w-full">
  <div class="mx-auto max-w-5xl">
    {@render children()}
  </div>
</div>
