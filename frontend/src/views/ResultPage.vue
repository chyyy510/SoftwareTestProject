<script setup>
import { useResultStore } from "../stores/resultStore";
import { ref } from "vue";

const resultStore = useResultStore();
const result = resultStore.resultData.ours;
const openFunctions = ref({}); // 用于保存每个函数是否展开

const toggleFunction = (funcName) => {
  openFunctions.value[funcName] = !openFunctions.value[funcName];
};

const isOpen = (funcName) => openFunctions.value[funcName];
</script>

<template>
  <div class="background-container">
  </div>
  <el-card class="result-card">
    <h2>🎯 测试生成结果</h2>

    <div
      v-for="(funcResult, funcName) in result"
      :key="funcName"
      class="func-block"
    >
      <el-card
        @click="toggleFunction(funcName)"
        shadow="hover"
        class="func-header"
      >
        <h3>{{ isOpen(funcName) ? "▾🧠" : "▸" }}函数名：{{ funcName }}</h3>
      </el-card>

      <!-- 每一段信息用 el-card 展示 -->
      <div v-if="isOpen(funcName)" class="function-body">
        <el-row :gutter="20" class="section-row">
          <el-col :span="12">
            <el-card shadow="hover" header="📌 初始条件">
              <div v-for="item in funcResult.initial" :key="item">
                <el-tag type="info" class="tag">{{ item }}</el-tag>
              </div>
            </el-card>
          </el-col>

          <el-col :span="12">
            <el-card shadow="hover" header="🔍 解析后条件">
              <div v-for="item in funcResult.parse" :key="item">
                <el-tag type="success" class="tag">{{ item }}</el-tag>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-row :gutter="20" class="section-row">
          <el-col :span="12">
            <el-card shadow="hover" header="📚 分组约束">
              <div v-for="(conds, varName) in funcResult.group" :key="varName">
                <strong>{{ varName }}：</strong>
                <ul>
                  <li v-for="c in conds" :key="c">{{ c }}</li>
                </ul>
              </div>
            </el-card>
          </el-col>

          <el-col :span="12">
            <el-card shadow="hover" header="🧪 条件测试样例">
              <div v-for="(vals, param) in funcResult.condition" :key="param">
                <strong>{{ param }}：</strong>
                <div style="margin-top: 4px">
                  <el-tag
                    v-for="val in vals"
                    :key="JSON.stringify(val)"
                    type="warning"
                    class="tag"
                  >
                    {{ JSON.stringify(val) }}
                  </el-tag>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-card shadow="hover" header="所有组合">
          <div v-for="item in funcResult.final" :key="item">
            <el-tag type="success" class="tag">{{ item }}</el-tag>
          </div>
        </el-card>

        <el-card shadow="hover" header="🎉 满足最终条件组合总数">
          <el-tag type="danger" size="large">{{
            funcResult.total || 0
          }}</el-tag>
        </el-card>
      </div>
    </div>
  </el-card>
</template>
<style scoped>
.background-container{
  background-image: url('../assets/images/background/6.jpg'); /* 设置背景图片 */
    background-size: cover; /* 背景图像填充整个容器 */
    background-position: center; /* 背景图像居中 */
    background-repeat: no-repeat; /* 禁止背景图像重复 */
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
</style>
