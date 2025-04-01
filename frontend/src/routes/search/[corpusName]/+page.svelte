<script lang="ts">
  import type { PageProps } from "./$types";
  import Fa from "svelte-fa";
  import { corpusIcon, documentIcon } from "$lib/icons";

  let { data }: PageProps = $props();
</script>

<ul class="list rounded-box bg-base-100 shadow-md">
  <li class="p-4 text-xs">
    Displaying {data.result.total_num_items} search results
  </li>

  {#each data.result.items as hit, index}
    <li class="list-row">
      <div>
        <div class="join">
          <span
            class="badge-soft tooltip join-item badge badge-primary"
            data-tip="Score: {hit.score}">
            #<span class="-ml-1 font-bold"
              >{data.result.offset + index + 1}</span>
          </span>
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
        <p class="my-2">{hit.text}</p>
      </div>
    </li>
  {/each}
</ul>
