import { defineConfig } from "vite";

const isCI = process.env.GITHUB_ACTIONS === "true";
const repositoryName = process.env.GITHUB_REPOSITORY?.split("/")[1];
const ciBase = repositoryName ? `/${repositoryName}/` : "/";
const base = process.env.VITE_BASE_PATH ?? (isCI ? ciBase : "/");

export default defineConfig({
  base,
  test: {
    environment: "jsdom",
    setupFiles: "./src/test/setup.js"
  }
});
