<script lang="ts">
  import type { PageProps } from "./$types";
  import Fa from "svelte-fa";
  import { faChevronRight } from "@fortawesome/free-solid-svg-icons";

  let { data }: PageProps = $props();
</script>

<ul class="list rounded-box bg-base-100 shadow-md">
  <li class="p-4 text-xs">Available corpora</li>

  {#each data["corpora"] as corpus}
    <a href="/browse/{corpus.name}">
      <li class="list-row hover:bg-base-300">
        <div class="list-col-grow">
          {corpus.name}
        </div>
        <div class="my-auto">
          <Fa icon={faChevronRight} />
        </div>
      </li>
    </a>
  {/each}
</ul>
