<script setup>
import { useResultStore } from "../stores/resultStore";

const resultStore = useResultStore();

console.log("结果数据：", resultStore.resultData);
</script>

<template>
  <div>
    <h2>上传结果展示</h2>
    <pre>{{ JSON.stringify(resultStore.resultData, null, 2) }}</pre>
  </div>
</template>
