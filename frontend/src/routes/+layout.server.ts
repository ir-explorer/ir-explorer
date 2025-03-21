import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async () => {
  return { currentYear: new Date().getFullYear() };
};
