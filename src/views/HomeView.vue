<template>
  <div class="home-page">
    <!-- 顶部毛玻璃导航 -->
    <div class="top-nav">
      <div class="greeting">
        <span class="greeting-emoji">👋</span>
        <span class="greeting-text">你好，{{ store.userInfo?.name || store.userInfo?.username || 'Lappy' }}</span>
      </div>
      <button class="notif-btn" @click="$router.push('/family-health')">
        <LocalIcon name="bell" size="22" />
        <span v-if="store.alerts.length" class="notif-dot"></span>
      </button>
    </div>

    <div class="page-body">
      <!-- Hero 区域：Mintlify 风的品牌绿大色块 -->
      <div class="hero-section">
        <div class="hero-bg-deco">
          <div class="deco-blob deco-blob--1"></div>
          <div class="deco-blob deco-blob--2"></div>
          <div class="deco-blob deco-blob--3"></div>
        </div>
        <div class="hero-content">
          <div class="hero-tag">家庭营养 · AI 助手</div>
          <h1 class="hero-title">
            <span class="hero-line">吃得更</span>
            <span class="hero-line">
              <span class="hero-highlight">聪明</span>
              <span class="hero-suffix">一点</span>
            </span>
          </h1>
          <p class="hero-desc">AI 智能菜篮子，让健康饮食更简单</p>
        </div>
        <div class="hero-cta">
          <button class="clay-btn clay-btn--primary" @click="$router.push('/recognize')">
            <LocalIcon name="photograph" size="20" />
            <span>开始拍照</span>
          </button>
        </div>
      </div>

      <!-- 家庭成员栏 (ClayCard 浮起) -->
      <div class="clay-card family-bar clay-card--soft-brand">
        <div class="family-header">
          <div class="family-info">
            <span class="family-eyebrow">FAMILY</span>
            <h2 class="family-name">{{ store.family.name }}</h2>
            <span class="family-members">共 {{ store.family.members.length }} 位成员</span>
          </div>
          <button class="family-more" @click="$router.push('/profile')">
            <span>管理</span>
            <LocalIcon name="arrow" size="14" />
          </button>
        </div>
        <div class="family-avatars">
          <div v-for="m in store.family.members" :key="m.id" class="family-avatar-item">
            <div class="avatar-circle">
              <LocalIcon name="user" size="20" color="#fff" />
            </div>
            <span class="avatar-name">{{ m.name }}</span>
          </div>
          <button class="add-avatar-btn" @click="$router.push('/profile')">
            <LocalIcon name="plus" size="18" color="var(--ab-brand-600)" />
          </button>
        </div>
      </div>

      <!-- 6 格快捷功能 — 真 Clay 彩色底 -->
      <div class="quick-grid">
        <div class="quick-item" @click="$router.push('/recognize')">
          <ClayIcon color="orange" size="lg">
            <LocalIcon name="camera" size="32" />
          </ClayIcon>
          <span class="quick-label">拍照识别</span>
        </div>
        <div class="quick-item" @click="$router.push('/family-health')">
          <ClayIcon color="peach" size="lg">
            <LocalIcon name="like-o" size="32" />
          </ClayIcon>
          <span class="quick-label">健康档案</span>
        </div>
        <div class="quick-item" @click="$router.push('/meal-plan')">
          <ClayIcon color="blue" size="lg">
            <LocalIcon name="calendar-o" size="32" />
          </ClayIcon>
          <span class="quick-label">一周食谱</span>
        </div>
        <div class="quick-item" @click="$router.push('/shopping-list')">
          <ClayIcon color="mint" size="lg">
            <LocalIcon name="list" size="32" />
          </ClayIcon>
          <span class="quick-label">采购清单</span>
        </div>
        <div class="quick-item" @click="$router.push('/basket')">
          <ClayIcon color="brand" size="lg">
            <LocalIcon name="shopping-cart-o" size="32" />
          </ClayIcon>
          <span class="quick-label">菜篮子</span>
        </div>
        <div class="quick-item" @click="$router.push('/family-health')">
          <ClayIcon color="lilac" size="lg">
            <LocalIcon name="warning-o" size="32" />
          </ClayIcon>
          <span class="quick-label">风险预警</span>
        </div>
      </div>

      <!-- 警告区 -->
      <div v-if="store.alerts.length" class="alerts-area">
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

      <!-- 本周营养摄入 -->
      <div class="section-header">
        <div>
          <span class="section-eyebrow">WEEKLY NUTRITION</span>
          <h3 class="section-label">本周营养摄入</h3>
        </div>
        <span class="section-extra" @click="$router.push('/basket')">详情 →</span>
      </div>
      <div class="nutrition-dashboard">
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
      <div class="section-header">
        <div>
          <span class="section-eyebrow">BASKET</span>
          <h3 class="section-label">家庭菜篮子</h3>
        </div>
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
        <div>
          <span class="section-eyebrow">QUICK ACTIONS</span>
          <h3 class="section-label">快捷操作</h3>
        </div>
      </div>
      <div class="quick-actions">
        <div class="action-card" @click="$router.push('/meal-plan')">
          <ClayIcon color="soft-orange" size="md">
            <LocalIcon name="description-o" size="22" color="var(--ab-orange-500)" />
          </ClayIcon>
          <div class="action-text">
            <span class="action-name">生成食谱</span>
            <span class="action-desc">智能一周食谱</span>
          </div>
          <LocalIcon name="arrow" size="16" color="var(--ab-text-tertiary)" />
        </div>
        <div class="action-card" @click="$router.push('/shopping-list')">
          <ClayIcon color="soft-blue" size="md">
            <LocalIcon name="todo-list-o" size="22" color="var(--ab-blue-500)" />
          </ClayIcon>
          <div class="action-text">
            <span class="action-name">采购清单</span>
            <span class="action-desc">{{ store.pendingShoppingCount }} 项待购</span>
          </div>
          <LocalIcon name="arrow" size="16" color="var(--ab-text-tertiary)" />
        </div>
        <div class="action-card" @click="$router.push('/family-health')">
          <ClayIcon color="soft-peach" size="md">
            <LocalIcon name="heart-o" size="22" color="var(--ab-peach-500)" />
          </ClayIcon>
          <div class="action-text">
            <span class="action-name">健康档案</span>
            <span class="action-desc">管理家庭成员健康</span>
          </div>
          <LocalIcon name="arrow" size="16" color="var(--ab-text-tertiary)" />
        </div>
      </div>

      <div style="height: 100px;"></div>
    </div>

    <AppTabbar :active="0" @change="handleTabChange" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import AppTabbar from '@/components/AppTabbar.vue'
