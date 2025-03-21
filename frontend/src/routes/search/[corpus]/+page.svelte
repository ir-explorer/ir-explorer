<script lang="ts">
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();
</script>

{#each data["hits"] as hit}
  <div class="py-5">
    <p>ID: {hit.id}</p>
    <p>Score: {hit.score}</p>
    <p>{hit.text}</p>
  </div>
{/each}
