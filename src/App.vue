<template>
  <div id="app">
    <!-- 粒子背景层（最底，固定定位，不阻塞点击） -->
    <ParticleBackground />
    <!-- 内容层 -->
    <div class="app-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import ParticleBackground from './components/ParticleBackground.vue'
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

/* 全局重置：让粒子背景透出 */
html, body {
  margin: 0;
  padding: 0;
  background: transparent;  /* 透出 canvas 粒子 */
  min-height: 100vh;
  font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

#app {
  position: relative;
  min-height: 100vh;
  background: transparent;
}

.app-content {
  position: relative;
  z-index: 1;
  min-height: 100vh;
}
</style>
