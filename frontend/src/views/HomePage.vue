<template>
  <div class="home-container">
    <!--将fade in 应用到标题-->
    <h1 class="fade-in">欢迎来到测试样例生成系统</h1>
    <p>这是一个基于静态分析的 Python 代码测试样例生成系统，
      <br>旨在帮助开发人员自动生成针对 Python 代码的各种测试样例.</p>
     <!-- 使用 Flexbox 来并排显示图片和按钮 -->
     <div class="content-container">
      <div class="image-container">
        <img src="../assets/images/cats/blue_cono.png" alt="示例图片" class="home-image" />
      </div>
      <div class="button-container">
        <router-link to="/upload">
          <button>由此上传 Python 文件</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 100px;
  text-align: center;
  min-height: 100vh;
  background-image: url('../assets/images/background/6.jpg'); /* 设置背景图片 */
  background-size: cover; /* 背景图像填充整个容器 */
  background-position: center; /* 背景图像居中 */
  background-repeat: no-repeat; /* 禁止背景图像重复 */
}
.content-container {
  display: flex;
  align-items: center; /* 确保图片和按钮垂直居中 */
  /*gap: -100px; /* 图片和按钮之间的间距 */
  margin-top: 50px;
}
/* 为标题设置动画 */
.fade-in {
  opacity: 0;
  transform: translateY(-30px); /* 让标题从上方滑入 */
  animation: fadeIn 1s ease-out forwards; /* 2秒钟的淡入动画 */
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
.button-container {
  margin-left: -10px; /* 为按钮容器添加左边距，控制与图片之间的距离 */
}

h1 {
  font-size: 4rem;
  margin-top: -250px;
  margin-bottom: 10px;
  color: #2600ae;
}

p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  color: #000000;
}

.button-group {
  display: flex;
  gap: 20px;
}

button {
  padding: 12px 24px;
  font-size: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
/* 新增的图片样式 */
.image-container {
  /*margin-bottom: 30px; /* 图片和按钮之间的间距 */
  max-width: 185px;/* 限制最大宽度 */
}

.home-image {
  width: 70%; /* 设置图片宽度为100% */
  max-width: 50%00px; /* 限制最大宽度 */
  height: auto; /* 保持图片比例 */
  border-radius: 8px; /* 可选，设置图片圆角 */
}


</style>
