<script lang="ts">
  import type { PageProps } from "./$types";
  import type { Corpus } from "$lib/types";

  let { data }: PageProps = $props();

  let selectedCorpus: Corpus | undefined = $state();
  let selectedCorpusName: string = $derived(
    selectedCorpus ? selectedCorpus.name : ""
  );
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

<div class="flex flex-col w-full h-full items-center justify-center">
  <h1 class="text-6xl m-8">IR Explorer</h1>
  <form class="flex flex-col gap-2">
    <div class="flex flex-row gap-2 items-center">
      <div class="dropdown">
        <div
          tabindex="0"
          role="button"
          class="btn text-lg/tight rounded-full w-8 h-8"
        >
          ⛭
        </div>
        <div
          class="dropdown-content card card-border mt-2 bg-base-100 border-base-300 shadow"
        >
          <div class="card-body">
            <fieldset class="fieldset">
              <legend class="fieldset-legend">Settings</legend>
              <label class="fieldset-label">Corpus</label>
              <select
                class="select select-sm w-48"
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
            </fieldset>
          </div>
        </div>
      </div>
      <label class="input w-xl">
        <input
          type="text"
          placeholder="Search..."
          bind:value={search}
          disabled={loading}
        />
        <span class="label">{selectedCorpusName}</span>
      </label>
      <a href={target}>
        <button
          class="btn w-16"
          type="submit"
          disabled={search.trim().length == 0 || !selectedCorpus}
          onclick={() => (loading = true)}
        >
          <span class={[loading && "loading loading-infinity loading-sm"]}
            >🔍</span
          >
        </button>
      </a>
    </div>
  </form>
</div>
