<script lang="ts">
  import { page } from "$app/state";
  import Alert from "$lib/components/Alert.svelte";
  import MetaDisplay from "$lib/components/browse/MetaDisplay.svelte";
  import PaginatedList from "$lib/components/browse/PaginatedList.svelte";
  import TextDisplay from "$lib/components/browse/TextDisplay.svelte";
  import { documentIcon, queryIcon } from "$lib/icons";
  import { selectedOptions } from "$lib/options.svelte";
  import type {
    OrderByOption,
    Paginated,
    Query,
    RelevantDocument,
  } from "$lib/types";
  import { truncate } from "$lib/util";
  import Fa from "svelte-fa";
  import type { PageProps } from "./$types";

  let { data }: PageProps = $props();

  // query list
  async function getQueriesPage(
    match: string | null,
    orderBy: string | null,
    desc: boolean,
    numItems: number,
    offset: number,
  ) {
    const searchParams = new URLSearchParams({
      corpusName: page.params.corpusName,
      datasetName: page.params.datasetName,
      desc: desc.toString(),
      numResults: numItems.toString(),
      offset: offset.toString(),
    });
    if (match !== null) {
      searchParams.append("match", match);
    }
    if (orderBy !== null) {
      searchParams.append("orderBy", orderBy);
    }

    const res = await fetch("/api/queries?" + searchParams);
    return (await res.json()) as Paginated<Query>;
  }
  const orderQueriesOptions = [
    { name: "Relevant documents", option: "relevant_documents" },
    { name: "Length", option: "length" },
    { name: "Match", option: "match_score" },
  ] as OrderByOption[];

  // relevant document list
  async function getDocumentsPage(
    match: string | null,
    orderBy: string | null,
    desc: boolean,
    numItems: number,
    offset: number,
  ) {
    const searchParams = new URLSearchParams({
      queryId: data.query !== null ? data.query.id : "",
      datasetName: page.params.datasetName,
      corpusName: page.params.corpusName,
      numResults: numItems.toString(),
      offset: offset.toString(),
      desc: desc.toString(),
    });
    if (match !== null) {
      searchParams.append("match", match);
    }
    if (orderBy !== null) {
      searchParams.append("orderBy", orderBy);
    }

    const res = await fetch("/api/relevantDocuments?" + searchParams);
    return (await res.json()) as Paginated<RelevantDocument>;
  }
  const orderRelevantDocumentsOptions = [
    { name: "Relevance", option: "relevance" },
    { name: "Length", option: "document_length" },
    { name: "Match", option: "document_match_score" },
  ] as OrderByOption[];
</script>

{#if page.url.searchParams.get("queryId") !== null && data.query === null}
  <Alert text={"Query not found."} />
{:else if data.query !== null}
  <!-- display selected query -->
  <MetaDisplay
    items={new Map([
      ["Corpus", data.query.corpusName],
      ["Dataset", data.query.datasetName],
      ["Query ID", data.query.id],
      ["Description", data.query.description],
      [
        "Number of relevant documents",
        data.query.numRelevantDocuments.toString(),
      ],
    ])} />
  <TextDisplay text={data.query.text} />

  {#if data.query.numRelevantDocuments > 0}
    <!-- display relevant documents for selected query -->
    <PaginatedList
      getPage={getDocumentsPage}
      getTargetLink={(d: RelevantDocument) =>
        `/browse/${page.params.corpusName}?${new URLSearchParams({ documentId: d.id })}`}
      orderByOptions={orderRelevantDocumentsOptions}>
      {#snippet headTitle()}
        <p class="my-auto">Relevant documents</p>
      {/snippet}
      {#snippet item(d: RelevantDocument)}
        <div class="flex flex-col gap-2">
          <div class="flex flex-row items-center justify-between">
            <p class="badge font-thin">
              <Fa icon={documentIcon} />
              {d.id}
            </p>
            <p class="badge badge-sm badge-secondary">
              Relevance: {d.relevance}
            </p>
          </div>
          <p>{truncate(d.text, selectedOptions.snippetLength)}</p>
        </div>
      {/snippet}
    </PaginatedList>
  {/if}
{:else}
  <!-- display query list -->
  <PaginatedList
    getPage={getQueriesPage}
    getTargetLink={(q: Query) =>
      `/browse/${page.params.corpusName}/${page.params.datasetName}?${new URLSearchParams({ queryId: q.id })}`}
    orderByOptions={orderQueriesOptions}
    goToTarget={`/browse/${page.params.corpusName}/${page.params.datasetName}`}
    goToName="queryId">
    {#snippet headTitle()}
      <p class="my-auto">Queries</p>
    {/snippet}
    {#snippet item(q: Query)}
      <div class="flex flex-col gap-2">
        <div class="flex flex-row items-center justify-between">
          <p class="badge font-thin"><Fa icon={queryIcon} /> {q.id}</p>
          {#if q.numRelevantDocuments > 0}
            <p class="badge badge-sm badge-secondary">
              {q.numRelevantDocuments} relevant
              {q.numRelevantDocuments == 1 ? "document" : "documents"}
            </p>
          {/if}
        </div>
        <p>{truncate(q.text, selectedOptions.snippetLength)}</p>
      </div>
    {/snippet}
  </PaginatedList>
{/if}