import ClayIcon from '@/components/ClayIcon.vue'
import AlertBar from '@/components/AlertBar.vue'
import NutriBadge from '@/components/NutriBadge.vue'
import VegCard from '@/components/VegCard.vue'

const store = useAppStore()
const router = useRouter()

onMounted(() => {
  store.loadAllData()
})

const handleTabChange = (index, item) => {
  if (item.path) router.push(item.path)
}

const getType = (key) => {
  const map = { vitaminC: 'vitamin', fiber: 'fiber', protein: 'protein', iron: 'iron', calcium: 'calcium' }
  return map[key] || 'other'
}

const getLabel = (key) => {
  const map = { vitaminC: '维C', fiber: '膳食纤维', protein: '蛋白质', iron: '铁元素', calcium: '钙元素' }
  return map[key] || key
}
</script>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  background: transparent;
  display: flex;
  flex-direction: column;
}

/* 顶部毛玻璃导航 */
.top-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px 12px;
  background: rgba(244, 248, 242, 0.4);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--ab-border-subtle);
}

.greeting {
  display: flex;
  align-items: center;
  gap: 8px;
}
.greeting-emoji {
  font-size: 22px;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08));
}
.greeting-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--ab-text-primary);
  letter-spacing: -0.01em;
}

.notif-btn {
  position: relative;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: #ffffff;
  border-radius: 14px;
  box-shadow: var(--ab-shadow-float-sm);
  cursor: pointer;
  color: var(--ab-text-primary);
  transition: transform var(--ab-transition-normal), box-shadow var(--ab-transition-normal);
  &:active { transform: scale(0.94); box-shadow: var(--ab-shadow-press); }
}
.notif-dot {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: var(--ab-peach-500);
  border-radius: 50%;
  box-shadow: 0 0 0 2px #fff;
}

.page-body {
  flex: 1;
  padding: 0 20px;
}

/* Hero 区域 — Mintlify 品牌色 + 负字距大标题 */
.hero-section {
  position: relative;
  margin: 16px 0 24px;
  padding: 32px 24px 80px;
  background: linear-gradient(135deg, #18E299 0%, #14b87c 60%, #0a7d52 100%);
  border-radius: 32px;
  overflow: hidden;
  box-shadow:
    0 16px 40px rgba(24, 226, 153, 0.25),
    inset 0 2px 0 rgba(255, 255, 255, 0.25);
}

.hero-bg-deco {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}
.deco-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(2px);
  opacity: 0.5;
  animation: clayFloat 6s ease-in-out infinite;
  &--1 {
    top: -30px; right: -20px;
    width: 140px; height: 140px;
    background: rgba(255, 255, 255, 0.2);
  }
  &--2 {
    bottom: -40px; left: -30px;
    width: 160px; height: 160px;
    background: rgba(255, 255, 255, 0.15);
    animation-delay: -2s;
  }
  &--3 {
    top: 40%; right: 30%;
    width: 80px; height: 80px;
    background: rgba(255, 217, 153, 0.3);
    animation-delay: -4s;
  }
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.04em;
  margin-bottom: 16px;
  backdrop-filter: blur(8px);
}

