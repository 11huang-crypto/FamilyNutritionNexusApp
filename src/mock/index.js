/**
 * ============================================
 * AI智能菜篮子 - Mock 数据服务
 * Mock Data Service (开发环境使用)
 * ============================================
 * 基于接口契约实现Mock，接口联调时切换 baseURL 即可
 *
 * API接口：
 *   POST /api/analyze         - 图片识别+营养分析
 *   GET  /api/family/basket   - 获取家庭菜篮子
 *   POST /api/basket/check    - 扫描禁忌组合
 *   POST /api/meal-plan       - 生成一周食谱
 *   GET  /api/shopping-list   - 获取采购清单
 *   WS   /ws/shopping-list    - 实时协同编辑（WebSocket模拟）
 */

import Mock from 'mockjs'

// 配置Mock
Mock.setup({
  timeout: '200-600' // 模拟网络延迟 200-600ms
})

// ============================================
// 图片引入（本地素材）
// ============================================

const vegImg = {
  tomatoes: new URL('@/assets/images/vegetable/tomatoes.jpg', import.meta.url).href,
  carrots: new URL('@/assets/images/vegetable/carrots.jpg', import.meta.url).href,
  broccoli: new URL('@/assets/images/vegetable/broccoli.jpg', import.meta.url).href,
  cauliflower: new URL('@/assets/images/vegetable/cauliflower.jpg', import.meta.url).href,
  cucumbers: new URL('@/assets/images/vegetable/cucumbers.jpg', import.meta.url).href,
  eggplant: new URL('@/assets/images/vegetable/eggplant.jpg', import.meta.url).href,
  corn: new URL('@/assets/images/vegetable/corn.jpg', import.meta.url).href,
  potatoes: new URL('@/assets/images/vegetable/potatoes.jpg', import.meta.url).href,
  bitterGourd: new URL('@/assets/images/vegetable/bitter gourd.jpg', import.meta.url).href,
  sweetPumpkin: new URL('@/assets/images/vegetable/sweet pumpkin.jpg', import.meta.url).href,
  spinach: new URL('@/assets/images/vegetable/spinach.jpg', import.meta.url).href,
}

const fruitImg = {
  apple: new URL('@/assets/images/fruit/apple.jpg', import.meta.url).href,
  banana: new URL('@/assets/images/fruit/banana.jpg', import.meta.url).href,
  orange: new URL('@/assets/images/fruit/orange.jpg', import.meta.url).href,
  kiwifruit: new URL('@/assets/images/fruit/kiwifruit.jpg', import.meta.url).href,
  pineapple: new URL('@/assets/images/fruit/pineapple.jpg', import.meta.url).href,
  pomegranate: new URL('@/assets/images/fruit/pomegranate.jpg', import.meta.url).href,
  strawberry: new URL('@/assets/images/fruit/strawberriey.jpg', import.meta.url).href,
  lemons: new URL('@/assets/images/fruit/lemons.jpg', import.meta.url).href,
  tangerines: new URL('@/assets/images/fruit/tangerines.jpg', import.meta.url).href,
  watermelon: new URL('@/assets/images/fruit/watermelon.jpg', import.meta.url).href,
}

// ============================================
// 基础数据（纯果蔬，无肉类/蛋奶/豆制品）
// ============================================

