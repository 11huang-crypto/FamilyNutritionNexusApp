<template>
  <!--
    组件：AlertBar 警告提示条
    用途：展示警告/提示/信息消息，支持多种类型和交互
    Props:
      - type: 类型 'warning' | 'danger' | 'info' | 'success'
      - message: 消息内容
      - icon: 自定义图标名 (可选，默认按类型)
      - closable: 是否可关闭
      - action: 操作按钮文字
      - compact: 是否紧凑模式
    Events:
      - close: 关闭时触发
      - action: 点击操作按钮时触发
  -->
  <transition name="alert-slide">
    <div
      v-if="visible"
      class="alert-bar"
      :class="[`is-${type}`, { 'is-compact': compact }]"
      role="alert"
    >
      <!-- 左侧图标 -->
      <div class="alert-icon">
        <van-icon :name="computedIcon" :size="compact ? 16 : 20" />
      </div>

      <!-- 消息内容 -->
      <div class="alert-content">
        <p class="alert-message">{{ message }}</p>
      </div>

      <!-- 操作按钮 -->
      <button
        v-if="action"
        class="alert-action"
        @click="$emit('action')"
      >
        {{ action }}
      </button>

      <!-- 关闭按钮 -->
      <button
        v-if="closable"
        class="alert-close"
        @click="handleClose"
        aria-label="关闭"
      >
        <van-icon name="cross" size="14" />
      </button>
    </div>
  </transition>
</template>

<script setup>
/**
 * AlertBar - 警告提示条
 * 四种视觉层级：danger(红) > warning(橙) > info(蓝) > success(绿)
 */
import { ref, computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'info',
    validator: v => ['warning', 'danger', 'info', 'success'].includes(v)
  },
  message: { type: String, required: true },
  icon: { type: String, default: '' },
  closable: { type: Boolean, default: true },
  action: { type: String, default: '' },
  compact: { type: Boolean, default: false },
  autoClose: { type: Number, default: 0 } // 自动关闭毫秒数，0表示不自动关闭
})

const emit = defineEmits(['close', 'action'])

const visible = ref(true)

// 默认图标映射
const defaultIcons = {
  warning: 'warning-o',
  danger: 'stop-circle-o',
  info: 'info-o',
  success: 'success'
}

const computedIcon = computed(() => props.icon || defaultIcons[props.type])

// 自动关闭
if (props.autoClose > 0) {
  setTimeout(() => {
    handleClose()
  }, props.autoClose)
}

const handleClose = () => {
  visible.value = false
  emit('close')
}
</script>

<style scoped lang="scss">
.alert-bar {
  display: flex;
  align-items: flex-start;
  gap: var(--ab-space-2);
  padding: var(--ab-space-3) var(--ab-space-4);
  border-radius: var(--ab-radius-lg);
  margin: var(--ab-space-2) 0;
  transition: all var(--ab-transition-normal);

  /* ========== 类型配色 ========== */
  &.is-danger {
    background: linear-gradient(135deg, #fef2f2, #fee2e2);
    border: 1px solid #fecaca;
    .alert-icon { color: #dc2626; }
    .alert-action { color: #dc2626; background: #fecaca; }
  }

  &.is-warning {
    background: linear-gradient(135deg, #fffbeb, #fef3c7);
    border: 1px solid #fde68a;
    .alert-icon { color: #d97706; }
    .alert-action { color: #d97706; background: #fde68a; }
  }

  &.is-info {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border: 1px solid #bfdbfe;
    .alert-icon { color: #2563eb; }
    .alert-action { color: #2563eb; background: #bfdbfe; }
  }

  &.is-success {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 1px solid #bbf7d0;
    .alert-icon { color: #16a34a; }
    .alert-action { color: #16a34a; background: #bbf7d0; }
  }

  /* ========== 紧凑模式 ========== */
  &.is-compact {
    padding: var(--ab-space-2) var(--ab-space-3);
    border-radius: var(--ab-radius-md);
    gap: var(--ab-space-1);

    .alert-message {
      font-size: var(--ab-text-sm);
    }
  }
}

.alert-icon {
  flex-shrink: 0;
  margin-top: 1px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.alert-content {
  flex: 1;
  min-width: 0;
}

.alert-message {
  font-size: var(--ab-text-sm);
  line-height: var(--ab-leading-normal);
  color: var(--ab-text-primary);
  word-break: break-word;
}

.alert-action {
  flex-shrink: 0;
  padding: var(--ab-space-1) var(--ab-space-3);
  border: none;
  border-radius: var(--ab-radius-md);
  font-size: var(--ab-text-sm);
  font-weight: var(--ab-font-medium);
  cursor: pointer;
  white-space: nowrap;
  transition: all var(--ab-transition-fast);

  &:active {
    opacity: 0.8;
    transform: scale(0.95);
  }
}

.alert-close {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: var(--ab-text-tertiary);
  border-radius: var(--ab-radius-md);
  cursor: pointer;
  transition: all var(--ab-transition-fast);
  margin-top: 1px;

  &:hover,
  &:active {
    background: rgba(0, 0, 0, 0.05);
    color: var(--ab-text-primary);
  }
}

/* ========== 过渡动画 ========== */
.alert-slide-enter-active,
.alert-slide-leave-active {
  transition: all 0.3s var(--ab-ease-smooth);
}

.alert-slide-enter-from,
.alert-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
  max-height: 0;
  margin: 0;
  padding-top: 0;
  padding-bottom: 0;
}
</style>
