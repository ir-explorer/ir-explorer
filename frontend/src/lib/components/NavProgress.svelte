<script lang="ts">
  import { afterNavigate, beforeNavigate } from "$app/navigation";
  import NProgress from "nprogress";
  import "nprogress/nprogress.css";

  NProgress.configure({ showSpinner: false });

  let timeout: number;
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
