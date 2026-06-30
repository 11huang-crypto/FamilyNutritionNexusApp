<template>
  <div class="meal-plan-page">
    <AppNavbar title="一周食谱" :showBack="true" />

    <div class="page-body">
      <!-- 星期切换 -->
      <div class="week-tabs">
        <div class="week-scroll">
          <button
            v-for="day in weekDays"
            :key="day.key"
            class="week-btn"
            :class="{ active: selectedDay === day.key }"
            @click="selectedDay = day.key"
          >
            {{ day.label }}
          </button>
        </div>
      </div>

      <!-- 当日食谱 -->
      <div class="day-content">
        <div class="meal-section" v-for="meal in mealTypes" :key="meal.key">
          <div class="meal-header clay-card">
            <span class="meal-emoji">{{ meal.emoji }}</span>
            <span class="meal-label">{{ meal.label }}</span>
            <span class="meal-cal">{{ getMealCalories(selectedDay, meal.key) }} kcal</span>
          </div>
          <div class="food-list">
            <div v-for="(food, index) in getMealFoods(selectedDay, meal.key)" :key="index" class="food-item clay-card">
              <div class="food-info">
                <span class="food-emoji">{{ getFoodEmoji(food.name) }}</span>
                <div class="food-text">
                  <span class="food-name">{{ food.name }}</span>
                  <span class="food-desc">{{ food.desc }}</span>
                </div>
              </div>
              <span class="food-cal">{{ food.calories }} kcal</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 生成按钮 -->
      <div class="bottom-bar">
        <button class="clay-btn clay-btn--primary clay-btn--block" @click="generatePlan" :disabled="loading">
          <van-loading v-if="loading" size="18" color="#fff" />
          <span v-else>🔄 重新生成食谱</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { showToast } from 'vant';
import { generateMealPlan } from '../api';
import AppNavbar from '@/components/AppNavbar.vue';

const loading = ref(false);
const selectedDay = ref('monday');

const weekDays = [
  { key: 'monday', label: '周一' }, { key: 'tuesday', label: '周二' },
  { key: 'wednesday', label: '周三' }, { key: 'thursday', label: '周四' },
  { key: 'friday', label: '周五' }, { key: 'saturday', label: '周六' },
  { key: 'sunday', label: '周日' }
];

const mealTypes = [
  { key: 'breakfast', label: '早餐', emoji: '🌅' },
  { key: 'lunch', label: '午餐', emoji: '☀️' },
  { key: 'dinner', label: '晚餐', emoji: '🌙' }
];

const mealPlan = ref({});

const defaultPlan = {
  monday: {
    breakfast: [{ name: '燕麦粥', desc: '健康营养早餐', calories: 150 }, { name: '水煮蛋', desc: '补充蛋白质', calories: 78 }],
    lunch: [{ name: '清蒸鱼', desc: '富含优质蛋白', calories: 200 }, { name: '清炒西兰花', desc: '维生素丰富', calories: 80 }, { name: '杂粮饭', desc: '膳食纤维充足', calories: 150 }],
    dinner: [{ name: '番茄炒蛋', desc: '家常美味', calories: 180 }, { name: '凉拌黄瓜', desc: '清爽可口', calories: 30 }]
  },
  tuesday: {
    breakfast: [{ name: '全麦面包', desc: '粗粮早餐', calories: 120 }, { name: '牛奶', desc: '补充钙质', calories: 100 }],
    lunch: [{ name: '红烧排骨', desc: '营养丰富', calories: 300 }, { name: '蒜蓉油麦菜', desc: '绿色蔬菜', calories: 50 }, { name: '白米饭', desc: '主食', calories: 130 }],
    dinner: [{ name: '豆腐汤', desc: '清淡营养', calories: 100 }, { name: '凉拌鸡丝', desc: '高蛋白低脂肪', calories: 150 }]
  },
  wednesday: {
    breakfast: [{ name: '小米粥', desc: '养胃佳品', calories: 100 }, { name: '茶叶蛋', desc: '风味独特', calories: 80 }],
    lunch: [{ name: '宫保鸡丁', desc: '经典川菜', calories: 250 }, { name: '炒青菜', desc: '新鲜蔬菜', calories: 40 }, { name: '荞麦面', desc: '健康主食', calories: 180 }],
    dinner: [{ name: '清蒸虾', desc: '海鲜美味', calories: 120 }, { name: '冬瓜汤', desc: '清热利湿', calories: 60 }]
  },
  thursday: {
    breakfast: [{ name: '包子', desc: '传统早餐', calories: 150 }, { name: '豆浆', desc: '植物蛋白', calories: 80 }],
    lunch: [{ name: '回锅肉', desc: '川味经典', calories: 320 }, { name: '炒土豆丝', desc: '家常小菜', calories: 100 }, { name: '米饭', desc: '主食', calories: 130 }],
    dinner: [{ name: '蔬菜沙拉', desc: '低脂健康', calories: 150 }, { name: '烤鸡胸肉', desc: '高蛋白', calories: 200 }]
  },
  friday: {
    breakfast: [{ name: '玉米', desc: '粗粮主食', calories: 120 }, { name: '酸奶', desc: '助消化', calories: 100 }],
    lunch: [{ name: '酸菜鱼', desc: '酸辣开胃', calories: 280 }, { name: '炒豆芽', desc: '清爽可口', calories: 60 }, { name: '米饭', desc: '主食', calories: 130 }],
    dinner: [{ name: '蘑菇汤', desc: '鲜美营养', calories: 80 }, { name: '清蒸南瓜', desc: '甜糯可口', calories: 90 }]
  },
  saturday: {
    breakfast: [{ name: '油条', desc: '传统早点', calories: 180 }, { name: '稀饭', desc: '清淡养胃', calories: 80 }],
    lunch: [{ name: '火锅', desc: '家庭聚餐', calories: 400 }, { name: '各种蔬菜', desc: '营养均衡', calories: 100 }],
    dinner: [{ name: '饺子', desc: '传统美食', calories: 250 }]
  },
  sunday: {
    breakfast: [{ name: '三明治', desc: '西式早餐', calories: 200 }, { name: '果汁', desc: '新鲜水果', calories: 80 }],
    lunch: [{ name: '红烧鱼', desc: '营养丰富', calories: 280 }, { name: '清炒时蔬', desc: '绿色健康', calories: 60 }, { name: '米饭', desc: '主食', calories: 130 }],
    dinner: [{ name: '蔬菜粥', desc: '清淡易消化', calories: 120 }, { name: '凉拌番茄', desc: '酸甜可口', calories: 40 }]
  }
};

