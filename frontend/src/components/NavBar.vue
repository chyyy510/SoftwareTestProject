<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="logo">软件测试导论大作业</div>
      <ul class="nav-links">
        <li>
          <router-link to="/" exact-active-class="active-link"
            >主页</router-link
          >
        </li>
        <li>
          <router-link to="/upload" exact-active-class="active-link"
            >上传代码</router-link
          >
        </li>
        <li>
          <router-link to="/result" exact-active-class="active-link"
            >人工代码生成结果</router-link
          >
        </li>
        <li>
          <router-link to="/about" exact-active-class="active-link"
            >API接口生成结果</router-link
          >
        </li>

        <li>
          <router-link to="/contact" exact-active-class="active-link"
            >联系我们</router-link
          >
        </li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background-color: #23246c;
  color: white;
  padding: 0px;
  height: 60px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  user-select: none;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 24px;
  margin: 0;
  padding: 0;
}

.nav-links li a {
  color: white;
  text-decoration: none;
  font-size: 16px;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.nav-links li a:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.active-link {
  background-color: rgba(255, 255, 255, 0.35);
  font-weight: 600;
}
</style>
