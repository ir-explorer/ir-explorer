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
    class="w-full flex flex-row justify-between items-center text-sm px-8 py-2 border-t border-base-300 bg-base-200/75 opacity-50"
  >
    <p>
      © {data.currentYear}
    </p>
    <a href="https://github.com/mrjleo/ir-explorer" class="hover:scale-125">
      <Fa icon={faGithub} />
    </a>
  </footer>
</div>
