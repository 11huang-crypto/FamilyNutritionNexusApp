import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/recognize',
    name: 'Recognize',
    component: () => import('../views/Recognize.vue')
  },
  {
    path: '/nutrition',
    name: 'Nutrition',
    component: () => import('../views/Nutrition.vue')
  },
  {
    path: '/family-health',
    name: 'FamilyHealth',
    component: () => import('../views/FamilyHealth.vue')
  },
  {
    path: '/meal-plan',
    name: 'MealPlan',
    component: () => import('../views/MealPlan.vue')
  },
  {
    path: '/shopping-list',
    name: 'ShoppingList',
    component: () => import('../views/ShoppingList.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router