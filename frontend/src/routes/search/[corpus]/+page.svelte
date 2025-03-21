<script lang="ts">
  import type { PageProps } from "./$types";
  import Fa from "svelte-fa";
  import { faFileLines, faHashtag } from "@fortawesome/free-solid-svg-icons";

  let { data }: PageProps = $props();
</script>

<ul class="list bg-base-100 rounded-box shadow-md">
  <li class="p-4 pb-2 text-xs">Search results</li>

  {#each data["hits"] as hit, index}
    <li class="list-row">
      <div>
        <div class="flex flex-row gap-2">
          <div class="tooltip" data-tip="Score: {hit.score}">
            <p class="badge badge-outline badge-primary font-bold">
              <Fa icon={faHashtag} />
              {index + 1}
            </p>
          </div>
          <p class="badge badge-outline">
            <Fa icon={faFileLines} />
            {hit.id}
          </p>
        </div>
        <p class="my-2">{hit.text}</p>
      </div>
    </li>
  {/each}
</ul>
