<script lang="ts">
  import type { PageProps } from "./$types";
  import Fa from "svelte-fa";
  import { corpusIcon, documentIcon } from "$lib/icons";

  let { data }: PageProps = $props();
</script>

<ul class="list bg-base-100 rounded-box shadow-md">
  <li class="p-4 text-xs">Search results</li>

  {#each data["hits"] as hit, index}
    <li class="list-row">
      <div>
        <div class="join">
          <p
            class="badge badge-soft badge-primary join-item tooltip"
            data-tip="Score: {hit.score}"
          >
            #<span class="-ml-1 font-bold">{index + 1}</span>
          </p>
          <p class="badge badge-soft join-item">
            <Fa icon={corpusIcon} />
            {hit.corpus_name}
          </p>
          <p class="badge badge-soft join-item">
            <Fa icon={documentIcon} />
            {hit.id}
          </p>
        </div>
        <p class="my-2">{hit.text}</p>
      </div>
    </li>
  {/each}
</ul>
