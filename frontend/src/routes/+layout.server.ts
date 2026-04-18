import { getAvailableOptions } from "$lib/server/backend";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async () => {
  const availableOptions = await getAvailableOptions();

  return {
    availableOptions,
    defaultOptions: {
      queryLanguage: availableOptions.queryLanguages[0] ?? null,
      modelName: availableOptions.modelNames[0] ?? null,
    },
  };
};
