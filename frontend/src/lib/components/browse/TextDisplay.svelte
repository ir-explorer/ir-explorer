<script lang="ts">
  interface Props {
    /** The title to render. */
    title: string;
    /** The text to render. */
    text: string;
  }

  let { title, text }: Props = $props();
</script>

<!--
@component
Display a query or document text in a scrollable component.
-->
<fieldset class="fieldset rounded-box border border-base-300 px-4 pb-2 shadow">
  <legend class="fieldset-legend">{title}</legend>
  <div
    class="max-h-128 overflow-y-scroll text-sm leading-relaxed whitespace-pre-wrap">
    {text}
  </div>
</fieldset>
