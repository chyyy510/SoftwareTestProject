// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";

// 引入你要展示的组件
import HomePage from "../views/HomePage.vue";
import UploadPage from "../views/UploadPage.vue";
import ResultPage from "../views/ResultPage.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage,
  },
  {
    path: "/upload",
    name: "Upload",
    component: UploadPage,
  },
  {
    path: "/result",
    name: "Result",
    component: ResultPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
