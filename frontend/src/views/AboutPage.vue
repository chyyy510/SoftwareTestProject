<template>
    <div class="intro-test">
      <p>该功能通过与百度云的 qianfan.ChatCompletion 接口交互，
          <br>利用 ERNIE-3.5 模型分析 Python 函数代码，自动为每个函数生成3组测试用例。
          <br>每组包括输入参数和期望的输出结果，并返回以 JSON 格式表示的测试用例。
      </p>
      <textarea id="outputField" v-model="inputValue"></textarea>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        inputValue: ''
      };
    }
  };
  </script>
  
  <style scoped>
.background-container{

}
.intro-test {
    display: flex;
    flex-direction: column;
    align-items: center; /* 居中对齐 */
    justify-content: top;
    text-align: center;
    min-height: 100vh;
  /* 背景图片的路径 */
  background-image: url('../assets/images/background/6.jpg'); 
  background-size: cover; /* 背景图片铺满整个容器 */
  background-position: center; /* 背景图片居中 */
  background-repeat: no-repeat; /* 背景图片不重复 */

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
    font-family: 'Courier New', Courier, monospace; /* 使用等宽字体 */
    resize: none; /* 禁止手动调整大小 */
    overflow: auto; /* 内容溢出时显示滚动条 */
  }
  </style>
  