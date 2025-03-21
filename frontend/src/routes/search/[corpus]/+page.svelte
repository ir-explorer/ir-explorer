<script lang="ts">
  import type { PageProps } from "./$types";
  import Fa from "svelte-fa";
  import {
    faBook,
    faFileLines,
    faHashtag,
  } from "@fortawesome/free-solid-svg-icons";

  let { data }: PageProps = $props();
</script>

<ul class="list bg-base-100 rounded-box shadow-md">
  <li class="p-4 text-xs">Search results</li>

  {#each data["hits"] as hit, index}
    <li class="list-row">
      <div>
        <div class="join">
          <p
            class="badge badge-primary join-item tooltip"
            data-tip="Score: {hit.score}"
          >
            <Fa icon={faHashtag} size={"sm"} />
            <span class="-ml-1.5">{index + 1}</span>
          </p>
          <p class="badge join-item">
            <Fa icon={faFileLines} />
            {hit.id}
          </p>
          <p class="badge join-item">
            <Fa icon={faBook} />
            {hit.corpus_name}
          </p>
        </div>
        <p class="my-2">{hit.text}</p>
      </div>
    </li>
  {/each}
</ul>
