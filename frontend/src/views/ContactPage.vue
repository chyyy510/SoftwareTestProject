<template>
  <div class="home-container">
    <!--将fade in 应用到title-->
    <h1 class="title-fade-in">我们是软件测试导论4组</h1>
    <!--text-->
    <p class="text-fade-in">
      组员：<br />
      陈红韵，徐赫昭，胡林敏
    </p>
    <!-- 使用 Flexbox 来并排显示图片和按钮 -->
    <div class="image-container">
      <img
        src="../assets/images/cats/blue_champ.png"
        alt="示例图片"
        class="home-image"
      />
    </div>
  </div>
</template>

<script></script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 100px;
  text-align: center;
  min-height: 100vh;
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

/*欢迎来到样例测试生成系统-*/
h1 {
  font-size: 4rem;
  margin-top: -180px;
  margin-bottom: 10px;
  color: #2600ae;
  font-family: "Roboto", sans-serif; /* 设置字体为 Roboto */
}

p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  color: #6e3d3d;
  line-height: 50px;
}

.button-group {
  display: flex;
  gap: 20px;
}

button {
  padding: 12px 24px;
  font-size: 1rem;
  background-color: #0056b3;
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
