<template>
  <div id="app">
    <div class="mode-switch">
      <span :class="{ active: !isUploadMode }" @click="isUploadMode = false">
        粘贴代码模式
      </span>
      <span :class="{ active: isUploadMode }" @click="isUploadMode = true">
        上传文件模式
      </span>
    </div>

    <div class="main-wrapper">
      <div v-if="isUploadMode">
        <input type="file" ref="fileInput" @change="handleFileUpload" />
        <button @click="uploadFile" class="pretty-button">上传文件</button>
      </div>

      <div v-else>
        <AceEditor v-model="codeContent" />
        <div class="button-wrapper">
          <button @click="submitCode" class="pretty-button">提交代码</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import AceEditor from "../components/AceEditor.vue"; // 路径根据你实际位置改
import BASE_URL from "../config";
import { useResultStore } from "../stores/resultStore";

export default {
  components: {
    AceEditor,
  },
  setup() {
    const isUploadMode = ref(true);
    const fileInput = ref(null);
    //const responseMessage = ref(null);
    const codeContent = ref("# Write some Python code here...");
    const router = useRouter();
    const resultStore = useResultStore();
    const handleFileUpload = (event) => {
      const file = event.target.files[0];
      if (!file || file.type !== "text/x-python") {
        alert("请上传一个 Python 文件");
      }
    };

    const uploadFile = async () => {
      const file = fileInput.value.files[0];
      if (!file) {
        alert("请选择一个文件进行上传");
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      try {
        const res = await fetch(`${BASE_URL}/upload/file/`, {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        console.log(JSON.stringify(data, null, 2));
        // 切换到新页面，比如跳转到 /result
        resultStore.setResult(data);
        router.push("/result");
      } catch (e) {
        alert("上传失败");
        console.log(e);
      }
    };

    const submitCode = async () => {
      try {
        const res = await fetch(`${BASE_URL}/upload/code/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code: codeContent.value }),
        });
        const data = await res.json();
        console.log(JSON.stringify(data, null, 2));
        //responseMessage.value = JSON.stringify(data, null, 2);

        // 切换到新页面，比如跳转到 /result
        resultStore.setResult(data);
        router.push("/result");
      } catch (e) {
        alert("提交失败");
      }
    };

    return {
      isUploadMode,
      fileInput,
      //responseMessage,
      handleFileUpload,
      uploadFile,
      codeContent,
      submitCode,
    };
  },
};
</script>

<style>
.main-wrapper {
  display: flex;
  justify-content: center;
  align-items: center; /* 可选：让它垂直居中 */
  margin-top: 100px; /* 可按需设置顶部间距 */
}
.mode-switch {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  background-color: white;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.mode-switch span {
  padding: 8px 16px;
  cursor: pointer;
  background-color: #f0f0f0;
  user-select: none;
  transition: background-color 0.3s, color 0.3s;
}

.mode-switch span.active {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

.pretty-button {
  background-color: #4caf50; /* 绿色背景 */
  color: white; /* 白色文字 */
  padding: 12px 24px; /* 内边距 */
  font-size: 16px; /* 字体大小 */
  border: none; /* 无边框 */
  border-radius: 6px; /* 圆角 */
  cursor: pointer; /* 鼠标样式 */
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 阴影 */
}

.pretty-button:hover {
  background-color: #45a049; /* 鼠标悬浮更深的绿 */
  transform: translateY(-2px); /* 轻微上移动效 */
}

.pretty-button:active {
  background-color: #3e8e41; /* 按下时更深 */
  transform: translateY(0); /* 复位 */
}

.button-wrapper {
  display: flex;
  justify-content: center; /* 水平居中 */
  margin-top: 30px; /* 向下移动一点 */
}
</style>
