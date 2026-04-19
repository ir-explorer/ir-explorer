import js from "@eslint/js";
import prettier from "eslint-config-prettier";
import svelte from "eslint-plugin-svelte";
import globals from "globals";
import ts from "typescript-eslint";
import svelteConfig from "./svelte.config.js";

export default ts.config(
  {
    ignores: ["build/", ".svelte-kit/", "node_modules/"],
  },
  js.configs.recommended,
  ...ts.configs.recommended,
  ...svelte.configs["flat/recommended"],
  prettier,
  ...svelte.configs["flat/prettier"],
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    rules: {
      "svelte/no-at-html-tags": "off",
      "svelte/no-navigation-without-resolve": "off",
      "svelte/prefer-svelte-reactivity": "off",
      "svelte/require-each-key": "off",
    },
  },
  {
    files: ["**/*.svelte", "**/*.svelte.js", "**/*.svelte.ts"],
    languageOptions: {
      parserOptions: {
        extraFileExtensions: [".svelte"],
        parser: ts.parser,
        svelteConfig,
      },
    },
  },
);