const vegDatabase = [
  { name: '西红柿', category: '蔬菜', image: vegImg.tomatoes, nutrients: { vitaminC: 23, fiber: 1.2, vitaminA: 42, potassium: 237 } },
  { name: '胡萝卜', category: '蔬菜', image: vegImg.carrots, nutrients: { vitaminA: 835, fiber: 2.8, vitaminC: 6, potassium: 320 } },
  { name: '苹果', category: '水果', image: fruitImg.apple, nutrients: { vitaminC: 5, fiber: 2.4, potassium: 107, sugar: 10 } },
  { name: '菠菜', category: '蔬菜', image: vegImg.spinach, nutrients: { iron: 2.7, vitaminK: 483, vitaminC: 28, fiber: 2.2 } },
  { name: '香蕉', category: '水果', image: fruitImg.banana, nutrients: { potassium: 358, vitaminC: 8.7, fiber: 2.6, sugar: 12 } },
  { name: '西兰花', category: '蔬菜', image: vegImg.broccoli, nutrients: { vitaminC: 89, fiber: 2.6, vitaminK: 101, iron: 0.7 } },
  { name: '橙子', category: '水果', image: fruitImg.orange, nutrients: { vitaminC: 53, fiber: 2.4, folate: 30, potassium: 181 } },
  { name: '蓝莓', category: '水果', image: fruitImg.strawberry, nutrients: { vitaminC: 9.7, fiber: 2.4, vitaminK: 19, anthocyanin: 163 } },
  { name: '黄瓜', category: '蔬菜', image: vegImg.cucumbers, nutrients: { vitaminC: 2.8, fiber: 0.5, potassium: 147, vitaminK: 16 } },
  { name: '南瓜', category: '蔬菜', image: vegImg.sweetPumpkin, nutrients: { vitaminA: 310, fiber: 0.5, potassium: 340, vitaminC: 9 } },
  { name: '茄子', category: '蔬菜', image: vegImg.eggplant, nutrients: { fiber: 1.8, potassium: 123, vitaminK: 3.5 } },
  { name: '玉米', category: '蔬菜', image: vegImg.corn, nutrients: { fiber: 2.7, vitaminC: 6.8, potassium: 270, sugar: 6.3 } },
  { name: '猕猴桃', category: '水果', image: fruitImg.kiwifruit, nutrients: { vitaminC: 93, fiber: 3, potassium: 312, vitaminK: 40 } },
  { name: '菠萝', category: '水果', image: fruitImg.pineapple, nutrients: { vitaminC: 48, fiber: 1.4, manganese: 0.93, sugar: 10 } },
  { name: '苦瓜', category: '蔬菜', image: vegImg.bitterGourd, nutrients: { vitaminC: 84, fiber: 3, iron: 0.4, potassium: 299 } },
  { name: '土豆', category: '蔬菜', image: vegImg.potatoes, nutrients: { vitaminC: 20, fiber: 2.2, potassium: 421, vitaminB6: 0.3 } },
  { name: '草莓', category: '水果', image: fruitImg.strawberry, nutrients: { vitaminC: 59, fiber: 2, folate: 24, manganese: 0.39 } },
  { name: '柠檬', category: '水果', image: fruitImg.lemons, nutrients: { vitaminC: 53, fiber: 2.8, potassium: 138, folate: 11 } },
  { name: '西瓜', category: '水果', image: fruitImg.watermelon, nutrients: { vitaminC: 8.1, vitaminA: 28, potassium: 112, sugar: 6 } },
  { name: '石榴', category: '水果', image: fruitImg.pomegranate, nutrients: { vitaminC: 10, fiber: 4, folate: 38, potassium: 236 } },
]

const familyMembers = [
  { id: 'u1', name: '爸爸', avatar: '', role: 'admin', color: '#3b82f6' },
  { id: 'u2', name: '妈妈', avatar: '', role: 'member', color: '#ec4899' },
  { id: 'u3', name: '宝宝', avatar: '', role: 'member', color: '#f59e0b' },
]

let basketItems = [
  { id: 1, name: '西红柿', category: '蔬菜', quantity: 3, unit: '个', freshness: 95, image: vegDatabase[0].image, nutrients: vegDatabase[0].nutrients, addedBy: 'u1', addedAt: '2026-06-06' },
  { id: 2, name: '胡萝卜', category: '蔬菜', quantity: 2, unit: '根', freshness: 88, image: vegDatabase[1].image, nutrients: vegDatabase[1].nutrients, addedBy: 'u2', addedAt: '2026-06-05' },
  { id: 3, name: '苹果', category: '水果', quantity: 5, unit: '个', freshness: 92, image: vegDatabase[2].image, nutrients: vegDatabase[2].nutrients, addedBy: 'u3', addedAt: '2026-06-06' },
  { id: 4, name: '菠菜', category: '蔬菜', quantity: 1, unit: '把', freshness: 75, image: vegDatabase[3].image, nutrients: vegDatabase[3].nutrients, addedBy: 'u1', addedAt: '2026-06-04' },
  { id: 5, name: '香蕉', category: '水果', quantity: 4, unit: '根', freshness: 80, image: vegDatabase[4].image, nutrients: vegDatabase[4].nutrients, addedBy: 'u2', addedAt: '2026-06-03' },
]

