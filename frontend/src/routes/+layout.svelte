<script lang="ts">
  import "../app.css";
  let { children } = $props();
</script>

<div class="w-screen h-screen max-w-full">
  {@render children()}
</div>
