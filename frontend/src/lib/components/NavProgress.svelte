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
