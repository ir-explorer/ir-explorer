<script lang="ts">
  interface Props {
    /** The title to render. */
    title?: string;
    /** Maps keys (names) to values, both of which are displayed. */
    items: Map<string, string | null>;
  }

  let { title = "Metadata", items }: Props = $props();
</script>

<!--
@component
Display arbitrary metadata.
-->
<fieldset class="fieldset rounded-box border border-base-300 px-4 pb-2 shadow">
  <legend class="fieldset-legend mb-0 p-0">{title}</legend>
  {#each [...items] as [key, value]}
    <div>
      <label for={key} class="label">{key}</label>
      <p id={key}>{value ?? "(none)"}</p>
    </div>
  {/each}
</fieldset>