const getMealFoods = (day, meal) => mealPlan.value[day]?.[meal] || [];
const getMealCalories = (day, meal) => getMealFoods(day, meal).reduce((sum, f) => sum + (f.calories || 0), 0);

const getFoodEmoji = (name) => {
  const map = { '燕麦': '🥣', '蛋': '🥚', '鱼': '🐟', '西兰花': '🥦', '杂粮': '🍚', '番茄': '🍅', '黄瓜': '🥒', '面包': '🍞', '牛奶': '🥛', '排骨': '🍖', '油麦菜': '🥬', '米饭': '🍚', '豆腐': '🫘', '鸡丝': '🐔', '小米': '🥣', '鸡丁': '🐔', '青菜': '🥬', '荞麦': '🍜', '虾': '🦐', '冬瓜': '🎃', '包子': '🥟', '豆浆': '🥛', '回锅肉': '🥩', '土豆': '🥔', '沙拉': '🥗', '鸡胸肉': '🐔', '玉米': '🌽', '酸奶': '🥛', '酸菜鱼': '🐟', '豆芽': '🌱', '蘑菇': '🍄', '南瓜': '🎃', '油条': '🥖', '稀饭': '🥣', '火锅': '🍲', '饺子': '🥟', '三明治': '🥪', '果汁': '🧃', '时蔬': '🥬', '蔬菜粥': '🥣', '番茄': '🍅' };
  for (const [key, emoji] of Object.entries(map)) {
    if (name.includes(key)) return emoji;
  }
  return '🍽️';
};

const generatePlan = async () => {
  loading.value = true;
  try {
    const response = await generateMealPlan({ days: 7, preferences: '均衡营养' });
    if (response.code === 200) mealPlan.value = response.data;
    else { mealPlan.value = defaultPlan; showToast({ type: 'warning', message: '使用默认食谱' }); }
  } catch (e) { mealPlan.value = defaultPlan; }
  finally { loading.value = false; }
};

onMounted(() => { mealPlan.value = defaultPlan; });
</script>

<style scoped lang="scss">
.meal-plan-page { min-height: 100vh; background: transparent; }
.page-body { padding: var(--ab-space-4); padding-bottom: 80px; }

.week-tabs { margin-bottom: var(--ab-space-4); }
.week-scroll { display: flex; gap: var(--ab-space-2); overflow-x: auto; padding-bottom: var(--ab-space-2); }

.week-btn {
  padding: var(--ab-space-2) var(--ab-space-4);
  border: 1px solid var(--ab-border-subtle);
  border-radius: var(--ab-radius-full);
  background: var(--ab-bg-elevated);
  color: var(--ab-text-secondary);
  font-size: var(--ab-text-sm);
  font-weight: var(--ab-font-medium);
  white-space: nowrap;
  cursor: pointer;
  transition: all var(--ab-transition-fast);
  box-shadow: var(--ab-clay-shadow-sm);
  &.active { background: var(--ab-brand-500); color: #fff; border-color: var(--ab-brand-500); }
  &:active { transform: scale(0.95); }
}

.day-content { display: flex; flex-direction: column; gap: var(--ab-space-4); }

.meal-section { display: flex; flex-direction: column; gap: var(--ab-space-3); }

.meal-header {
  display: flex; align-items: center; gap: var(--ab-space-2); padding: var(--ab-space-3) var(--ab-space-4);
}
.meal-emoji { font-size: 24px; }
.meal-label { font-size: var(--ab-text-base); font-weight: var(--ab-font-semibold); flex: 1; }
.meal-cal { font-size: var(--ab-text-sm); color: var(--ab-text-tertiary); }

.food-list { display: flex; flex-direction: column; gap: var(--ab-space-2); }

.food-item {
  display: flex; align-items: center; justify-content: space-between; padding: var(--ab-space-3) var(--ab-space-4);
}
.food-info { display: flex; align-items: center; gap: var(--ab-space-3); }
.food-emoji { font-size: 24px; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.1)); }
.food-text { display: flex; flex-direction: column; gap: 2px; }
.food-name { font-size: var(--ab-text-base); font-weight: var(--ab-font-medium); color: var(--ab-text-primary); }
.food-desc { font-size: var(--ab-text-xs); color: var(--ab-text-tertiary); }
.food-cal { font-size: var(--ab-text-sm); font-weight: var(--ab-font-semibold); color: var(--ab-brand-600); }

.bottom-bar { margin-top: var(--ab-space-4); }
</style>
