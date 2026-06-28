<template>
  <!--
    HomeView.vue - 首页 / 家庭营养仪表盘
  -->
  <div class="home-page">
    <!-- 顶部导航 -->
    <AppNavbar title="AI智能菜篮子" :showBack="false" />

    <!-- 滚动内容区 -->
    <div class="page-body">
      <!-- 家庭成员栏 -->
      <div class="family-bar card-base">
        <div class="family-header">
          <div class="family-info">
            <h2 class="family-name">{{ store.family.name }}</h2>
            <span class="family-members">共 {{ store.family.members.length }} 位成员</span>
          </div>
          <button class="family-more" @click="$router.push('/profile')">
            <van-icon name="arrow" size="16" />
          </button>
        </div>
        <div class="family-avatars">
          <div v-for="m in store.family.members" :key="m.id" class="family-avatar-item">
            <div class="avatar-circle">
              <van-icon name="user" size="20" color="#fff" />
            </div>
            <span class="avatar-name">{{ m.name }}</span>
          </div>
          <button class="add-avatar-btn" @click="$router.push('/profile')">
            <van-icon name="plus" size="16" color="#22c55e" />
          </button>
        </div>
      </div>

      <!-- 警告区 -->
      <div class="alerts-area">
        <AlertBar
          v-for="alert in store.alerts"
          :key="alert.id"
          :type="alert.type"
          :message="alert.message"
          :icon="alert.icon"
          :closable="true"
          @close="store.dismissAlert(alert.id)"
        />
      </div>

      <!-- 营养仪表盘 -->
      <div class="section-header flex-between">
        <h3 class="section-label">本周营养摄入</h3>
        <span class="section-extra" @click="$router.push('/basket')">查看详情 →</span>
      </div>
      <div class="nutrition-dashboard grid-2col">
        <NutriBadge
          v-for="(val, key) in store.weeklyNutrition"
          :key="key"
          :type="getType(key)"
          :label="getLabel(key)"
          :value="val.current"
          :percent="Math.round((val.current / val.target) * 100)"
          size="lg"
        />
      </div>

      <!-- 菜篮子预览 -->
      <div class="section-header flex-between">
        <h3 class="section-label">家庭菜篮子</h3>
        <span class="section-count">{{ store.basketCount }} 件</span>
      </div>
      <div class="basket-preview">
        <VegCard
          v-for="item in store.basket.slice(0, 4)"
          :key="item.id"
          :item="item"
          variant="list"
          :showFreshness="true"
          :showNutrients="true"
          @click="$router.push('/basket')"
        />
        <div v-if="store.basket.length > 4" class="more-hint" @click="$router.push('/basket')">
          查看全部 {{ store.basketCount }} 件 →
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="section-header">
        <h3 class="section-label">快捷操作</h3>
      </div>
      <div class="quick-actions grid-2col">
        <div class="action-card" @click="$router.push('/meal-plan')">
          <div class="action-icon" style="background: #fff7ed;">
            <van-icon name="description-o" size="24" color="#f97316" />
          </div>
          <div class="action-text">
            <span class="action-name">生成食谱</span>
            <span class="action-desc">智能一周食谱</span>
          </div>
        </div>
        <div class="action-card" @click="$router.push('/shopping-list')">
          <div class="action-icon" style="background: #eff6ff;">
            <van-icon name="todo-list-o" size="24" color="#3b82f6" />
          </div>
          <div class="action-text">
            <span class="action-name">采购清单</span>
            <span class="action-desc">{{ store.pendingShoppingCount }} 项待购</span>
          </div>
        </div>
        <div class="action-card" @click="$router.push('/family-health')">
          <div class="action-icon" style="background: #fee2e2;">
            <van-icon name="heart-o" size="24" color="#ef4444" />
          </div>
          <div class="action-text">
            <span class="action-name">健康档案</span>
            <span class="action-desc">管理家庭成员健康</span>
          </div>
        </div>
      </div>

      <div style="height: 20px;"></div>
    </div>

    <!-- 底部导航栏 -->
    <AppTabbar :active="0" @change="handleTabChange" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import AppNavbar from '@/components/AppNavbar.vue'
import AppTabbar from '@/components/AppTabbar.vue'
import FamilyAvatar from '@/components/FamilyAvatar.vue'
import AlertBar from '@/components/AlertBar.vue'
import NutriBadge from '@/components/NutriBadge.vue'
import VegCard from '@/components/VegCard.vue'

