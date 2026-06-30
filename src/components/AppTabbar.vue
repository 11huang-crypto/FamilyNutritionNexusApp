<template>
  <div class="app-tabbar" :class="{ 'safe-area': safeArea }">
    <div class="tabbar-items">
      <div
        v-for="(item, index) in items"
        :key="item.name"
        class="tab-item"
        :class="{ 'is-active': activeIndex === index }"
        @click="handleClick(index, item)"
      >
        <div class="tab-icon-wrap">
          <ClayIcon :color="getIconColor(index, activeIndex === index)" size="sm">
            <LocalIcon :name="activeIndex === index ? item.iconActive || item.icon : item.icon" size="20" />
          </ClayIcon>
          <span v-if="item.badge" class="tab-badge">{{ item.badge > 99 ? '99+' : item.badge }}</span>
          <span v-else-if="item.dot" class="tab-dot"></span>
        </div>
        <span class="tab-label">{{ item.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import ClayIcon from './ClayIcon.vue'

const props = defineProps({
  active: { type: Number, default: 0 },
  items: {
    type: Array,
    default: () => [
      { name: 'home', label: '首页', icon: 'home-o', iconActive: 'home', path: '/' },
      { name: 'analyze', label: 'AI识图', icon: 'camera-o', iconActive: 'camera', path: '/analyze' },
      { name: 'profile', label: '我的', icon: 'user-o', iconActive: 'user', path: '/profile' },
    ]
  },
  safeArea: { type: Boolean, default: true }
})

const emit = defineEmits(['update:active', 'change'])

const activeIndex = computed({
  get: () => props.active,
  set: (val) => emit('update:active', val)
})

const getIconColor = (index, isActive) => {
  // 激活态用强彩色 Clay 底，未激活用浅色软底
  if (isActive) {
    const activeColors = ['brand', 'orange', 'lilac']
    return activeColors[index % activeColors.length]
  }
  return 'soft-gray'
}

const handleClick = (index, item) => {
  activeIndex.value = index
  emit('change', index, item)
}
</script>

<style scoped lang="scss">
.app-tabbar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  width: 100%;
  max-width: 480px;
  background: rgba(255, 255, 255, 0.4);
  box-shadow: 0 -8px 24px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-top: 1px solid var(--ab-border-subtle);

  &.safe-area {
    padding-bottom: env(safe-area-inset-bottom);
  }
}

.tabbar-items {
  position: relative;
  display: flex;
  height: 68px;
  padding: 8px 12px;
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  cursor: pointer;
  color: var(--ab-text-tertiary);
  transition: all var(--ab-transition-normal);
  position: relative;

  &.is-active {
    color: var(--ab-text-primary);
    .tab-label {
      font-weight: 700;
      color: var(--ab-text-primary);
    }
    .tab-icon-wrap :deep(.clay-icon) {
      animation: clayIconPop 0.5s var(--ab-ease-spring);
    }
  }

  &:active {
    .tab-icon-wrap :deep(.clay-icon) {
      transform: scale(0.92);
    }
  }
}

.tab-icon-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tab-label {
  font-size: 10px;
  line-height: 1;
  font-weight: 500;
  transition: all var(--ab-transition-fast);
  letter-spacing: -0.01em;
}

.tab-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  background: var(--ab-peach-500);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #fff;
  box-shadow: 0 2px 6px rgba(255, 107, 53, 0.4);
}

.tab-dot {
  position: absolute;
  top: 0;
  right: 0;
  width: 8px;
  height: 8px;
  background: var(--ab-peach-500);
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.3);
}
</style>
