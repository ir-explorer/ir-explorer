import { get_datasets } from "$lib/server/backend";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
  return { datasets: await get_datasets(params.corpus) };
};
