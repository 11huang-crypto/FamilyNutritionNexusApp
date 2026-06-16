<template>
  <!--
    MealPlanView.vue - 一周食谱页
  -->
  <div class="meal-plan-page">
    <AppNavbar title="一周食谱" rightIcon="add-o" />

    <div class="page-body">
      <div class="plan-intro card-base" style="background: linear-gradient(135deg, #fff7ed, #ffedd5);">
        <h3 class="intro-title">AI 智能食谱</h3>
        <p class="intro-desc">基于菜篮子食材 + 家庭成员偏好，智能生成一周食谱</p>
        <van-button type="primary" round size="small" style="margin-top: 8px;" @click="generatePlan">重新生成</van-button>
      </div>

      <div v-if="generating" class="loading-area">
        <van-loading type="spinner" size="32" color="#22c55e" />
        <span>AI 正在为您搭配营养食谱...</span>
      </div>

      <div v-else-if="plan.length > 0">
        <div
          v-for="day in plan"
          :key="day.day"
          class="day-block card-base"
        >
          <div class="day-header flex-between">
            <div>
              <h4 class="day-name">{{ day.day }}</h4>
              <span class="day-date">{{ day.date }}</span>
            </div>
            <div class="day-stats">
              <span class="day-cal">{{ day.dayNutrition.calories }} 千卡</span>
              <span class="day-balance">均衡度 {{ day.dayNutrition.balance }}%</span>
            </div>
          </div>

          <div class="day-meals">
            <div
              v-for="meal in day.meals"
              :key="meal.type"
              class="meal-item"
            >
              <span class="meal-type">{{ meal.type }}</span>
              <span class="meal-name">{{ meal.name }}</span>
              <div class="meal-nutrition">
                <NutriBadge type="protein" label="蛋白" :value="meal.nutrition.protein" unit="g" size="sm" :showValue="true" />
                <NutriBadge type="fiber" label="碳水" :value="meal.nutrition.carbs" unit="g" size="sm" :showValue="true" />
                <NutriBadge type="other" label="卡路里" :value="meal.nutrition.calories" unit="kcal" size="sm" :showValue="true" />
              </div>
              <div class="meal-ingredients">
                <span v-for="ing in meal.ingredients" :key="ing" class="ingredient-tag">{{ ing }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <van-empty description="还没有食谱，点击上方按钮生成" />
      </div>

      <div style="height: 20px;"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppNavbar from '@/components/AppNavbar.vue'
import NutriBadge from '@/components/NutriBadge.vue'
import { generateMealPlan } from '@/api'
import { useAppStore } from '@/stores'
import { Toast } from 'vant'

const store = useAppStore()
const plan = ref([])
const generating = ref(false)

const generatePlan = async () => {
  generating.value = true
  try {
    const res = await generateMealPlan({
      familySize: store.family.members.length,
      preferences: [],
      restrictions: store.taboos.map(t => t.item),
    })
    plan.value = res.data.plan
    Toast.success('食谱已生成')
  } catch {
    Toast.fail('生成失败')
  }
  generating.value = false
}
</script>

<style scoped lang="scss">
.meal-plan-page {
  min-height: 100vh;
  background: var(--ab-bg-page);
}

.page-body {
  padding: var(--ab-space-4);
  padding-bottom: 80px;
}

.plan-intro {
  margin-bottom: var(--ab-space-4);
}

.intro-title {
  font-size: var(--ab-text-lg);
  font-weight: var(--ab-font-bold);
  color: var(--ab-secondary-700);
}

.intro-desc {
  font-size: var(--ab-text-sm);
  color: var(--ab-secondary-600);
  margin-top: 4px;
}

.loading-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--ab-space-3);
  padding: var(--ab-space-10) 0;
  color: var(--ab-text-secondary);
}

.day-block {
  margin-bottom: var(--ab-space-4);
}

.day-header {
  margin-bottom: var(--ab-space-3);
  padding-bottom: var(--ab-space-3);
  border-bottom: 1px solid var(--ab-border-light);
}

.day-name {
  font-size: var(--ab-text-lg);
  font-weight: var(--ab-font-bold);
  color: var(--ab-text-primary);
}

.day-date {
  font-size: var(--ab-text-sm);
  color: var(--ab-text-tertiary);
}

.day-stats {
  text-align: right;
}

.day-cal {
  font-size: var(--ab-text-sm);
  color: var(--ab-secondary-600);
  font-weight: var(--ab-font-medium);
  display: block;
}

.day-balance {
  font-size: var(--ab-text-xs);
  color: var(--ab-success);
}

.day-meals {
  display: flex;
  flex-direction: column;
  gap: var(--ab-space-3);
}

.meal-item {
  padding: var(--ab-space-3);
  background: var(--ab-gray-50);
  border-radius: var(--ab-radius-md);
}

.meal-type {
  display: inline-block;
  padding: 2px 8px;
  background: var(--ab-primary-100);
  color: var(--ab-primary-700);
  font-size: var(--ab-text-xs);
  font-weight: var(--ab-font-bold);
  border-radius: var(--ab-radius-sm);
  margin-bottom: 6px;
}

.meal-name {
  display: block;
  font-size: var(--ab-text-base);
  font-weight: var(--ab-font-medium);
  color: var(--ab-text-primary);
  margin-bottom: 8px;
}

.meal-nutrition {
  display: flex;
  gap: var(--ab-space-2);
  margin-bottom: 8px;
}

.meal-ingredients {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.ingredient-tag {
  padding: 2px 6px;
  background: var(--ab-bg-surface);
  color: var(--ab-text-secondary);
  font-size: var(--ab-text-xs);
  border-radius: var(--ab-radius-sm);
  border: 1px solid var(--ab-border);
}

.empty-state {
  padding-top: var(--ab-space-12);
}
</style>
