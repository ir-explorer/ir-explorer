<script lang="ts">
  import { page } from "$app/state";
  import {
    MAX_ITEMS_PER_PAGE,
    MAX_RAG_DOCUMENTS,
    MAX_SNIPPET_LENGTH,
  } from "$lib/config";
  import { browseIcon, closeMenuIcon, menuIcon, searchIcon } from "$lib/icons";
  import { selectedOptions } from "$lib/options.svelte";
  import type { AvailableOptions } from "$lib/types";
  import Fa from "svelte-fa";
  import IconWithText from "./IconWithText.svelte";
  import Logo from "./Logo.svelte";

  interface Props {
    /** All available options. */
    availableOptions: AvailableOptions;
  }
  const { availableOptions }: Props = $props();

  const atSearch: boolean = $derived(
    page.url.pathname.startsWith("/search") || page.url.pathname == "/",
  );
  const atBrowse: boolean = $derived(page.url.pathname.startsWith("/browse"));
</script>

<!--
@component
The main menu drawer.
-->
<div class="drawer w-auto">
  <input id="main-menu" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content">
    <label for="main-menu" class="drawer-button btn btn-ghost btn-sm">
      <Fa icon={menuIcon} />
    </label>
  </div>
  <div class="drawer-side z-99">
    <label for="main-menu" class="drawer-overlay"></label>
    <div class="menu min-h-full w-80 bg-base-200 p-4 text-base-content">
      <div class="flex w-full items-center gap-4">
        <label for="main-menu" class="drawer-button btn btn-ghost btn-sm">
          <Fa icon={closeMenuIcon} />
        </label>
        <Logo small />
      </div>

      <div class="divider my-2"></div>

      <!-- navigation -->
      <ul class="menu w-full p-0">
        <li>
          <a
            class={[atSearch && "pointer-events-none menu-active"]}
            href="/search">
            <IconWithText icon={searchIcon} text="Search" wide />
          </a>
        </li>
        <li>
          <a
            class={[atBrowse && "pointer-events-none menu-active"]}
            href="/browse">
            <IconWithText icon={browseIcon} text="Browse" wide />
          </a>
        </li>
      </ul>

      <div class="divider my-2"></div>

      <!-- search settings -->
      <fieldset class="fieldset gap-4">
        <legend class="fieldset-legend">Search</legend>

        <label class="fieldset-label flex flex-col items-start">
          Query language
          <select
            class="select w-full select-sm"
            name="language"
            bind:value={selectedOptions.queryLanguage}>
            {#each availableOptions.queryLanguages as language}
              <option value={language}>{language}</option>
            {/each}
          </select>
        </label>

        {#if availableOptions.corpusNames.length > 0}
          <label class="fieldset-label flex flex-col items-start">
            Search only in
            <div
              id="filter-corpora"
              class="menu w-full gap-2 rounded-box border border-base-300 bg-base-100 text-sm">
              {#each availableOptions.corpusNames as corpusName}
                <label>
                  <input
                    type="checkbox"
                    class="toggle mr-2 toggle-sm"
                    value={corpusName}
                    bind:group={selectedOptions.corpusNames}
                    name="corpus" />
                  {corpusName}
                </label>
              {/each}
            </div>
          </label>
        {/if}
      </fieldset>

      <div class="my-2"></div>

      <!-- browse settings -->
      <fieldset class="fieldset gap-4">
        <legend class="fieldset-legend">Browse</legend>

        <label class="fieldset-label flex flex-col items-start">
          <div class="flex w-full flex-row justify-between">
            <span>Items per page</span>
            <span class="pr-2">{selectedOptions.itemsPerPage}</span>
          </div>
          <input
            type="range"
            min="1"
            max={MAX_ITEMS_PER_PAGE}
            bind:value={selectedOptions.itemsPerPage}
            class="range range-sm" />
        </label>

        <label class="fieldset-label flex flex-col items-start">
          <div class="flex w-full flex-row justify-between">
            <span>Snippet length</span>
            <span class="pr-2">{selectedOptions.snippetLength}</span>
          </div>
          <input
            type="range"
            min="0"
            max={MAX_SNIPPET_LENGTH}
            bind:value={selectedOptions.snippetLength}
            class="range range-sm" />
        </label>

        {#if availableOptions.modelNames.length > 0}
          <fieldset class="fieldset gap-4">
            <legend class="fieldset-legend">Generation</legend>
            <label class="fieldset-label flex flex-col items-start">
              LLM
              <select
                class="select w-full select-sm"
                name="model"
                bind:value={selectedOptions.modelName}>
                {#each availableOptions.modelNames as modelName}
                  <option value={modelName}>{modelName}</option>
                {/each}
              </select>
            </label>

            <label class="fieldset-label flex flex-col items-start">
              <div class="flex w-full flex-row justify-between">
                <span>Number of documents (RAG)</span>
                <span class="pr-2">{selectedOptions.numRagDocuments}</span>
              </div>
              <input
                type="range"
                min="1"
                max={MAX_RAG_DOCUMENTS}
                bind:value={selectedOptions.numRagDocuments}
                class="range range-sm" />
            </label>
          </fieldset>
        {/if}
      </fieldset>
    </div>
  </div>
</div>
