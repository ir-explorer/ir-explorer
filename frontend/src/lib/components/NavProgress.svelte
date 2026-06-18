<script lang="ts">
  import { afterNavigate, beforeNavigate } from "$app/navigation";
  import NProgress from "nprogress";
  import "nprogress/nprogress.css";

  NProgress.configure({ showSpinner: false });

  let timeout: ReturnType<typeof setTimeout>;
  beforeNavigate(() => {
    timeout = setTimeout(NProgress.start, 200);
  });

  afterNavigate(() => {
    clearTimeout(timeout);
    NProgress.done();
  });
</script>

<!--
@component
A progress indicator displayed when the app navigates.

Only shown if navigation takes more than 200ms.
-->

<style>
  :global(#nprogress .bar) {
    background: var(--color-primary);
    height: 2px;
  }

  :global(#nprogress .peg) {
    box-shadow:
      0 0 10px var(--color-primary),
      0 0 5px var(--color-primary);
  }
</style>