let shoppingItems = [
  { id: 1, name: '西兰花', category: '蔬菜', quantity: 1, unit: '颗', checked: false, assignedTo: 'u1' },
  { id: 2, name: '猕猴桃', category: '水果', quantity: 6, unit: '个', checked: true, assignedTo: 'u2' },
  { id: 3, name: '草莓', category: '水果', quantity: 1, unit: '盒', checked: false, assignedTo: 'u3' },
  { id: 4, name: '玉米', category: '蔬菜', quantity: 2, unit: '根', checked: false, assignedTo: 'u1' },
  { id: 5, name: '柠檬', category: '水果', quantity: 3, unit: '个', checked: false, assignedTo: 'u2' },
]

let nextId = 100

// ============================================
// API Mock 接口
// ============================================

// POST /api/analyze - 图片识别+营养分析
Mock.mock('/api/analyze', 'post', (options) => {
  const body = JSON.parse(options.body || '{}')

  // 随机选1-2个食材返回
  const count = Mock.Random.integer(1, 2)
  const results = Mock.Random.shuffle(vegDatabase).slice(0, count).map(item => ({
    ...item,
    confidence: Mock.Random.float(85, 99, 1, 1),
    recognitionTime: '0.8s',
  }))

  // 可能触发禁忌检查（果蔬禁忌组合）
  const hasTaboo = results.some(r =>
    r.name === '菠菜' && results.some(r2 => r2.name === '黄瓜')
  )
  const alerts = hasTaboo ? [
    { type: 'warning', message: '提示：菠菜 + 黄瓜同食可能影响维生素C吸收', icon: 'warning-o' }
  ] : []

  // 价格估算
  const units = ['斤', '个', '把', '颗', '根', '盒']
  const estimatedPrices = results.map(r => ({
    name: r.name,
    price: Mock.Random.float(2, 15, 2, 2),
    unit: '元/' + units[Mock.Random.integer(0, 5)],
  }))

  return {
    code: 200,
    data: { results, alerts, estimatedPrices, totalItems: results.length },
    message: '识别成功'
  }
})

// GET /api/family/basket - 获取家庭菜篮子
Mock.mock('/api/family/basket', 'get', {
  code: 200,
  data: () => ({
    items: basketItems,
    total: basketItems.length,
    summary: {
      vegetableCount: basketItems.filter(i => i.category === '蔬菜').length,
      fruitCount: basketItems.filter(i => i.category === '水果').length,
      lowFreshness: basketItems.filter(i => i.freshness < 80),
    }
  }),
  message: 'ok'
})

// POST /api/basket/check - 扫描禁忌组合
Mock.mock('/api/basket/check', 'post', (options) => {
  const body = JSON.parse(options.body || '{}')
  const itemNames = body.items || basketItems.map(i => i.name)

  // 已知果蔬禁忌组合
  const tabooPairs = [
    { items: ['菠菜', '黄瓜'], reason: '同食可能影响维生素C吸收', severity: 'warning' },
    { items: ['西红柿', '南瓜'], reason: '南瓜含维生素C分解酶，同食降低西红柿营养', severity: 'info' },
    { items: ['橘子', '萝卜'], reason: '可能诱发甲状腺肿', severity: 'warning' },
  ]

  const found = tabooPairs.filter(pair =>
    pair.items.every(item => itemNames.includes(item))
  )

  return {
    code: 200,
    data: {
      hasConflict: found.length > 0,
      conflicts: found,
      checkedCount: itemNames.length,
      checkedAt: new Date().toISOString(),
    },
    message: found.length > 0 ? `发现${found.length}条风险` : '未发现禁忌组合'
  }
})

