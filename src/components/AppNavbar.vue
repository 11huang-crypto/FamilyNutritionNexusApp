<template>
  <!--
    组件：AppNavbar 顶部导航栏
    用途：页面顶部导航，支持返回、标题、右侧操作区
    Props:
      - title: 标题文字
      - showBack: 是否显示返回按钮
      - transparent: 是否透明背景
      - sticky: 是否吸顶
      - rightText: 右侧文字按钮
      - rightIcon: 右侧图标名称
    Events:
      - back: 点击返回时触发
      - right-click: 点击右侧按钮时触发
  -->
  <div
    class="app-navbar"
    :class="{
      'is-transparent': transparent,
      'is-sticky': sticky,
      'has-shadow': !transparent
    }"
  >
    <div class="navbar-content">
      <!-- 左侧返回按钮 -->
      <div class="navbar-left">
        <slot name="left">
          <button
            v-if="showBack"
            class="nav-btn nav-back"
            @click="handleBack"
            aria-label="返回"
          >
            <van-icon name="arrow-left" size="20" />
          </button>
        </slot>
      </div>

      <!-- 中间标题 -->
      <div class="navbar-center">
        <slot name="title">
          <h1 class="nav-title">{{ title }}</h1>
        </slot>
      </div>

      <!-- 右侧操作区 -->
      <div class="navbar-right">
        <slot name="right">
          <button
            v-if="rightText"
            class="nav-btn nav-text-btn"
            @click="$emit('right-click')"
          >
            {{ rightText }}
          </button>
          <button
            v-else-if="rightIcon"
            class="nav-btn nav-icon-btn"
            @click="$emit('right-click')"
          >
            <van-icon :name="rightIcon" size="20" />
          </button>
        </slot>
      </div>
    </div>

    <!-- 底部进度条（可选） -->
    <div v-if="loading" class="navbar-progress">
      <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
/**
 * AppNavbar - 顶部导航栏组件
 * 基于 Vant NavBar 的设计理念，但更轻量、更灵活
 */
import { useRouter } from 'vue-router'

const props = defineProps({
  title: { type: String, default: '' },
  showBack: { type: Boolean, default: true },
  transparent: { type: Boolean, default: false },
  sticky: { type: Boolean, default: true },
  rightText: { type: String, default: '' },
  rightIcon: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  progress: { type: Number, default: 0 },
  customBack: { type: Function, default: null }
})

const emit = defineEmits(['back', 'right-click'])

const router = useRouter()

const handleBack = () => {
  if (props.customBack) {
    props.customBack()
  } else {
    emit('back')
    router.back()
  }
}
</script>

<style scoped lang="scss">
.app-navbar {
  position: relative;
  z-index: 100;
  background: var(--ab-bg-elevated);
  transition: background var(--ab-transition-fast);

  &.is-sticky {
    position: sticky;
    top: 0;
  }

  &.is-transparent {
    background: transparent;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;

    .nav-title {
      color: var(--ab-text-inverse);
    }

    .nav-btn {
      color: var(--ab-text-inverse);
    }
  }

  &.has-shadow {
    box-shadow: var(--ab-shadow-sm);
  }
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 48px;
  padding: 0 var(--ab-space-3);
}

.navbar-left,
.navbar-right {
  flex: 0 0 auto;
  min-width: 48px;
  display: flex;
  align-items: center;
}

.navbar-right {
  justify-content: flex-end;
}

.navbar-center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 var(--ab-space-2);
}

.nav-title {
  font-size: var(--ab-text-lg);
  font-weight: var(--ab-font-bold);
  color: var(--ab-text-primary);
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 220px;
}

.nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: var(--ab-text-primary);
  border-radius: var(--ab-radius-md);
  cursor: pointer;
  transition: all var(--ab-transition-fast);

  &:active {
    background: var(--ab-gray-100);
    transform: scale(0.92);
  }
}

.nav-text-btn {
  width: auto;
  padding: 0 var(--ab-space-3);
  font-size: var(--ab-text-sm);
  font-weight: var(--ab-font-medium);
  color: var(--ab-primary-600);
}

.navbar-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--ab-gray-200);
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--ab-primary-400), var(--ab-primary-600));
  transition: width 0.3s var(--ab-ease-smooth);
}
</style>
