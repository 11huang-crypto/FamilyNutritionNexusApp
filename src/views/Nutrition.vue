<template>
  <div class="nutrition-page">
    <AppNavbar title="营养分析" :showBack="true" />

    <div class="page-body">
      <!-- 食物头部 — Clay 软糯卡 -->
      <div class="food-header clay-card clay-card--feature clay-card--soft-mint" v-if="foodData">
        <div class="food-avatar">
          <span class="food-emoji">{{ foodData.emoji || '🥦' }}</span>
        </div>
        <div class="food-header-info">
          <h1 class="food-name">{{ foodData.name }}</h1>
          <span class="food-category">{{ foodData.category }}</span>
        </div>
        <div class="food-score">
          <div class="score-ring">
            <span class="score-num">{{ healthScore }}</span>
            <span class="score-tag">健康分</span>
          </div>
        </div>
      </div>

      <!-- 营养总览 — 4 张彩色 Clay 卡 -->
      <div class="nutrition-summary" v-if="foodData">
        <div class="summary-item summary-item--orange">
          <span class="summary-emoji">🔥</span>
          <span class="summary-value">{{ totalCalories }}</span>
          <span class="summary-label">总热量<br/>kcal</span>
        </div>
        <div class="summary-item summary-item--peach">
          <span class="summary-emoji">🥩</span>
          <span class="summary-value">{{ totalProtein }}</span>
          <span class="summary-label">蛋白质<br/>g</span>
        </div>
        <div class="summary-item summary-item--blue">
          <span class="summary-emoji">🍚</span>
          <span class="summary-value">{{ totalCarbs }}</span>
          <span class="summary-label">碳水<br/>g</span>
        </div>
        <div class="summary-item summary-item--lilac">
          <span class="summary-emoji">🥑</span>
          <span class="summary-value">{{ totalFat }}</span>
          <span class="summary-label">脂肪<br/>g</span>
        </div>
      </div>

      <!-- 营养成分详情 -->
      <div class="clay-card section-card" v-if="foodData">
        <div class="section-header-row">
          <span class="section-eyebrow">NUTRITION FACTS</span>
          <h3 class="section-title">营养成分详情</h3>
        </div>
        <div class="detail-grid">
          <div class="detail-row" v-for="item in nutritionDetails" :key="item.label">
            <span class="detail-emoji">{{ item.emoji }}</span>
            <span class="detail-label">{{ item.label }}</span>
            <div class="detail-bar-wrap">
              <div class="detail-bar" :class="`detail-bar--${item.colorKey}`" :style="{ width: item.percent + '%' }"></div>
            </div>
            <span class="detail-value">{{ item.value }}</span>
          </div>
        </div>
      </div>

      <!-- 健康提示 -->
      <div class="clay-card section-card clay-card--soft-brand" v-if="foodData">
        <div class="section-header-row">
          <span class="section-eyebrow">HEALTH TIPS</span>
          <h3 class="section-title">健康提示</h3>
        </div>
        <div class="tips-list">
          <div class="tip-item" v-for="(tip, index) in healthTips" :key="index">
            <ClayIcon :color="tip.color" size="sm">
              <span class="tip-icon">{{ tip.icon }}</span>
            </ClayIcon>
            <span class="tip-text">{{ tip.text }}</span>
          </div>
        </div>
      </div>

      <!-- 食用建议 -->
      <div class="clay-card section-card clay-card--soft-orange" v-if="foodData">
        <div class="section-header-row">
          <span class="section-eyebrow">DIETARY ADVICE</span>
          <h3 class="section-title">食用建议</h3>
        </div>
        <p class="suggestion-text">{{ foodData?.suggestion || '暂无特别建议' }}</p>
      </div>

      <!-- 空状态 -->
      <div class="empty-state" v-if="!foodData && !loading">
        <div class="empty-emoji-wrap">
          <span class="empty-emoji">🔍</span>
        </div>
        <p class="empty-text">暂无数据，请先进行食材识别</p>
        <button class="clay-btn clay-btn--primary" @click="$router.push('/recognize')">去识别</button>
      </div>

      <van-loading v-if="loading" class="loading-center" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppNavbar from '@/components/AppNavbar.vue'
