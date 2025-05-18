import { defineStore } from "pinia";

export const useResultStore = defineStore("result", {
  state: () => ({
    resultData: {},
  }),
  actions: {
    setResult(data) {
      this.resultData = data;
    },
  },
});
