<script lang="ts">
  import type { PageProps } from "./$types";
  import Fa from "svelte-fa";
  import { faFileLines, faHashtag } from "@fortawesome/free-solid-svg-icons";

  let { data }: PageProps = $props();
</script>

<ul class="list bg-base-100 rounded-box shadow">
  <li class="p-4 pb-2 text-xs">Search results</li>

  {#each data["hits"] as hit, index}
    <li class="list-row">
      <div>
        <div class="flex flex-row">
          <div class="tooltip" data-tip="Score: {hit.score}">
            <p class="badge bade-soft badge-primary">
              <Fa icon={faHashtag} />
              {index + 1}
            </p>
          </div>
          <p class="badge"><Fa icon={faFileLines} /> {hit.id}</p>
        </div>
        <p class="my-2">{hit.text}</p>
      </div>
    </li>
  {/each}
</ul>
