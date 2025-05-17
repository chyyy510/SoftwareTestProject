<script setup>
import Navbar from "./components/Navbar.vue";
</script>

<template>
  <Navbar />
  <router-view />
</template>

<style>
html,
body {
  background: linear-gradient(to bottom, #f0f4f8, #d9e2ec);
  min-height: 100vh;
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-repeat: no-repeat;
  background-attachment: fixed; /* 背景固定 */
  background-size: cover; /* 背景拉满页面 */
}
</style>
