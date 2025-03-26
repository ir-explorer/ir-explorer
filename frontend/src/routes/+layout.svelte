<script lang="ts">
  import "../app.css";
  import { Fa } from "svelte-fa";
  import { faGithub } from "@fortawesome/free-brands-svg-icons";

  let { data, children } = $props();
</script>

<svelte:head>
  <title>IR explorer</title>
</svelte:head>

<div class="w-screen h-screen max-w-full max-h-full grid grid-rows-[1fr_auto]">
  <div>
    {@render children()}
  </div>

  <footer
    class="flex flex-row items-center justify-between w-full px-8 py-2 text-sm border-t opacity-50 border-base-300 bg-base-200/75"
  >
    <p>
      © {data.currentYear}
    </p>
    <a href="https://github.com/mrjleo/ir-explorer" class="hover:scale-125">
      <Fa icon={faGithub} />
    </a>
  </footer>
</div>
