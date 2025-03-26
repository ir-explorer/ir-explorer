<script lang="ts">
  import { page } from "$app/state";
  import { menuIcon, searchIcon, browseIcon } from "$lib/icons";
  import Fa from "svelte-fa";

  let atSearch: boolean = $derived(page.url.pathname.startsWith("/search"));
  let atBrowse: boolean = $derived(page.url.pathname.startsWith("/browse"));
</script>

<div class="dropdown">
  <div
    tabindex="0"
    role="button"
    class="w-8 h-8 bg-transparent border-none btn"
  >
    <Fa icon={menuIcon} />
  </div>
  <div class="w-40 mt-2 shadow dropdown-content bg-base-200 rounded-box">
    <ul class="w-full menu">
      <li>
        <a href="/" class={[atSearch && "menu-active"]}
          ><span class="flex justify-center w-4 mr-4"
            ><Fa icon={searchIcon} /></span
          >Search</a
        >
      </li>
      <li>
        <a href="/browse" class={[atBrowse && "menu-active"]}
          ><span class="flex justify-center w-4 mr-4"
            ><Fa icon={browseIcon} /></span
          >Browse</a
        >
      </li>
    </ul>
  </div>
</div>
