import { get_corpora } from "$lib/server/backend";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async () => {
  return { corpora: await get_corpora() };
};
