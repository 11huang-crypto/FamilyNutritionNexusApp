<template>
  <!--
    组件：NutriBadge 营养标签徽章
    用途：展示食材的营养成分，多种类型和尺寸
    Props:
      - type: 营养类型 'vitamin' | 'fiber' | 'protein' | 'mineral' | 'other'
      - label: 标签文字
      - value: 数值
      - unit: 单位 (默认 mg/g)
      - size: 尺寸 'sm' | 'md' | 'lg'
      - showValue: 是否显示数值
      - percent: 百分比进度 (0-100)，有值时显示进度条
    Events:
      - click: 点击时触发
  -->
  <div
    class="nutri-badge"
    :class="[`is-${type}`, `size-${size}`, { 'has-percent': percent !== null }]"
    @click="$emit('click')"
  >
    <!-- 图标 -->
    <span class="badge-icon">
      <van-icon :name="iconName" :size="iconSize" />
    </span>

    <!-- 标签文字 -->
    <span class="badge-label">{{ label }}</span>

    <!-- 数值 -->
    <span v-if="showValue && value !== undefined" class="badge-value">
      {{ value }}<span class="badge-unit">{{ unit }}</span>
    </span>

    <!-- 百分比进度条 -->
    <div v-if="percent !== null" class="badge-progress">
      <div class="progress-track">
        <div
          class="progress-fill"
          :style="{ width: clampedPercent + '%' }"
        ></div>
      </div>
      <span class="progress-text">{{ clampedPercent }}%</span>
    </div>
  </div>
</template>

<script setup>
/**
 * NutriBadge - 营养标签徽章
 * 颜色编码系统：维生素=青绿，纤维=橙黄，蛋白质=蓝紫，矿物质=靛蓝
 */
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'other',
    validator: v => ['vitamin', 'fiber', 'protein', 'mineral', 'other'].includes(v)
  },
  label: { type: String, required: true },
  value: { type: [Number, String], default: undefined },
  unit: { type: String, default: 'mg' },
  size: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md', 'lg'].includes(v)
  },
  showValue: { type: Boolean, default: true },
  percent: { type: Number, default: null }
})

const emit = defineEmits(['click'])

// 图标映射
const iconMap = {
  vitamin: 'gem-o',
  fiber: 'flower-o',
  protein: 'fire-o',
  mineral: 'diamond-o',
  other: 'label-o'
}

const iconName = computed(() => iconMap[props.type] || 'label-o')

// 图标尺寸
const iconSizeMap = { sm: 12, md: 14, lg: 16 }
const iconSize = computed(() => iconSizeMap[props.size] || 14)

// 百分比限制
const clampedPercent = computed(() => {
  if (props.percent === null) return 0
  return Math.min(100, Math.max(0, props.percent))
})
</script>

<style scoped lang="scss">
.nutri-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border-radius: var(--ab-radius-sm);
  font-weight: var(--ab-font-medium);
  white-space: nowrap;
  cursor: default;
  transition: all var(--ab-transition-fast);

  &:active {
    transform: scale(0.95);
  }

  /* ========== 类型配色 ========== */
  &.is-vitamin {
    background: #e8f5e9;
    color: #2e7d32;
    .badge-icon { color: #4caf50; }
    .progress-fill { background: linear-gradient(90deg, #81c784, #4caf50); }
  }

  &.is-fiber {
    background: #fff3e0;
    color: #e65100;
    .badge-icon { color: #ff9800; }
    .progress-fill { background: linear-gradient(90deg, #ffb74d, #ff9800); }
  }

  &.is-protein {
    background: #f3e5f5;
    color: #7b1fa2;
    .badge-icon { color: #9c27b0; }
    .progress-fill { background: linear-gradient(90deg, #ce93d8, #9c27b0); }
  }

  &.is-mineral {
    background: #e3f2fd;
    color: #1565c0;
    .badge-icon { color: #2196f3; }
    .progress-fill { background: linear-gradient(90deg, #90caf9, #2196f3); }
  }

  &.is-other {
    background: var(--ab-gray-100);
    color: var(--ab-gray-600);
    .badge-icon { color: var(--ab-gray-500); }
    .progress-fill { background: linear-gradient(90deg, var(--ab-gray-400), var(--ab-gray-500)); }
  }

  /* ========== 尺寸变体 ========== */
  &.size-sm {
    padding: 2px 8px;
    font-size: var(--ab-text-xs);
    border-radius: var(--ab-radius-sm);
  }

  &.size-md {
    padding: 4px 10px;
    font-size: var(--ab-text-sm);
    border-radius: var(--ab-radius-md);
  }

  &.size-lg {
    padding: 6px 14px;
    font-size: var(--ab-text-base);
    border-radius: var(--ab-radius-lg);
  }

  /* ========== 带进度条模式 ========== */
  &.has-percent {
    flex-direction: column;
    align-items: stretch;
    gap: 6px;
    padding: var(--ab-space-3);
    background: var(--ab-bg-card);
    border: 1px solid var(--ab-border-light);
    box-shadow: var(--ab-shadow-sm);
    border-radius: var(--ab-radius-md);

    .badge-icon {
      align-self: flex-start;
    }

    .badge-label {
      font-size: var(--ab-text-sm);
      font-weight: var(--ab-font-bold);
    }

    .badge-value {
      font-size: var(--ab-text-xl);
      font-weight: var(--ab-font-bold);
      color: var(--ab-text-primary);
    }
  }
}

.badge-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.badge-label {
  line-height: 1;
}

.badge-value {
  line-height: 1;
}

.badge-unit {
  font-size: 0.75em;
  margin-left: 1px;
  opacity: 0.7;
}

.badge-progress {
  display: flex;
  align-items: center;
  gap: var(--ab-space-2);
}

.progress-track {
  flex: 1;
  height: 6px;
  background: var(--ab-gray-200);
  border-radius: var(--ab-radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: var(--ab-radius-full);
  transition: width 0.6s var(--ab-ease-smooth);
}

.progress-text {
  font-size: var(--ab-text-xs);
  color: var(--ab-text-tertiary);
  font-weight: var(--ab-font-bold);
  min-width: 32px;
  text-align: right;
}
</style>
