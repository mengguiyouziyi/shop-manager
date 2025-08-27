<template>
  <div class="min-h-screen bg-background text-foreground transition-colors">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { useDark, useToggle } from '@vueuse/core'

// 暗色模式支持
const isDark = useDark()
const toggleDark = useToggle(isDark)

// 导出供其他组件使用
defineExpose({
  isDark,
  toggleDark
})
</script>

<style>
/* 样式已迁移到 index.css */
</style>