.hero-title {
  font-size: 44px;
  font-weight: 700;
  color: #fff;
  line-height: 1.05;
  letter-spacing: -0.04em;
  margin-bottom: 12px;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}
.hero-line {
  display: block;
}
.hero-highlight {
  display: inline-block;
  background: #fff;
  color: #0a7d52;
  padding: 0 12px;
  border-radius: 16px;
  margin-right: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: rotate(-2deg);
}
.hero-suffix {
  color: #fff;
}
.hero-desc {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.92);
  font-weight: 500;
  letter-spacing: -0.01em;
}

.hero-cta {
  position: absolute;
  right: 24px;
  bottom: 24px;
  z-index: 1;
}
.hero-cta .clay-btn {
  background: #ffffff;
  color: #0a7d52;
  font-weight: 600;
  box-shadow:
    0 8px 20px rgba(0, 0, 0, 0.12),
    inset 0 -2px 0 rgba(0, 0, 0, 0.06);
  &:active { transform: translateY(1px) scale(0.98); }
}

/* 家庭栏 */
.family-bar {
  margin-top: -56px;       /* 让卡片"侵入" Hero 区 */
  position: relative;
  z-index: 2;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.family-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}
.family-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.family-eyebrow {
  font-size: 10px;
  font-weight: 700;
  color: var(--ab-brand-600);
  letter-spacing: 0.1em;
}
.family-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--ab-text-primary);
  letter-spacing: -0.02em;
}
.family-members {
  font-size: 12px;
  color: var(--ab-text-tertiary);
}
.family-more {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 6px 12px;
  background: var(--ab-brand-500);
  color: #fff;
  border: none;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: var(--ab-shadow-float-sm);
  transition: transform var(--ab-transition-fast);
  &:active { transform: scale(0.94); }
}

.family-avatars {
  display: flex;
  align-items: center;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 4px;
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
  border-radius: 50%;
  background: linear-gradient(135deg, var(--ab-brand-300), var(--ab-brand-500));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--ab-shadow-float-sm);
  color: #fff;
}
.avatar-name {
  font-size: 11px;
  color: var(--ab-text-secondary);
  font-weight: 500;
}

.add-avatar-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px dashed var(--ab-brand-300);
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  cursor: pointer;
  transition: all var(--ab-transition-fast);
  &:active { background: var(--ab-brand-50); }
}

/* 6 格快捷网格 */
.quick-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 24px;
}
.quick-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 4px;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: var(--ab-shadow-float-sm);
  cursor: pointer;
  border: 1px solid var(--ab-border-subtle);
  transition: transform var(--ab-transition-normal), box-shadow var(--ab-transition-normal);
  &:active {
    transform: scale(0.95);
    box-shadow: var(--ab-shadow-press);
  }
}
.emoji-icon {
  display: inline-block;
  font-size: 30px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.08));
  line-height: 1;
}
.quick-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--ab-text-primary);
  letter-spacing: -0.01em;
}

/* 警告区 */
.alerts-area {
  margin-top: 20px;
}

/* 区域标题 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-top: 28px;
  margin-bottom: 12px;
}
.section-eyebrow {
  display: block;
  font-size: 10px;
  font-weight: 700;
  color: var(--ab-brand-600);
  letter-spacing: 0.12em;
  margin-bottom: 4px;
}
.section-label {
  font-size: 20px;
  font-weight: 700;
  color: var(--ab-text-primary);
  letter-spacing: -0.02em;
  line-height: 1.1;
}
.section-extra {
  font-size: 13px;
  color: var(--ab-brand-600);
  cursor: pointer;
  font-weight: 600;
  padding: 4px 10px;
  background: var(--ab-brand-50);
  border-radius: 9999px;
}
.section-count {
  font-size: 13px;
  color: var(--ab-text-tertiary);
  font-weight: 500;
}

/* 营养仪表盘 */
.nutrition-dashboard {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

/* 菜篮子预览 */
.basket-preview {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.more-hint {
  text-align: center;
  padding: 14px;
  font-size: 13px;
  color: var(--ab-brand-600);
  font-weight: 600;
  cursor: pointer;
  background: var(--ab-brand-50);
  border-radius: 16px;
  box-shadow: var(--ab-shadow-float-sm);
  &:active { transform: scale(0.98); }
}

/* 快捷操作 */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.action-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  background: #ffffff;
  border-radius: 18px;
  box-shadow: var(--ab-shadow-float-sm);
  border: 1px solid var(--ab-border-subtle);
  cursor: pointer;
  transition: transform var(--ab-transition-normal);
  &:active { transform: scale(0.98); }
}
.action-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 0;
}
.action-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--ab-text-primary);
  letter-spacing: -0.01em;
}
.action-desc {
  font-size: 12px;
  color: var(--ab-text-tertiary);
}
</style>
