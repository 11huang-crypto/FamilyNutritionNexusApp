import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // 登录页面
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', requiresAuth: false }
  },

  // ========== 需要登录的页面 ==========
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: '首页', requiresAuth: true }
  },
  {
    path: '/recognize',
    name: 'Recognize',
    component: () => import('@/views/Recognize.vue'),
    meta: { title: '拍照识材', requiresAuth: true }
  },
  {
    path: '/nutrition',
    name: 'Nutrition',
    component: () => import('@/views/Nutrition.vue'),
    meta: { title: '营养分析', requiresAuth: true }
  },
  {
    path: '/family-health',
    name: 'FamilyHealth',
    component: () => import('@/views/FamilyHealth.vue'),
    meta: { title: '家庭健康', requiresAuth: true }
  },
  {
    path: '/meal-plan',
    name: 'MealPlan',
    component: () => import('@/views/MealPlan.vue'),
    meta: { title: '食谱推荐', requiresAuth: true }
  },
  {
    path: '/shopping-list',
    name: 'ShoppingList',
    component: () => import('@/views/ShoppingList.vue'),
    meta: { title: '采购清单', requiresAuth: true }
  },

  // ========== 成员4 唐峰 — 公共组件展示与原型页面 ==========
  {
    path: '/demo',
    name: 'demo',
    component: () => import('@/views/DemoView.vue'),
    meta: { title: '组件库展示', requiresAuth: true }
  },
  {
    path: '/analyze',
    name: 'analyze',
    component: () => import('@/views/AnalyzeView.vue'),
    meta: { title: '拍照识材', requiresAuth: true }
  },
  {
    path: '/basket',
    name: 'basket',
    component: () => import('@/views/BasketView.vue'),
    meta: { title: '菜篮子', requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { title: '个人中心', requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// 路由守卫：检查登录状态
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} - AI智能菜篮子`
  }

  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      next('/login')
      return
    }
    
    const tokenPayload = JSON.parse(atob(token.split('.')[1]))
    const now = Math.floor(Date.now() / 1000)
    if (tokenPayload.exp && tokenPayload.exp < now) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('family_id')
      next('/login')
      return
    }
  }

  if (to.path === '/login') {
    const token = localStorage.getItem('token')
    if (token) {
      try {
        const tokenPayload = JSON.parse(atob(token.split('.')[1]))
        const now = Math.floor(Date.now() / 1000)
        if (tokenPayload.exp && tokenPayload.exp > now) {
          next('/')
          return
        }
      } catch (e) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('family_id')
      }
    }
  }

  next()
})

export default router
