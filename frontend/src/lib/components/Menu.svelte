<script lang="ts">
  import { page } from "$app/state";
  import { menuIcon, searchIcon, browseIcon } from "$lib/icons";
  import Fa from "svelte-fa";

  let atSearch: boolean = $derived(page.url.pathname.startsWith("/search"));
  let atBrowse: boolean = $derived(page.url.pathname.startsWith("/browse"));
</script>

<div class="dropdown">
  <div tabindex="0" role="button" class="btn h-8 w-8 btn-ghost">
    <Fa icon={menuIcon} />
  </div>
  <div class="dropdown-content mt-2 w-40 rounded-box bg-base-200 shadow">
    <ul class="menu w-full">
      <li>
        <a href="/" class={[atSearch && "menu-active"]}
          ><span class="mr-4 flex w-4 justify-center"
            ><Fa icon={searchIcon} /></span
          >Search</a>
      </li>
      <li>
        <a href="/browse" class={[atBrowse && "menu-active"]}
          ><span class="mr-4 flex w-4 justify-center"
            ><Fa icon={browseIcon} /></span
          >Browse</a>
      </li>
    </ul>
  </div>
</div>
