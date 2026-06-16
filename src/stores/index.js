import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 本地图片引入
const vegImg = {
  tomatoes: new URL('@/assets/images/vegetable/tomatoes.jpg', import.meta.url).href,
  carrots: new URL('@/assets/images/vegetable/carrots.jpg', import.meta.url).href,
  broccoli: new URL('@/assets/images/vegetable/broccoli.jpg', import.meta.url).href,
  spinach: new URL('@/assets/images/vegetable/spinach.jpg', import.meta.url).href,
}
const fruitImg = {
  apple: new URL('@/assets/images/fruit/apple.jpg', import.meta.url).href,
  banana: new URL('@/assets/images/fruit/banana.jpg', import.meta.url).href,
  orange: new URL('@/assets/images/fruit/orange.jpg', import.meta.url).href,
}

/**
 * 全局状态管理
 * Global State Store
 */
export const useAppStore = defineStore('app', () => {
  // 当前家庭空间信息
  const family = ref({
    id: 'fam_001',
    name: '幸福小家',
    members: [
      { id: 'u1', name: '爸爸', avatar: '', role: 'admin', color: '#3b82f6' },
      { id: 'u2', name: '妈妈', avatar: '', role: 'member', color: '#ec4899' },
      { id: 'u3', name: '宝宝', avatar: '', role: 'member', color: '#f59e0b' },
    ]
  })

  // 当前菜篮子（纯果蔬）
  const basket = ref([
    { id: 1, name: '西红柿', category: '蔬菜', quantity: 3, unit: '个', freshness: 95, image: vegImg.tomatoes, nutrients: { vitaminC: 23, fiber: 1.2 }, addedBy: 'u1', addedAt: '2026-06-06' },
    { id: 2, name: '胡萝卜', category: '蔬菜', quantity: 2, unit: '根', freshness: 88, image: vegImg.carrots, nutrients: { vitaminA: 835, fiber: 2.8 }, addedBy: 'u2', addedAt: '2026-06-05' },
    { id: 3, name: '苹果', category: '水果', quantity: 5, unit: '个', freshness: 92, image: fruitImg.apple, nutrients: { vitaminC: 5, fiber: 2.4 }, addedBy: 'u3', addedAt: '2026-06-06' },
    { id: 4, name: '菠菜', category: '蔬菜', quantity: 1, unit: '把', freshness: 75, image: vegImg.spinach, nutrients: { iron: 2.7, vitaminK: 483 }, addedBy: 'u1', addedAt: '2026-06-04' },
  ])

  // 采购清单（纯果蔬）
  const shoppingList = ref([
    { id: 1, name: '西兰花', category: '蔬菜', quantity: 1, unit: '颗', checked: false, assignedTo: 'u1' },
    { id: 2, name: '猕猴桃', category: '水果', quantity: 6, unit: '个', checked: true, assignedTo: 'u2' },
    { id: 3, name: '草莓', category: '水果', quantity: 1, unit: '盒', checked: false, assignedTo: 'u3' },
    { id: 4, name: '橙子', category: '水果', quantity: 3, unit: '个', checked: false, assignedTo: 'u1' },
  ])

  // 饮食禁忌
  const taboos = ref([
    { memberId: 'u1', item: '菠菜', reason: '痛风' },
    { memberId: 'u3', item: '花生', reason: '过敏' },
  ])

  // 本周营养摄入
  const weeklyNutrition = ref({
    vitaminC: { current: 65, target: 100 },
    fiber: { current: 18, target: 25 },
    protein: { current: 45, target: 60 },
    iron: { current: 8, target: 12 },
    calcium: { current: 500, target: 800 },
  })

  // 警告信息（果蔬相关）
  const alerts = ref([
    { id: 1, type: 'warning', message: '菠菜新鲜度下降至75%，建议尽快食用', icon: 'clock-o' },
    { id: 2, type: 'warning', message: '菠菜 + 黄瓜同食可能影响维生素C吸收', icon: 'warning-o' },
    { id: 3, type: 'info', message: '本周维生素C摄入偏低，建议增加柑橘类水果', icon: 'info-o' },
  ])

  // 计算属性
  const basketCount = computed(() => basket.value.length)
  const pendingShoppingCount = computed(() => shoppingList.value.filter(i => !i.checked).length)
  const activeAlerts = computed(() => alerts.value.filter(a => a.type !== 'info'))

  // Actions
  const addToBasket = (item) => {
    basket.value.unshift({ ...item, id: Date.now(), addedAt: new Date().toISOString().split('T')[0] })
  }

  const removeFromBasket = (id) => {
    basket.value = basket.value.filter(item => item.id !== id)
  }

  const toggleShoppingItem = (id) => {
    const item = shoppingList.value.find(i => i.id === id)
    if (item) item.checked = !item.checked
  }

  const dismissAlert = (id) => {
    alerts.value = alerts.value.filter(a => a.id !== id)
  }

  return {
    family, basket, shoppingList, taboos, weeklyNutrition, alerts,
    basketCount, pendingShoppingCount, activeAlerts,
    addToBasket, removeFromBasket, toggleShoppingItem, dismissAlert
  }
})