// POST /api/meal-plan - 生成一周食谱（纯素）
Mock.mock('/api/meal-plan', 'post', (options) => {
  const body = JSON.parse(options.body || '{}')
  const familySize = body.familySize || 3

  const weekDays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  const mealTypes = ['breakfast', 'lunch', 'dinner']

  const mealNames = {
    breakfast: ['杂粮粥+水果拼盘', '南瓜小米粥', '豆浆+全麦面包', '燕麦水果碗', '红薯粥+坚果', '玉米汁+素包子', '番茄蔬菜面'],
    lunch: ['番茄炒蛋+米饭', '西兰花炒胡萝卜+米饭', '凉拌黄瓜+清炒菠菜', '红烧茄子+炒时蔬', '蒜蓉西兰花+蒸玉米', '酸辣土豆丝+米饭', '素炒三鲜+米饭'],
    dinner: ['蔬菜浓汤', '菌菇汤面', '凉拌西红柿+小米粥', '素炒苦瓜+杂粮饭', '南瓜汤+素饺子', '番茄意面', '蔬菜沙拉+水果拼盘'],
  }

  const plan = weekDays.map((day, di) => ({
    day,
    date: getDateStr(di),
    meals: mealTypes.map(type => ({
      type: type === 'breakfast' ? '早餐' : type === 'lunch' ? '午餐' : '晚餐',
      name: mealNames[type][di],
      nutrition: {
        calories: Mock.Random.integer(300, 700),
        protein: Mock.Random.float(10, 30, 1, 1),
        carbs: Mock.Random.float(30, 80, 1, 1),
        fat: Mock.Random.float(5, 20, 1, 1)
      },
      ingredients: Mock.Random.shuffle(vegDatabase).slice(0, 4).map(v => v.name),
    })),
    dayNutrition: {
      calories: Mock.Random.integer(1400, 2000),
      protein: Mock.Random.float(40, 70, 1, 1),
      balance: Mock.Random.integer(70, 95),
    }
  }))

  return {
    code: 200,
    data: { plan, familySize, generatedAt: new Date().toISOString() },
    message: '食谱生成成功'
  }
})

// GET /api/shopping-list - 获取采购清单
Mock.mock('/api/shopping-list', 'get', {
  code: 200,
  data: () => ({
    items: shoppingItems,
    total: shoppingItems.length,
    completed: shoppingItems.filter(i => i.checked).length,
    assignees: familyMembers.map(m => ({
      ...m,
      count: shoppingItems.filter(i => i.assignedTo === m.id).length,
      completed: shoppingItems.filter(i => i.assignedTo === m.id && i.checked).length,
    }))
  }),
  message: 'ok'
})

// POST /api/shopping-list/add - 添加采购项
Mock.mock('/api/shopping-list/add', 'post', (options) => {
  const body = JSON.parse(options.body || '{}')
  const newItem = {
    id: nextId++,
    name: body.name,
    category: body.category || '其他',
    quantity: body.quantity || 1,
    unit: body.unit || '个',
    checked: false,
    assignedTo: body.assignedTo || 'u1',
  }
  shoppingItems.unshift(newItem)
  return { code: 200, data: newItem, message: '添加成功' }
})

// PUT /api/shopping-list/toggle - 切换选中状态
Mock.mock('/api/shopping-list/toggle', 'put', (options) => {
  const body = JSON.parse(options.body || '{}')
  const item = shoppingItems.find(i => i.id === body.id)
  if (item) item.checked = !item.checked
  return { code: 200, data: item, message: 'ok' }
})

// ============================================
// 工具函数
// ============================================

function getDateStr(offset) {
  const d = new Date()
  d.setDate(d.getDate() + offset)
  return (d.getMonth() + 1) + '/' + d.getDate()
}

console.log('[Mock] AI智能菜篮子 Mock数据服务已启动，共注册 6 个接口')
console.log('[Mock] 接口列表：POST /api/analyze, GET /api/family/basket, POST /api/basket/check, POST /api/meal-plan, GET /api/shopping-list, POST /api/shopping-list/add')
