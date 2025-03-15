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

<form>
  <select
    class="select"
    name="corpora"
    id="corpora"
    bind:value={selected_corpus}
  >
    {#each data.corpora as corpus}
      <option value={corpus}>{corpus.name}</option>
    {/each}
  </select>
  <input class="input" type="text" bind:value={search} />
  <a href={target}>
    <button class="btn" type="submit">🔍</button>
  </a>
</form>
