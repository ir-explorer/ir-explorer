<script lang="ts">
  import { menuIcon } from "$lib/icons";
  import type { SearchOptions, SearchSettings } from "$lib/types";
  import Fa from "svelte-fa";
  import Logo from "./Logo.svelte";

  let {
    searchOptions,
    searchSettings = $bindable(),
  }: {
    searchOptions: SearchOptions;
    searchSettings: SearchSettings;
  } = $props();

  const languageInit = "English";
</script>

<div class="drawer">
  <input id="my-drawer" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content">
    <label for="my-drawer" class="drawer-button btn btn-ghost btn-sm">
      <Fa icon={menuIcon} />
    </label>
  </div>
  <div class="drawer-side z-99">
    <label for="my-drawer" aria-label="close sidebar" class="drawer-overlay"
    ></label>
    <div class="menu min-h-full w-80 gap-4 bg-base-200 p-4 text-base-content">
      <div class="flex w-full gap-4">
        <label for="my-drawer" class="drawer-button btn btn-ghost btn-sm">
          <Fa icon={menuIcon} />
        </label>
        <a href="/">
          <Logo />
        </a>
      </div>

      <fieldset class="fieldset gap-2">
        <legend class="fieldset-legend">Search settings</legend>

        <label class="fieldset-label flex flex-col items-start">
          Query language
          <select
            class="select w-full select-sm"
            name="language"
            value={languageInit}>
            {#each searchOptions.queryLanguages as language}
              <option value={language}>{language}</option>
            {/each}
          </select>
        </label>

        <label
          for="filter-corpora"
          class="fieldset-label flex flex-col items-start">
          Search only in
        </label>
        <div
          id="filter-corpora"
          class="menu w-full gap-2 rounded-box border border-base-300 bg-base-100 text-sm">
          {#each searchOptions.corpusNames as corpusName}
            <label>
              <input
                type="checkbox"
                class="toggle mr-2 toggle-sm"
                value={corpusName}
                bind:group={searchSettings.corpusNames}
                name="corpus" />
              {corpusName}
            </label>
          {/each}
        </div>
      </fieldset>
    </div>
  </div>
</div>
