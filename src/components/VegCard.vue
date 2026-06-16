<template>
  <!--
    组件：VegCard 果蔬卡片
    用途：展示果蔬信息，支持多种变体（列表/网格/详情）
    Props:
      - item: 果蔬数据对象 { name, category, quantity, unit, freshness, image, nutrients, addedBy?, addedAt? }
      - variant: 变体 'list' | 'grid' | 'detail'
      - showFreshness: 是否显示新鲜度
      - showNutrients: 是否显示营养标签
      - deletable: 是否可删除
    Events:
      - click: 点击卡片
      - delete: 点击删除
  -->
  <div
    class="veg-card"
    :class="[`is-${variant}`]"
    @click="$emit('click', item)"
  >
    <!-- 图片区域 -->
    <div class="card-image-wrap">
      <img
        :src="item.image"
        :alt="item.name"
        class="card-image"
        loading="lazy"
      />
      <!-- 新鲜度徽章 -->
      <div
        v-if="showFreshness && item.freshness"
        class="freshness-badge"
        :class="freshnessClass"
      >
        <van-icon name="flower-o" size="10" />
        <span>{{ item.freshness }}%</span>
      </div>
      <!-- 类别标签 -->
      <div class="category-tag">{{ item.category }}</div>
    </div>

    <!-- 内容区域 -->
    <div class="card-content">
      <div class="card-header">
        <h3 class="card-title">{{ item.name }}</h3>
        <span class="card-quantity">{{ item.quantity }}{{ item.unit }}</span>
      </div>

      <!-- 营养标签 -->
      <div v-if="showNutrients && item.nutrients" class="card-nutrients">
        <NutriBadge
          v-for="(value, key) in displayedNutrients"
          :key="key"
          :type="getNutrientType(key)"
          :label="getNutrientLabel(key)"
          :value="value"
          size="sm"
        />
      </div>

      <!-- 添加信息 -->
      <div v-if="item.addedBy && item.addedAt" class="card-meta">
        <FamilyAvatar
          v-if="member"
          :member="member"
          size="xs"
          :showName="false"
        />
        <span class="meta-text">{{ formatDate(item.addedAt) }} 添加</span>
      </div>
    </div>

    <!-- 删除按钮 -->
    <button
      v-if="deletable"
      class="delete-btn"
      @click.stop="$emit('delete', item)"
      aria-label="删除"
    >
      <van-icon name="cross" size="14" />
    </button>
  </div>
</template>

<script setup>
/**
 * VegCard - 果蔬信息卡片
 * 三种变体：列表模式、网格模式、详情模式
 */
import { computed } from 'vue'
import NutriBadge from './NutriBadge.vue'
import FamilyAvatar from './FamilyAvatar.vue'
import { useAppStore } from '@/stores'

const props = defineProps({
  item: {
    type: Object,
    required: true,
    default: () => ({
      name: '未知食材',
      category: '其他',
      quantity: 1,
      unit: '个',
      freshness: 100,
      image: '',
      nutrients: {}
    })
  },
  variant: { type: String, default: 'list', validator: v => ['list', 'grid', 'detail'].includes(v) },
  showFreshness: { type: Boolean, default: true },
  showNutrients: { type: Boolean, default: true },
  deletable: { type: Boolean, default: false }
})

const emit = defineEmits(['click', 'delete'])

const store = useAppStore()

// 新鲜度样式
const freshnessClass = computed(() => {
  const f = props.item.freshness
  if (f >= 90) return 'is-fresh'
  if (f >= 70) return 'is-normal'
  return 'is-warning'
})

// 查找添加者
const member = computed(() => {
  if (!props.item.addedBy) return null
  return store.family.members.find(m => m.id === props.item.addedBy)
})

// 只显示前2个营养素
const displayedNutrients = computed(() => {
  const keys = Object.keys(props.item.nutrients || {}).slice(0, 2)
  const result = {}
  keys.forEach(k => { result[k] = props.item.nutrients[k] })
  return result
})

const getNutrientType = (key) => {
  const map = {
    vitaminC: 'vitamin', vitaminA: 'vitamin', vitaminK: 'vitamin',
    fiber: 'fiber', protein: 'protein', iron: 'mineral',
    calcium: 'mineral'
  }
  return map[key] || 'other'
}

const getNutrientLabel = (key) => {
  const map = {
    vitaminC: '维C', vitaminA: '维A', vitaminK: '维K',
    fiber: '纤维', protein: '蛋白', iron: '铁',
    calcium: '钙'
  }
  return map[key] || key
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const now = new Date()
  const diff = Math.floor((now - d) / (1000 * 60 * 60 * 24))
  if (diff === 0) return '今天'
  if (diff === 1) return '昨天'
  if (diff < 7) return `${diff}天前`
  return `${d.getMonth() + 1}/${d.getDate()}`
}
</script>

