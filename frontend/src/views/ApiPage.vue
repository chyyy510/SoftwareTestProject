<script setup>
import { useResultStore } from "../stores/resultStore";
import { ref, computed } from "vue";

const resultStore = useResultStore();
const ai = resultStore.resultData.ai;

const ai_error = resultStore.resultData.ai_error;

const grouped = ai_error
  ? {}
  : ai.reduce((acc, item) => {
      const funcName = item.function;
      if (!acc[funcName]) {
        acc[funcName] = [];
      }
      acc[funcName].push({
        inputs: item.inputs,
        expected: item.expected,
      });
      return acc;
    }, {});

const openFunctions = ref({}); // 用于保存每个函数是否展开

const toggleFunction = (funcName) => {
  openFunctions.value[funcName] = !openFunctions.value[funcName];
};

const isOpen = (funcName) => openFunctions.value[funcName];
function formatInput(inputs) {
  // 简单格式化数组，避免直接显示大量嵌套数组
  return JSON.stringify(inputs);
}

function formatOutput(output) {
  return JSON.stringify(output);
}
</script>

<template>
  <div class="intro-test">
    <p>
      该功能通过与百度云的 qianfan.ChatCompletion 接口交互， <br />利用
      ERNIE-3.5 模型分析 Python 函数代码，自动为每个函数生成3组测试用例。
      <br />每组包括输入参数和期望的输出结果，并返回以 JSON 格式表示的测试用例。
    </p>
  </div>
  <div>
    <el-card class="result-card">
      <h2 class="title">🎯 测试生成结果</h2>
      <!--解析成功-->
      <div v-if="!ai_error">
        <div
          v-for="(cases, funcName) in grouped"
          :key="funcName"
          class="function-block"
        >
          <el-card @click="toggleFunction(funcName)" shadow="hover">
            <h3 class="func-name">
              {{ isOpen(funcName) ? "▾🧠" : "▸" }}函数名：{{ funcName }}
            </h3>
          </el-card>

          <div v-if="isOpen(funcName)">
            <ul class="cases-list">
              <li v-for="(item, index) in cases" :key="index" class="case-item">
                <div>
                  <strong>输入：</strong
                  ><code>{{ formatInput(item.inputs[0]) }}</code>
                </div>
                <div>
                  <strong>期望输出：</strong
                  ><code>{{ formatOutput(item.expected) }}</code>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <!--解析失败-->
      <div v-else>
        <div>由于含有数组等特殊输入或其他原因，此处显示原始格式</div>
        <pre class="pretty-json">{{ ai }}</pre>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      inputValue: "",
    };
  },
};
</script>

<style scoped>
.intro-test {
  display: flex;
  flex-direction: column;
  align-items: center; /* 居中对齐 */
  justify-content: top;
  text-align: center;
}

p {
  font-size: 1rem;
  margin-bottom: 30px;
  color: #6e3d3d;
  line-height: 30px;
}

textarea {
  padding: 10px;
  font-size: 1rem;
  width: 400px;
  height: 200px; /* 固定高度 */
  background-color: black; /* 黑色背景 */
  color: white; /* 白色文字 */
  border: 2px solid #333; /* 深灰色边框 */
  font-family: "Courier New", Courier, monospace; /* 使用等宽字体 */
  resize: none; /* 禁止手动调整大小 */
  overflow: auto; /* 内容溢出时显示滚动条 */
}

.result-card {
  max-width: 900px;
  margin: 40px auto;
  padding: 20px;
}
.func-block {
  margin-bottom: 30px;
}
.tag-item {
  margin: 4px 6px 4px 0;
}
.group-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 8px; /* 行间距 */
}
.group-table tr {
  background: #fafafa;
  border-radius: 6px;
  /* 让单元格带圆角需要用 display block */
  display: table-row;
}
.group-table td {
  padding: 8px 12px;
  vertical-align: middle;
}
.var-name {
  width: 80px;
  font-weight: 600;
  color: #303133;
  user-select: text;
}
.section-row {
  display: flex;
  gap: 0px;
}

.section-row > .el-col {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.section-row > .el-col > .el-card {
  flex: 1; /* 让卡片撑满父容器高度 */
  display: flex;
  flex-direction: column;
}

.el-card > .el-card__body {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.result-card {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px 30px;
  background-color: #fff;
  box-shadow: 0 4px 14px rgb(0 0 0 / 0.1);
  border-radius: 12px;
}

.title {
  font-weight: 700;
  font-size: 1.8rem;
  color: #409eff; /* Element Plus 主色 */
  margin-bottom: 24px;
  text-align: center;
  user-select: none;
}

.function-block {
  margin-bottom: 30px;
  padding: 18px 20px;
  border: 1px solid #e4e7ed;
  border-radius: 10px;
  background-color: #f9fbfd;
  transition: background-color 0.3s ease;
}

.function-block:hover {
  background-color: #e6f0ff;
}

.func-name {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: #303133;
  user-select: text;
  border-bottom: 2px solid #409eff;
  padding-bottom: 6px;
}

.cases-list {
  list-style-type: none;
  padding-left: 0;
}

.case-item {
  background: #fff;
  border-radius: 8px;
  padding: 12px 15px;
  margin-bottom: 12px;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
  font-size: 1rem;
  line-height: 1.5;
}

.case-item strong {
  color: #606266;
}

.case-item code {
  background-color: #f0f4f8;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: "Courier New", Courier, monospace;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
<style scoped>
.pretty-json {
  background-color: #f5f5f5;
  color: #333;
  padding: 10px 15px;
  border-radius: 5px;
  font-family: Consolas, "Courier New", monospace;
  font-size: 14px;
  white-space: pre-wrap; /* 自动换行 */
  word-break: break-word;
  max-height: 400px;
  overflow-y: auto;
}
</style>
