<script lang="ts">
  import { page } from "$app/state";
  import { browseIcon, closeMenuIcon, menuIcon, searchIcon } from "$lib/icons";
  import type { SearchOptions, SearchSettings } from "$lib/types";
  import Fa from "svelte-fa";
  import Logo from "./Logo.svelte";

  interface Props {
    /** The search options (available options for each). */
    searchOptions: SearchOptions;
    /** The bindable chosen search settings. */
    searchSettings: SearchSettings;
  }

  let { searchOptions, searchSettings = $bindable() }: Props = $props();

  const languageInit = "English";

  let atSearch: boolean = $derived(
    page.url.pathname.startsWith("/search") || page.url.pathname == "/",
  );
  let atBrowse: boolean = $derived(page.url.pathname.startsWith("/browse"));
</script>

<!--
@component
The main menu drawer.
-->
<div class="drawer w-auto">
  <input id="my-drawer" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content">
    <label for="my-drawer" class="drawer-button btn btn-ghost btn-sm">
      <Fa icon={menuIcon} />
    </label>
  </div>
  <div class="drawer-side z-99">
    <label for="my-drawer" aria-label="close sidebar" class="drawer-overlay"
    ></label>
    <div class="menu min-h-full w-80 bg-base-200 p-4 text-base-content">
      <div class="flex w-full items-center gap-4">
        <label for="my-drawer" class="drawer-button btn btn-ghost btn-sm">
          <Fa icon={closeMenuIcon} />
        </label>
        <Logo small />
      </div>

      <div class="divider my-2"></div>

      <ul class="menu w-full p-0">
        <!-- Sidebar content here -->
        <li>
          <a
            class={[atSearch && "menu-active pointer-events-none", "px-0"]}
            href="/search">
            <Fa icon={searchIcon} class="mx-2 w-4" />Search
          </a>
        </li>
        <li>
          <a
            class={[atBrowse && "menu-active pointer-events-none", "px-0"]}
            href="/browse">
            <Fa icon={browseIcon} class="mx-2 w-4" />Browse
          </a>
        </li>
      </ul>

      <div class="divider my-2"></div>

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
