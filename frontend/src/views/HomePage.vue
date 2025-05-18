<template>
  <div class="home-container">
    <!--将fade in 应用到title-->
    <h1 class="title-fade-in">欢迎来到测试样例生成系统</h1>
    <!--text-->
    <p class="text-fade-in">
      这是一个基于静态分析的 Python 代码测试样例生成系统，
      <br />旨在帮助开发人员自动生成针对 Python 代码的各种测试样例。
      <br />我们的系统能为您提供有力的支持，帮助您更轻松地进行开发和测试。
      <br />点击以下按钮立即体验，提升您的开发效率！
    </p>
    <!-- 使用 Flexbox 来并排显示图片和按钮 -->
    <div class="content-container">
      <div class="image-container">
        <img
          src="../assets/images/cats/blue_cono.png"
          alt="示例图片"
          class="home-image"
        />
      </div>
      <div class="button1-container">
        <router-link to="/upload">
          <button>人工代码分析</button>
        </router-link>
      </div>
      <div class="button2-container">
        <router-link to="/upload">
          <button>API接口分析</button>
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

  background-size: cover; /* 背景图像填充整个容器 */
  background-position: center; /* 背景图像居中 */
  background-repeat: no-repeat; /* 禁止背景图像重复 */
}
.content-container {
  display: flex;
  align-items: center; /* 确保图片和按钮垂直居中 */
  /*gap: -100px; /* 图片和按钮之间的间距 */
  margin-top: 50px;
  margin-left: -100px;
}
/* 为标题设置动画 */
.title-fade-in {
  opacity: 0;
  transform: translateY(-30px); /* 让标题从上方滑入 */
  animation: fadeIn 1s ease-out forwards; /* 1秒钟的淡入动画 */
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

/* 为 <p> 标签设置淡入动画 */
.text-fade-in {
  opacity: 0;
  transform: translateY(-20px); /* 让文字从上方滑入 */
  animation: fadeInText 1s ease-out forwards; /* 1秒钟的淡入动画 */
  animation-delay: 1s; /* 延迟1秒后开始 */
}

@keyframes fadeInText {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/*人工代码分析*/
.button1-container {
  margin-left: -10px; /* 为按钮容器添加左边距，控制与图片之间的距离 */
}
/*API接口分析 */
.button2-container {
  margin-left: 20px; /* 为按钮容器添加左边距，控制与图片之间的距离 */
}
/*欢迎来到样例测试生成系统-*/
h1 {
  font-size: 4rem;
  margin-top: -250px;
  margin-bottom: 10px;
  color: #2600ae;
  font-family: "Roboto", sans-serif; /* 设置字体为 Roboto */
}

p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  color: #6e3d3d;
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
  max-width: 185px; /* 限制最大宽度 */
}

.home-image {
  width: 70%; /* 设置图片宽度为100% */
  max-width: 50%00px; /* 限制最大宽度 */
  height: auto; /* 保持图片比例 */
  border-radius: 8px; /* 可选，设置图片圆角 */
}
</style>