<style scoped lang="scss">
.veg-card {
  position: relative;
  background: var(--ab-bg-card);
  border-radius: var(--ab-radius-lg);
  box-shadow: var(--ab-shadow-sm);
  overflow: hidden;
  transition: all var(--ab-transition-normal);
  cursor: pointer;

  &:active {
    transform: scale(0.98);
    box-shadow: var(--ab-shadow-md);
  }
}

/* ========== 列表变体 ========== */
.is-list {
  display: flex;
  align-items: stretch;
  gap: var(--ab-space-3);
  padding: var(--ab-space-3);

  .card-image-wrap {
    width: 80px;
    height: 80px;
    flex-shrink: 0;
  }

  .card-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: var(--ab-radius-md);
  }

  .card-content {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: var(--ab-space-1) 0;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .card-title {
    font-size: var(--ab-text-base);
    font-weight: var(--ab-font-bold);
    color: var(--ab-text-primary);
  }

  .card-quantity {
    font-size: var(--ab-text-sm);
    color: var(--ab-text-tertiary);
    font-weight: var(--ab-font-medium);
  }

  .card-nutrients {
    display: flex;
    gap: var(--ab-space-2);
    margin-top: var(--ab-space-1);
  }

  .card-meta {
    display: flex;
    align-items: center;
    gap: var(--ab-space-1);
    margin-top: var(--ab-space-1);
  }

  .meta-text {
    font-size: var(--ab-text-xs);
    color: var(--ab-text-tertiary);
  }
}

/* ========== 网格变体 ========== */
.is-grid {
  display: flex;
  flex-direction: column;

  .card-image-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 1;
  }

  .card-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: var(--ab-radius-lg) var(--ab-radius-lg) 0 0;
  }

  .card-content {
    padding: var(--ab-space-3);
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .card-title {
    font-size: var(--ab-text-base);
    font-weight: var(--ab-font-bold);
    color: var(--ab-text-primary);
  }

  .card-quantity {
    font-size: var(--ab-text-sm);
    color: var(--ab-text-tertiary);
  }

  .card-nutrients {
    display: flex;
    gap: var(--ab-space-1);
    margin-top: var(--ab-space-2);
    flex-wrap: wrap;
  }

  .card-meta {
    display: flex;
    align-items: center;
    gap: var(--ab-space-1);
    margin-top: var(--ab-space-2);
    padding-top: var(--ab-space-2);
    border-top: 1px solid var(--ab-border-light);
  }

  .meta-text {
    font-size: var(--ab-text-xs);
    color: var(--ab-text-tertiary);
  }
}

/* ========== 详情变体 ========== */
.is-detail {
  display: flex;
  flex-direction: column;

  .card-image-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 10;
  }

  .card-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: var(--ab-radius-lg) var(--ab-radius-lg) 0 0;
  }

  .card-content {
    padding: var(--ab-space-4);
  }

  .card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: var(--ab-space-3);
  }

  .card-title {
    font-size: var(--ab-text-xl);
    font-weight: var(--ab-font-bold);
    color: var(--ab-text-primary);
  }

  .card-quantity {
    font-size: var(--ab-text-lg);
    color: var(--ab-primary-600);
    font-weight: var(--ab-font-bold);
  }

  .card-nutrients {
    display: flex;
    gap: var(--ab-space-2);
    flex-wrap: wrap;
    margin-top: var(--ab-space-2);
  }

  .card-meta {
    display: flex;
    align-items: center;
    gap: var(--ab-space-2);
    margin-top: var(--ab-space-3);
    padding-top: var(--ab-space-3);
    border-top: 1px solid var(--ab-border-light);
  }
}

/* ========== 公共元素 ========== */
.card-image-wrap {
  position: relative;
  overflow: hidden;
}

.category-tag {
  position: absolute;
  bottom: 8px;
  left: 8px;
  padding: 2px 8px;
  background: rgba(0, 0, 0, 0.5);
  color: var(--ab-text-inverse);
  font-size: var(--ab-text-xs);
  border-radius: var(--ab-radius-sm);
  backdrop-filter: blur(4px);
}

.freshness-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 2px 8px;
  border-radius: var(--ab-radius-full);
  font-size: var(--ab-text-xs);
  font-weight: var(--ab-font-bold);
  color: var(--ab-text-inverse);
  backdrop-filter: blur(4px);

  &.is-fresh {
    background: rgba(34, 197, 94, 0.85);
  }

  &.is-normal {
    background: rgba(245, 158, 11, 0.85);
  }

  &.is-warning {
    background: rgba(239, 68, 68, 0.85);
  }
}

.delete-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.4);
  border: none;
  border-radius: var(--ab-radius-full);
  color: var(--ab-text-inverse);
  cursor: pointer;
  transition: all var(--ab-transition-fast);
  z-index: 2;

  &:active {
    background: var(--ab-danger);
    transform: scale(0.9);
  }
}
</style>
