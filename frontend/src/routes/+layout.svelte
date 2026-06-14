<script lang="ts">
  import IconWithText from "$lib/components/IconWithText.svelte";
  import NavProgress from "$lib/components/NavProgress.svelte";
  import { selectedOptions } from "$lib/options.svelte";
  import { faGithub } from "@fortawesome/free-brands-svg-icons";
  import { untrack } from "svelte";
  import "../app.css";
  import type { LayoutProps } from "./$types";

  const { data, children }: LayoutProps = $props();
  const defaultOptions = untrack(() => data.defaultOptions);

  // if values are missing, fall back to defaults
  if (selectedOptions.queryLanguage === null) {
    selectedOptions.queryLanguage = defaultOptions.queryLanguage;
  }
  if (selectedOptions.modelName === null) {
    selectedOptions.modelName = defaultOptions.modelName;
  }
</script>

<svelte:head>
  <title>IR explorer</title>
</svelte:head>

<NavProgress />
<div
  class="grid max-h-full min-h-screen w-screen max-w-full grid-rows-[1fr_auto]">
  <div>
    {@render children()}
  </div>

  <footer
    class="flex w-full flex-col justify-between gap-2 border-t border-base-300 bg-base-100 px-4 py-2 text-sm text-base-content/65 md:flex-row md:items-center">
    <a
      class="inline-flex w-fit items-center text-base-content/75 hover:text-base-content"
      href="https://github.com/ir-explorer">
      <IconWithText icon={faGithub} text="ir-explorer" />
    </a>
    <p>
      Made with
      <a
        class="link text-base-content/75 link-hover"
        href="https://www.paradedb.com/">
        ParadeDB</a
      >,
      <a
        class="link text-base-content/75 link-hover"
        href="https://litestar.dev/">
        Litestar</a
      >, and
      <a
        class="link text-base-content/75 link-hover"
        href="https://svelte.dev/">
        SvelteKit</a
      >.
    </p>
  </footer>
</div>