const store = useAppStore()
const router = useRouter()

/** 页面加载时获取数据 */
onMounted(() => {
  store.loadAllData()
})

/** 用户更换头像 */
const handleAvatarChange = ({ memberId, dataUrl }) => {
  const member = store.family.members.find(m => m.id === memberId)
  if (member) {
    member.avatar = dataUrl
  }
}

/** 底部导航切换 */
const handleTabChange = (index, item) => {
  if (item.path) {
    router.push(item.path)
  }
}

const getType = (key) => {
  const map = {
    vitaminC: 'vitamin', fiber: 'fiber', protein: 'protein',
    iron: 'mineral', calcium: 'mineral'
  }
  return map[key] || 'other'
}

const getLabel = (key) => {
  const map = {
    vitaminC: '维生素C', fiber: '膳食纤维', protein: '蛋白质',
    iron: '铁元素', calcium: '钙元素'
  }
  return map[key] || key
}
</script>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  background: var(--ab-bg-page);
  display: flex;
  flex-direction: column;
}

.page-body {
  flex: 1;
  padding: var(--ab-space-4);
  padding-bottom: 80px;
}

.family-bar {
  display: flex;
  flex-direction: column;
  gap: var(--ab-space-3);
  margin-bottom: var(--ab-space-3);
  padding: var(--ab-space-4);
}

.family-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.family-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.family-name {
  font-size: var(--ab-text-lg);
  font-weight: var(--ab-font-bold);
  color: var(--ab-text-primary);
}

.family-members {
  font-size: var(--ab-text-xs);
  color: var(--ab-text-tertiary);
}

.family-more {
  padding: 8px;
  border: none;
  background: transparent;
  color: var(--ab-text-tertiary);
  cursor: pointer;
}

.family-avatars {
  display: flex;
  align-items: center;
  gap: var(--ab-space-3);
  overflow-x: auto;
  padding-bottom: var(--ab-space-1);
}

.family-avatar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.avatar-circle {
  width: 44px;
  height: 44px;
  border-radius: var(--ab-radius-full);
  background: linear-gradient(135deg, var(--ab-primary-400) 0%, var(--ab-primary-600) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-name {
  font-size: var(--ab-text-xs);
  color: var(--ab-text-secondary);
}

.add-avatar-btn {
  width: 44px;
  height: 44px;
  border-radius: var(--ab-radius-full);
  border: 2px dashed var(--ab-primary-300);
  background: var(--ab-primary-50);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  cursor: pointer;
  transition: all var(--ab-transition-fast);

  &:active {
    background: var(--ab-primary-100);
  }
}

.alerts-area {
  margin-bottom: var(--ab-space-4);
}

.section-header {
  margin-bottom: var(--ab-space-3);
  margin-top: var(--ab-space-2);
}

.section-label {
  font-size: var(--ab-text-base);
  font-weight: var(--ab-font-bold);
  color: var(--ab-text-primary);
}

.section-extra {
  font-size: var(--ab-text-sm);
  color: var(--ab-primary-600);
  cursor: pointer;
}

.section-count {
  font-size: var(--ab-text-sm);
  color: var(--ab-text-tertiary);
}

.nutrition-dashboard {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--ab-space-3);
  margin-bottom: var(--ab-space-4);
}

.basket-preview {
  display: flex;
  flex-direction: column;
  gap: var(--ab-space-2);
  margin-bottom: var(--ab-space-4);
}

.more-hint {
  text-align: center;
  padding: var(--ab-space-3);
  font-size: var(--ab-text-sm);
  color: var(--ab-primary-600);
  font-weight: var(--ab-font-medium);
  cursor: pointer;
}

.quick-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--ab-space-3);
}

.action-card {
  display: flex;
  align-items: center;
  gap: var(--ab-space-3);
  background: var(--ab-bg-card);
  border-radius: var(--ab-radius-lg);
  padding: var(--ab-space-4);
  box-shadow: var(--ab-shadow-sm);
  cursor: pointer;
  transition: all var(--ab-transition-fast);

  &:active {
    transform: scale(0.97);
    box-shadow: var(--ab-shadow-md);
  }
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--ab-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.action-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.action-name {
  font-size: var(--ab-text-base);
  font-weight: var(--ab-font-bold);
  color: var(--ab-text-primary);
}

.action-desc {
  font-size: var(--ab-text-xs);
  color: var(--ab-text-tertiary);
}

.grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--ab-space-3);
}
</style>
