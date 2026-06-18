<script lang="ts">
  interface Props {
    /** Maps keys (names) to values, both of which are displayed. */
    items: Map<string, string | null>;
  }

  const { items }: Props = $props();

  const visibleItems = $derived(
    [...items].filter(([, value]) => value !== null) as [string, string][],
  );
</script>

<!--
@component
Display arbitrary metadata.
-->
<section>
  {#if visibleItems.length > 0}
    <dl class="flex flex-wrap items-stretch gap-2">
      {#each visibleItems as [key, value] (key)}
        <div
          class="max-w-full min-w-0 rounded-field bg-base-200 px-3 py-2 shadow-sm md:max-w-80">
          <dt class="text-xs font-medium text-base-content/60">
            {key}
          </dt>
          <dd
            class="mt-0.5 min-w-0 text-sm font-semibold wrap-break-word text-base-content">
            {value}
          </dd>
        </div>
      {/each}
    </dl>
  {/if}
</section>
