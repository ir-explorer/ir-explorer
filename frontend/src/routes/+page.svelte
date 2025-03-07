<script lang="ts">
  import type { PageProps } from "./$types";
  import type { Corpus } from "$lib/types";

  let { data }: PageProps = $props();
  let selected_corpus: Corpus | undefined = $state();
</script>

<label for="cars">Choose a corpus:</label>
<select name="corpora" id="corpora" bind:value={selected_corpus}>
  {#each data.corpora as corpus}
    <option value={corpus}>{corpus.name}</option>
  {/each}
</select>
<p>
  selected corpus: {selected_corpus ? selected_corpus.name : ""}
</p>
