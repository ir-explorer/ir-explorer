<script lang="ts">
  import NavProgress from "$lib/components/NavProgress.svelte";
  import { faGithub } from "@fortawesome/free-brands-svg-icons";
  import { Fa } from "svelte-fa";
  import "../app.css";

  let { data, children } = $props();
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
    class="flex w-full flex-row items-center justify-between border-t border-base-300 bg-base-200 px-8 py-2 text-sm">
    <p>
      © {data.currentYear}
    </p>
    <a href="https://github.com/mrjleo/ir-explorer" class="hover:scale-125">
      <Fa icon={faGithub} />
    </a>
  </footer>
</div>