import ClayIcon from '@/components/ClayIcon.vue'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const foodData = ref(null)

const healthTips = [
  { icon: '✓', color: 'mint', text: '低热量高营养，适合减肥人群' },
  { icon: '✓', color: 'mint', text: '富含抗氧化物质' },
  { icon: 'i', color: 'blue', text: '烹饪时间不宜过长' }
]

const totalCalories = computed(() => foodData.value?.calories || 0)
const totalProtein = computed(() => foodData.value?.protein || 0)
const totalCarbs = computed(() => foodData.value?.carbs || 0)
const totalFat = computed(() => foodData.value?.fat || 0)
const healthScore = computed(() => {
  if (!foodData.value) return 0
  let score = 80
  if ((foodData.value.calories || 0) < 50) score += 8
  if ((foodData.value.protein || 0) > 2) score += 6
  if ((foodData.value.fiber || 0) > 2) score += 6
  return Math.min(99, score)
})

const nutritionDetails = computed(() => {
  if (!foodData.value) return []
  const maxVal = Math.max(foodData.value.calories || 0, foodData.value.protein || 0, foodData.value.carbs || 0, foodData.value.fat || 0, foodData.value.fiber || 0, 1)
  return [
    { label: '热量', emoji: '🔥', value: (foodData.value.calories || 0) + ' kcal', percent: ((foodData.value.calories || 0) / maxVal) * 100, colorKey: 'orange' },
    { label: '蛋白质', emoji: '🥩', value: (foodData.value.protein || 0) + ' g', percent: ((foodData.value.protein || 0) / maxVal) * 100, colorKey: 'peach' },
    { label: '碳水', emoji: '🍚', value: (foodData.value.carbs || 0) + ' g', percent: ((foodData.value.carbs || 0) / maxVal) * 100, colorKey: 'blue' },
    { label: '脂肪', emoji: '🥑', value: (foodData.value.fat || 0) + ' g', percent: ((foodData.value.fat || 0) / maxVal) * 100, colorKey: 'lilac' },
    { label: '纤维', emoji: '🥦', value: (foodData.value.fiber || 0) + ' g', percent: ((foodData.value.fiber || 0) / maxVal) * 100, colorKey: 'mint' },
  ]
})

onMounted(() => {
  const dataParam = route.query.data
  if (dataParam) {
    try {
      const parsed = JSON.parse(decodeURIComponent(dataParam))
      foodData.value = { ...parsed, ...(parsed.nutrition || {}) }
    } catch (e) { setDefaultData() }
  } else { setDefaultData() }
})

const setDefaultData = () => {
  foodData.value = {
    name: '西兰花', category: '蔬菜类',
    calories: 34, protein: 2.8, carbs: 7.6, fat: 0.4, fiber: 2.6,
    vitaminC: 51, calcium: 47, emoji: '🥦',
    suggestion: '西兰花富含维生素C和膳食纤维，建议清炒或焯水后凉拌，保留营养成分。'
  }
}
</script>

<style scoped lang="scss">
.nutrition-page { min-height: 100vh; background: transparent; }
.page-body { padding: var(--ab-space-4); padding-bottom: 80px; display: flex; flex-direction: column; gap: var(--ab-space-4); }

/* 食物头部 — 3 列布局 */
.food-header {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--ab-space-4);
}
.food-avatar {
  width: 64px;
  height: 64px;
  border-radius: 20px;
  background: linear-gradient(135deg, #a7f3c6 0%, #34d77a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--ab-shadow-float-sm);
  flex-shrink: 0;
}
.food-emoji {
  font-size: 36px;
  line-height: 1;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.10));
}
.food-header-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}
.food-name {
  font-size: 26px;
  font-weight: 700;
  color: var(--ab-text-primary);
  letter-spacing: -0.03em;
  line-height: 1.1;
}
.food-category {
  font-size: 12px;
  color: var(--ab-text-tertiary);
  font-weight: 500;
}
.food-score {
  flex-shrink: 0;
}
.score-ring {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #fff 0%, var(--ab-mint-50) 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: var(--ab-shadow-float-sm);
  border: 2px solid var(--ab-mint-200);
}
.score-num {
  font-size: 22px;
  font-weight: 700;
  color: var(--ab-mint-600);
  line-height: 1;
  letter-spacing: -0.02em;
}
.score-tag {
  font-size: 9px;
  color: var(--ab-text-tertiary);
  font-weight: 600;
  margin-top: 2px;
}

