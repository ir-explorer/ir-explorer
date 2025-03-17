<script lang="ts">
  import type { PageProps } from "./$types";
  import type { Corpus } from "$lib/types";

  let { data }: PageProps = $props();

  let selectedCorpus: Corpus | undefined = $state();
  let search: string = $state("");
  let target: string = $derived(
    selectedCorpus
      ? "/search/" +
          selectedCorpus.name +
          "?" +
          new URLSearchParams({ q: search })
      : "/"
  );
  let loading: boolean = $state(false);
</script>

<form>
  <select
    class="select"
    name="corpora"
    id="corpora"
    bind:value={selectedCorpus}
    onsubmit={() => (loading = true)}
    disabled={loading}
  >
    {#each data.corpora as corpus}
      <option value={corpus}>{corpus.name}</option>
    {/each}
  </select>
  <input class="input" type="text" bind:value={search} disabled={loading} />
  <a href={target}>
    <button
      class="btn"
      type="submit"
      disabled={search.trim().length == 0 || !selectedCorpus}
      onclick={() => (loading = true)}
    >
      <span class={[loading && "loading loading-infinity loading-sm"]}>🔍</span>
    </button>
  </a>
</form>
