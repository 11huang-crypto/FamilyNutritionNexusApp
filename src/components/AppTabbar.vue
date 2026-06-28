<template>
  <!--
    组件：AppTabbar 底部Tab栏
    用途：APP底部导航，支持徽标、动画切换
    Props:
      - active: 当前激活项的索引
      - items: Tab项配置数组 [{ path, name, icon, badge?, dot? }]
      - safeArea: 是否适配安全区域
    Events:
      - change: 切换时触发，返回索引
  -->
  <div class="app-tabbar" :class="{ 'safe-area': safeArea }">
    <div class="tabbar-bg">
      <!-- 高亮背景滑块 -->
      <div
        class="active-bg"
        :style="{ transform: `translateX(${activeIndex * 100}%)` }"
      ></div>
    </div>

    <div class="tabbar-items">
      <div
        v-for="(item, index) in items"
        :key="item.name"
        class="tab-item"
        :class="{ 'is-active': activeIndex === index }"
        @click="handleClick(index, item)"
      >
        <div class="tab-icon-wrap">
          <van-icon
            :name="activeIndex === index ? item.iconActive || item.icon : item.icon"
            :size="22"
            class="tab-icon"
          />
          <span v-if="item.badge" class="tab-badge">{{ item.badge > 99 ? '99+' : item.badge }}</span>
          <span v-else-if="item.dot" class="tab-dot"></span>
        </div>
        <span class="tab-label">{{ item.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * AppTabbar - 底部Tab导航栏
 * 自定义动画切换效果，比原生 Vant Tabbar 更精致
 */
import { computed } from 'vue'

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

const handleClick = (index, item) => {
  activeIndex.value = index
  emit('change', index, item)
}
</script>

<style scoped lang="scss">
.app-tabbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: var(--ab-bg-elevated);
  box-shadow: 0 -1px 10px rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);

  &.safe-area {
    padding-bottom: env(safe-area-inset-bottom);
  }
}

.tabbar-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;

  .active-bg {
    position: absolute;
    top: 4px;
    left: 0;
    width: calc(100% / v-bind('items.length'));
    height: calc(100% - 8px);
    background: var(--ab-primary-50);
    border-radius: var(--ab-radius-lg);
    transition: transform var(--ab-transition-normal) var(--ab-ease-spring);
  }
}

.tabbar-items {
  position: relative;
  display: flex;
  height: 56px;
}

.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  cursor: pointer;
  transition: color var(--ab-transition-fast);
  color: var(--ab-text-tertiary);

  &.is-active {
    color: var(--ab-primary-600);

    .tab-icon {
      animation: iconPop 0.4s var(--ab-ease-spring);
    }

    .tab-label {
      font-weight: var(--ab-font-bold);
    }
  }
}

@keyframes iconPop {
  0% { transform: scale(1); }
  40% { transform: scale(1.25); }
  100% { transform: scale(1); }
}

.tab-icon-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 22px;
}

.tab-icon {
  transition: transform var(--ab-transition-fast);
}

.tab-label {
  font-size: 10px;
  line-height: 1;
  font-weight: var(--ab-font-medium);
  transition: all var(--ab-transition-fast);
}

.tab-badge {
  position: absolute;
  top: -4px;
  right: -6px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  background: var(--ab-danger);
  color: var(--ab-text-inverse);
  font-size: 10px;
  font-weight: var(--ab-font-bold);
  border-radius: var(--ab-radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--ab-bg-elevated);
}

.tab-dot {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 8px;
  height: 8px;
  background: var(--ab-danger);
  border-radius: var(--ab-radius-full);
  border: 2px solid var(--ab-bg-elevated);
}
</style>