/* 营养总览 — 4 彩色 Clay 卡 */
.nutrition-summary {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 14px 6px;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: var(--ab-shadow-float-sm);
  border: 1px solid var(--ab-border-subtle);
  text-align: center;
  position: relative;
  overflow: hidden;

  &--orange { background: linear-gradient(135deg, var(--ab-orange-50) 0%, #fff 100%); }
  &--peach  { background: linear-gradient(135deg, var(--ab-peach-50) 0%, #fff 100%); }
  &--blue   { background: linear-gradient(135deg, var(--ab-blue-50) 0%, #fff 100%); }
  &--lilac  { background: linear-gradient(135deg, var(--ab-lilac-50) 0%, #fff 100%); }
}
.summary-emoji {
  font-size: 22px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.10));
  line-height: 1;
}
.summary-value {
  font-size: 22px;
  font-weight: 700;
  color: var(--ab-text-primary);
  letter-spacing: -0.02em;
  line-height: 1;
}
.summary-label {
  font-size: 10px;
  color: var(--ab-text-tertiary);
  font-weight: 500;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

/* 通用 section 卡 */
.section-card {
  padding: var(--ab-space-5);
}
.section-header-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: var(--ab-space-4);
}
.section-eyebrow {
  font-size: 10px;
  font-weight: 700;
  color: var(--ab-brand-600);
  letter-spacing: 0.12em;
}
.section-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--ab-text-primary);
  letter-spacing: -0.02em;
  line-height: 1.1;
}

/* 营养成分条 */
.detail-grid { display: flex; flex-direction: column; gap: 12px; }
.detail-row { display: flex; align-items: center; gap: 8px; }
.detail-emoji {
  font-size: 18px;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.08));
}
.detail-label {
  width: 50px;
  font-size: 13px;
  color: var(--ab-text-secondary);
  font-weight: 500;
  flex-shrink: 0;
}
.detail-bar-wrap {
  flex: 1;
  height: 10px;
  background: var(--ab-gray-100);
  border-radius: 9999px;
  overflow: hidden;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.06);
}
.detail-bar {
  height: 100%;
  border-radius: 9999px;
  transition: width 0.6s var(--ab-ease-smooth);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.4);
  &--orange { background: linear-gradient(90deg, var(--ab-orange-300), var(--ab-orange-500)); }
  &--peach  { background: linear-gradient(90deg, var(--ab-peach-300), var(--ab-peach-500)); }
  &--blue   { background: linear-gradient(90deg, var(--ab-blue-300), var(--ab-blue-500)); }
  &--lilac  { background: linear-gradient(90deg, var(--ab-lilac-300), var(--ab-lilac-500)); }
  &--mint   { background: linear-gradient(90deg, var(--ab-mint-300), var(--ab-mint-500)); }
}
.detail-value {
  width: 64px;
  text-align: right;
  font-size: 13px;
  font-weight: 700;
  color: var(--ab-text-primary);
  flex-shrink: 0;
}

/* 健康提示 */
.tips-list { display: flex; flex-direction: column; gap: 10px; }
.tip-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: #ffffff;
  border-radius: 14px;
  box-shadow: var(--ab-shadow-float-sm);
}
.tip-icon {
  font-size: 14px;
  font-weight: 700;
  color: #fff;
  line-height: 1;
}
.tip-text {
  font-size: 13px;
  color: var(--ab-text-secondary);
  font-weight: 500;
}

/* 食用建议 */
.suggestion-text {
  font-size: 14px;
  color: var(--ab-text-secondary);
  line-height: 1.6;
  margin: 0;
  font-weight: 500;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--ab-space-4);
  padding: 60px 20px;
}
.empty-emoji-wrap {
  width: 100px;
  height: 100px;
  border-radius: 32px;
  background: linear-gradient(135deg, var(--ab-brand-100), var(--ab-brand-300));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--ab-shadow-float);
}
.empty-emoji {
  font-size: 48px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.12));
}
.empty-text { font-size: 14px; color: var(--ab-text-tertiary); }

.loading-center { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); }
</style>
