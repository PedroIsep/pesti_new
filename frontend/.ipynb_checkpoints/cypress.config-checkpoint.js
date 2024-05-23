import { defineConfig } from "cypress";

export default defineConfig({
  projectId: "tc1byz",
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
