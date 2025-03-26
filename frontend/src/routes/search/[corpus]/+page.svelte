<script lang="ts">
  import type { PageProps } from "./$types";
  import Fa from "svelte-fa";
  import { corpusIcon, documentIcon } from "$lib/icons";

  let { data }: PageProps = $props();
</script>

<ul class="shadow-md list bg-base-100 rounded-box">
  <li class="p-4 text-xs">Search results</li>

  {#each data["hits"] as hit, index}
    <li class="list-row">
      <div>
        <div class="join">
          <span
            class="badge badge-soft badge-primary join-item tooltip"
            data-tip="Score: {hit.score}"
          >
            #<span class="-ml-1 font-bold">{index + 1}</span>
          </span>
          <a
            class="badge badge-soft badge-neutral hover:text-primary join-item"
            href="/browse/{hit.corpus_name}"
          >
            <Fa icon={corpusIcon} />
            {hit.corpus_name}
          </a>
          <a
            class="badge badge-soft badge-neutral hover:text-primary join-item"
            href="/browse/{hit.corpus_name}?doc={hit.id}"
          >
            <Fa icon={documentIcon} />
            {hit.id}
          </a>
        </div>
        <p class="my-2">{hit.text}</p>
      </div>
    </li>
  {/each}
</ul>
