<template>
  <div
    class="nutri-badge"
    :class="[`is-${type}`, `size-${size}`, { 'has-percent': percent !== null }]"
    @click="$emit('click')"
  >
    <!-- 顶部：LocalIcon + 标签 + 数值 -->
    <div class="badge-top">
      <span class="badge-icon">
        <LocalIcon :name="iconName" :size="iconSize" />
      </span>
      <span class="badge-label">{{ label }}</span>
    </div>
    <div v-if="showValue && value !== undefined" class="badge-value">
      {{ value }}<span class="badge-unit">{{ unit }}</span>
    </div>

    <!-- 进度条 -->
    <div v-if="percent !== null" class="badge-progress">
      <div class="progress-track">
        <div class="progress-fill" :style="{ width: clampedPercent + '%' }"></div>
      </div>
      <span class="progress-text">{{ clampedPercent }}%</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'other',
    validator: v => ['vitamin', 'fiber', 'protein', 'mineral', 'iron', 'calcium', 'other'].includes(v)
  },
  label: { type: String, required: true },
  value: { type: [Number, String], default: undefined },
  unit: { type: String, default: 'mg' },
  size: { type: String, default: 'md', validator: v => ['sm', 'md', 'lg'].includes(v) },
  showValue: { type: Boolean, default: true },
  percent: { type: Number, default: null }
})

const emit = defineEmits(['click'])

const emojiMap = {
  protein: '🥩',
  vitamin: '🍊',
  vitaminC: '🍊',
  fiber: '🥦',
  mineral: '🪨',
  iron: '🩸',
  calcium: '🥛',
  other: '📊'
}

// 用 41 个本地 PNG 替代 emoji（颜色、风格统一）
const iconNameMap = {
  protein: 'fire-o',        // 蛋白质 → 火焰
  vitamin: 'VC',            // 维C → 维生素C专用图标（用户指定 2026-06-30）
  vitaminC: 'VC',
  fiber: 'flower-o-veggie', // 纤维 → 蔬菜花
  mineral: 'gem-o',         // 矿物 → 宝石
  iron: 'gem-o',            // 铁 → 橙色宝石（用户指定 2026-06-30）
  calcium: 'diamond-o',     // 钙 → 钻石（用户指定）
  other: 'info-o',          // 其他 → 信息
}
const iconName = computed(() => iconNameMap[props.type] || 'info-o')
const iconSize = computed(() => props.size === 'lg' ? 20 : 18)

const clampedPercent = computed(() => {
  if (props.percent === null) return 0
  return Math.min(100, Math.max(0, props.percent))
})
</script>

<style scoped lang="scss">
.nutri-badge {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 6px;
  padding: 12px;
  background: #ffffff;
  border-radius: 18px;
  box-shadow: var(--ab-shadow-float-sm);
  border: 1px solid var(--ab-border-subtle);
  transition: all var(--ab-transition-normal);
  cursor: default;

  &:active { transform: scale(0.97); box-shadow: var(--ab-shadow-press); }

  /* 类型配色 — emoji 容器彩色 Clay 底 */
  &.is-vitamin {
    .badge-icon {
      background: linear-gradient(135deg, var(--ab-orange-200) 0%, var(--ab-orange-400) 100%);
      box-shadow: 0 4px 10px rgba(249, 115, 22, 0.25);
    }
    .badge-value { color: var(--ab-orange-600); }
    .progress-fill { background: linear-gradient(90deg, var(--ab-orange-300), var(--ab-orange-500)); }
  }
  &.is-fiber {
    .badge-icon {
      background: linear-gradient(135deg, var(--ab-mint-200) 0%, var(--ab-mint-400) 100%);
      box-shadow: 0 4px 10px rgba(27, 196, 101, 0.25);
    }
    .badge-value { color: var(--ab-mint-600); }
    .progress-fill { background: linear-gradient(90deg, var(--ab-mint-300), var(--ab-mint-500)); }
  }
  &.is-protein {
    .badge-icon {
      background: linear-gradient(135deg, var(--ab-peach-200) 0%, var(--ab-peach-400) 100%);
      box-shadow: 0 4px 10px rgba(255, 107, 53, 0.25);
    }
    .badge-value { color: var(--ab-peach-600); }
    .progress-fill { background: linear-gradient(90deg, var(--ab-peach-300), var(--ab-peach-500)); }
  }
  &.is-mineral, &.is-iron {
    .badge-icon {
      background: linear-gradient(135deg, var(--ab-blue-200) 0%, var(--ab-blue-400) 100%);
      box-shadow: 0 4px 10px rgba(59, 135, 240, 0.25);
    }
    .badge-value { color: var(--ab-blue-600); }
    .progress-fill { background: linear-gradient(90deg, var(--ab-blue-300), var(--ab-blue-500)); }
  }
  &.is-calcium {
    .badge-icon {
      background: linear-gradient(135deg, var(--ab-lilac-200) 0%, var(--ab-lilac-400) 100%);
      box-shadow: 0 4px 10px rgba(129, 95, 240, 0.25);
    }
    .badge-value { color: var(--ab-lilac-600); }
    .progress-fill { background: linear-gradient(90deg, var(--ab-lilac-300), var(--ab-lilac-500)); }
  }
  &.is-other {
    .badge-icon {
      background: linear-gradient(135deg, var(--ab-gray-100) 0%, var(--ab-gray-300) 100%);
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    }
    .badge-value { color: var(--ab-gray-700); }
    .progress-fill { background: linear-gradient(90deg, var(--ab-gray-300), var(--ab-gray-500)); }
  }

  /* 尺寸 */
  &.size-sm { padding: 8px; border-radius: 14px; }
  &.size-md { padding: 10px; border-radius: 16px; }
  &.size-lg { padding: 12px; border-radius: 18px; }
}

.badge-top {
  display: flex;
  align-items: center;
  gap: 6px;
}

.badge-icon {
  width: 28px;
  height: 28px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.emoji-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  line-height: 1;
  filter: drop-shadow(0 1px 2px rgba(0,0,0,0.15));
}

/* LocalIcon 在 .badge-icon (28×28 圆角方块) 内垂直水平居中 */
.badge-icon {
  padding: 0;
}
.badge-icon :deep(.local-icon) {
  display: block;
  filter: drop-shadow(0 1px 2px rgba(0,0,0,0.15));
}

.badge-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--ab-text-primary);
  line-height: 1;
  letter-spacing: -0.01em;
}

.badge-value {
  font-size: 18px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.02em;
}
.badge-unit {
  font-size: 0.6em;
  margin-left: 2px;
  opacity: 0.7;
  font-weight: 600;
}

.badge-progress {
  display: flex;
  align-items: center;
  gap: 6px;
}

.progress-track {
  flex: 1;
  height: 6px;
  background: var(--ab-gray-100);
  border-radius: 9999px;
  overflow: hidden;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04);
}

.progress-fill {
  height: 100%;
  border-radius: 9999px;
  transition: width 0.6s var(--ab-ease-smooth);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

.progress-text {
  font-size: 10px;
  color: var(--ab-text-tertiary);
  font-weight: 700;
  min-width: 28px;
  text-align: right;
}
</style>
