<template>
  <div class="home-container">
    <h1>欢迎来到测试样例生成系统</h1>
    <p>请选择您要使用的功能：</p>
    <div class="button-group">
      <router-link to="/upload">
        <button>上传 Python 文件</button>
      </router-link>
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
  background: linear-gradient(to bottom, #f0f4f8, #d9e2ec);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #333;
}

p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  color: #555;
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
</style>
