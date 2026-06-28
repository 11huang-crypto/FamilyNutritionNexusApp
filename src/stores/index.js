import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '../utils/axios'

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
    id: null,
    name: '我的家庭',
    members: []
  })

  // 当前菜篮子
  const basket = ref([])

  // 采购清单
  const shoppingList = ref([])

  // 饮食禁忌
  const taboos = ref([])

  // 本周营养摄入（使用 Mock 数据，因为后端暂无此接口）
  const weeklyNutrition = ref({
    vitaminC: { current: 65, target: 100 },
    fiber: { current: 18, target: 25 },
    protein: { current: 45, target: 60 },
    iron: { current: 8, target: 12 },
    calcium: { current: 500, target: 800 },
  })

  // 警告信息
  const alerts = ref([])

  // 加载状态
  const loading = ref(false)

  // 计算属性
  const basketCount = computed(() => basket.value.length)
  const pendingShoppingCount = computed(() => shoppingList.value.filter(i => !i.checked).length)
  const activeAlerts = computed(() => alerts.value.filter(a => a.type !== 'info'))

  /**
   * 加载家庭数据
   */
  const loadFamilyData = async () => {
    try {
      loading.value = true
      const response = await axios.get('/family/my')
      // 后端返回格式：{"families": [...]}
      const families = response.families || response
      if (families && families.length > 0) {
        family.value = {
          ...families[0],
          members: []
        }
        localStorage.setItem('family_id', family.value.id.toString())
      }
    } catch (error) {
      console.error('加载家庭数据失败:', error)
    } finally {
      loading.value = false
    }
  }

  /**
   * 创建家庭
   */
  const createFamily = async (familyData) => {
    try {
      loading.value = true
      const response = await axios.post('/family/create', familyData)
      if (response && response.id) {
        family.value = response
        localStorage.setItem('family_id', response.id.toString())
      }
      return response
    } catch (error) {
      console.error('创建家庭失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * 加载菜篮子数据
   */
  const loadBasketData = async () => {
    try {
      const family_id = localStorage.getItem('family_id')
      if (!family_id) return
      
      const response = await axios.get(`/basket/family/${family_id}`)
      if (response && response.items) {
        // 转换数据格式，添加本地图片
        basket.value = response.items.map((item, index) => ({
          ...item,
          image: index % 2 === 0 ? vegImg.tomatoes : fruitImg.apple,
          freshness: 80 + Math.floor(Math.random() * 20)
        }))
        
        // 根据健康档案生成警告
        generateAlerts()
      }
    } catch (error) {
      console.error('加载菜篮子数据失败:', error)
      // 使用 Mock 数据作为降级方案
      basket.value = [
        { id: 1, name: '西红柿', category: '蔬菜', quantity: 3, unit: '个', freshness: 95, image: vegImg.tomatoes, nutrients: { vitaminC: 23, fiber: 1.2 }, addedBy: 'u1', addedAt: '2026-06-06' },
        { id: 2, name: '胡萝卜', category: '蔬菜', quantity: 2, unit: '根', freshness: 88, image: vegImg.carrots, nutrients: { vitaminA: 835, fiber: 2.8 }, addedBy: 'u2', addedAt: '2026-06-05' },
        { id: 3, name: '苹果', category: '水果', quantity: 5, unit: '个', freshness: 92, image: fruitImg.apple, nutrients: { vitaminC: 5, fiber: 2.4 }, addedBy: 'u3', addedAt: '2026-06-06' },
        { id: 4, name: '菠菜', category: '蔬菜', quantity: 1, unit: '把', freshness: 75, image: vegImg.spinach, nutrients: { iron: 2.7, vitaminK: 483 }, addedBy: 'u1', addedAt: '2026-06-04' },
      ]
    }
  }

  /**
   * 添加食材到菜篮子
   */
  const addToBasket = async (item) => {
    try {
      const family_id = localStorage.getItem('family_id')
      const response = await axios.post('/basket/item', {
        family_id: parseInt(family_id),
        ...item
      })
      
      // 重新加载菜篮子
      await loadBasketData()
      return response
    } catch (error) {
      console.error('添加食材失败:', error)
      throw error
    }
  }

  /**
   * 移除食材
   */
  const removeFromBasket = (id) => {
    basket.value = basket.value.filter(item => item.id !== id)
  }

  /**
   * 检查食材禁忌
   */
  const checkFoodConflicts = async () => {
    try {
      const family_id = localStorage.getItem('family_id')
      if (!family_id) return
      
      const response = await axios.get(`/basket/check?family_id=${family_id}`)
      if (response && response.conflicts) {
        return response.conflicts
      }
      return []
    } catch (error) {
      console.error('检查食材禁忌失败:', error)
      return []
    }
  }

  /**
   * 生成警告信息
   */
  const generateAlerts = async () => {
    const newAlerts = []
    
    // 检查新鲜度
    basket.value.forEach(item => {
      if (item.freshness && item.freshness < 80) {
        newAlerts.push({
          id: Date.now() + Math.random(),
          type: 'warning',
          message: `${item.name}新鲜度下降至${item.freshness}%，建议尽快食用`,
          icon: 'clock-o'
        })
      }
    })
    
    // 检查食材禁忌
    const conflicts = await checkFoodConflicts()
    conflicts.forEach(conflict => {
      newAlerts.push({
        id: Date.now() + Math.random(),
        type: 'warning',
        message: `${conflict.food1} + ${conflict.food2}: ${conflict.reason}`,
        icon: 'warning-o'
      })
    })
    
    // 营养建议
    Object.entries(weeklyNutrition.value).forEach(([key, val]) => {
      const percent = (val.current / val.target) * 100
      if (percent < 70) {
        const labels = {
          vitaminC: '维生素C',
          fiber: '膳食纤维',
          protein: '蛋白质',
          iron: '铁元素',
          calcium: '钙元素'
        }
        newAlerts.push({
          id: Date.now() + Math.random(),
          type: 'info',
          message: `本周${labels[key]}摄入偏低，建议增加相关食物`,
          icon: 'info-o'
        })
      }
    })
    
    alerts.value = newAlerts.slice(0, 5) // 最多显示5条警告
  }

  /**
   * 加载采购清单
   */
  const loadShoppingList = async () => {
    try {
      const family_id = localStorage.getItem('family_id')
      if (!family_id) return
      
      const response = await axios.get(`/shopping-list/realtime?family_id=${family_id}`)
      if (response && response.items) {
        shoppingList.value = response.items
      }
    } catch (error) {
      console.error('加载采购清单失败:', error)
      // 使用 Mock 数据作为降级方案
      shoppingList.value = [
        { id: 1, name: '西兰花', category: '蔬菜', quantity: 1, unit: '颗', checked: false },
        { id: 2, name: '猕猴桃', category: '水果', quantity: 6, unit: '个', checked: true },
        { id: 3, name: '草莓', category: '水果', quantity: 1, unit: '盒', checked: false },
        { id: 4, name: '橙子', category: '水果', quantity: 3, unit: '个', checked: false },
      ]
    }
  }

  /**
   * 切换采购项状态
   */
  const toggleShoppingItem = (id) => {
    const item = shoppingList.value.find(i => i.id === id)
    if (item) item.checked = !item.checked
  }

  /**
   * 关闭警告
   */
  const dismissAlert = (id) => {
    alerts.value = alerts.value.filter(a => a.id !== id)
  }

  /**
   * 加载所有数据
   */
  const loadAllData = async () => {
    await loadFamilyData()
    await loadBasketData()
    await loadShoppingList()
  }

  /**
   * 退出登录
   */
  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('family_id')
    family.value = { id: null, name: '我的家庭', members: [] }
    basket.value = []
    shoppingList.value = []
    taboos.value = []
    alerts.value = []
  }

  return {
    family, basket, shoppingList, taboos, weeklyNutrition, alerts,
    basketCount, pendingShoppingCount, activeAlerts, loading,
    loadFamilyData, createFamily, loadBasketData, addToBasket,
    removeFromBasket, checkFoodConflicts, generateAlerts,
    loadShoppingList, toggleShoppingItem, dismissAlert, loadAllData,
    logout
  }
})
