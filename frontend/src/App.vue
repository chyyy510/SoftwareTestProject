<script setup>
import Navbar from "./components/Navbar.vue";
</script>

<template>
  <Navbar />
  <router-view />
</template>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
}
</style>
