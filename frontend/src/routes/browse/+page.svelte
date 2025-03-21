<script lang="ts">
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();
</script>

<p>Available corpora:</p>
<ul>
  {#each data["corpora"] as corpus}
    <li>{corpus.name}</li>
  {/each}
</ul>
