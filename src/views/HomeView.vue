<template>
  <!--
    HomeView.vue - 首页 / 家庭营养仪表盘
  -->
  <div class="home-page">
    <!-- 顶部导航 -->
    <AppNavbar title="AI智能菜篮子" :showBack="false" rightIcon="search" />

    <!-- 滚动内容区 -->
    <div class="page-body">
      <!-- 家庭成员栏 -->
      <div class="family-bar card-base">
        <div class="family-info">
          <h2 class="family-name">{{ store.family.name }}</h2>
          <span class="family-members">共 {{ store.family.members.length }} 位成员</span>
        </div>
        <div class="family-avatars">
          <FamilyAvatar
            v-for="m in store.family.members"
            :key="m.id"
            :member="m"
            size="md"
            :showName="true"
            :editable="true"
            @avatar-change="handleAvatarChange"
          />
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
        <div class="action-card" @click="$router.push('/analyze')">
          <div class="action-icon" style="background: #dcfce7;">
            <van-icon name="photo-o" size="24" color="#22c55e" />
          </div>
          <div class="action-text">
            <span class="action-name">拍照识材</span>
            <span class="action-desc">AI识别+营养分析</span>
          </div>
        </div>
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
        <div class="action-card" @click="$router.push('/demo')">
          <div class="action-icon" style="background: #fef3c7;">
            <van-icon name="apps-o" size="24" color="#f59e0b" />
          </div>
          <div class="action-text">
            <span class="action-name">组件展示</span>
            <span class="action-desc">开发用Demo页</span>
          </div>
        </div>
      </div>

      <div style="height: 20px;"></div>
    </div>
  </div>
</template>

<script setup>
import { useAppStore } from '@/stores'
import AppNavbar from '@/components/AppNavbar.vue'
import FamilyAvatar from '@/components/FamilyAvatar.vue'
import AlertBar from '@/components/AlertBar.vue'
import NutriBadge from '@/components/NutriBadge.vue'
import VegCard from '@/components/VegCard.vue'

const store = useAppStore()

/** 用户更换头像 */
const handleAvatarChange = ({ memberId, dataUrl }) => {
  const member = store.family.members.find(m => m.id === memberId)
  if (member) {
    member.avatar = dataUrl
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
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--ab-space-3);
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

.family-avatars {
  display: flex;
  align-items: center;
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
