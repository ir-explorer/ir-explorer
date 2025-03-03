<script lang="ts">
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();
</script>

<p>Search hits:</p>
<ul>
  {#each data["hits"] as hit}
    <li>{hit.text}</li>
    <br />
  {/each}
</ul>
