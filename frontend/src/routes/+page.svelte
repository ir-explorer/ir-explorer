<script lang="ts">
  import type { PageProps } from "./$types";
  import type { Corpus } from "$lib/types";

  let { data }: PageProps = $props();

  let selected_corpus: Corpus | undefined = $state();
  let search: string = $state("");
  let target: string = $derived(
    selected_corpus
      ? "/search/" +
          selected_corpus.name +
          "?" +
          new URLSearchParams({ q: search })
      : "/"
  );
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
<input type="text" bind:value={search} />
<a href={target}>
  <button>search</button>
</a>
