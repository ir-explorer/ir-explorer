<script lang="ts">
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();
</script>

<p>Available datasets:</p>
<ul>
  {#each data["datasets"] as dataset}
    <li>{dataset.name}</li>
  {/each}
</ul>
