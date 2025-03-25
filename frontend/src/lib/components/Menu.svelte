<script lang="ts">
  import { page } from "$app/state";
  import { menuIcon, searchIcon, browseIcon } from "$lib/icons";
  import Fa from "svelte-fa";

  let atSearch: boolean = $derived(
    page.url.pathname === "/" || page.url.pathname.startsWith("/search")
  );
  let atBrowse: boolean = $derived(page.url.pathname.startsWith("/browse"));
</script>

<div class="dropdown">
  <div
    tabindex="0"
    role="button"
    class="btn border-none bg-transparent h-8 w-8"
  >
    <Fa icon={menuIcon} />
  </div>
  <ul class="dropdown-content menu w-40 bg-base-200 mt-2 rounded-box shadow">
    <li>
      <a href="/" class={[atSearch && "menu-active"]}
        ><span class="w-4 mr-4 flex justify-center"
          ><Fa icon={searchIcon} /></span
        >Search</a
      >
    </li>
    <li>
      <a href="/browse" class={[atBrowse && "menu-active"]}
        ><span class="w-4 mr-4 flex justify-center"
          ><Fa icon={browseIcon} /></span
        >Browse</a
      >
    </li>
  </ul>
</div>
