<template>
  <!--
    DemoView.vue - 组件库展示页
    展示所有公共组件的变体和用法，供团队检查和统一视觉风格
  -->
  <div class="demo-page">
    <!-- 顶部导航 -->
    <AppNavbar
      title="组件库展示"
      :showBack="true"
      rightText="规范"
      @right-click="showSpec = true"
    />

    <div class="demo-content">
      <!-- 页面说明 -->
      <div class="demo-intro">
        <h2 class="section-title">AI智能菜篮子 — 公共组件库 v1.0</h2>
        <p class="section-desc">Color: 健康绿 #22c55e | Font: Noto Sans SC | Radius: 8-12px | Spacing: 4px基准</p>
      </div>

      <!-- ========== 1. 导航栏 Navbar ========== -->
      <section class="demo-section">
        <h3 class="demo-heading">
          <LocalIcon name="wap-nav" size="18" color="#22c55e" />
          <span>01. AppNavbar — 顶部导航栏</span>
        </h3>

        <!-- 默认样式 -->
        <div class="demo-block bg-gray">
          <p class="demo-label">默认：标题 + 返回 + 右侧图标</p>
          <AppNavbar title="我的菜篮子" :showBack="true" rightIcon="search" />
        </div>

        <!-- 透明样式 -->
        <div class="demo-block bg-gradient">
          <p class="demo-label">透明背景模式（用于头部有大图时）</p>
          <AppNavbar title="食材详情" :showBack="true" :transparent="true" rightText="编辑" />
        </div>

        <!-- 带进度条 -->
        <div class="demo-block bg-gray">
          <p class="demo-label">带进度条（上传/分析场景）</p>
          <AppNavbar title="分析中..." :showBack="true" :loading="true" :progress="65" />
        </div>
      </section>

      <!-- ========== 2. 底部Tab栏 Tabbar ========== -->
      <section class="demo-section">
        <h3 class="demo-heading">
          <LocalIcon name="bars" size="18" color="#22c55e" />
          <span>02. AppTabbar — 底部Tab栏</span>
        </h3>

        <div class="demo-block tabbar-demo">
          <p class="demo-label">5个Tab：首页/菜篮子/识材/食谱/清单</p>
          <AppTabbar
            :active="activeTab"
            :items="demoTabItems"
            @update:active="activeTab = $event"
          />
        </div>
      </section>

      <!-- ========== 3. 果蔬卡片 VegCard ========== -->
      <section class="demo-section">
        <h3 class="demo-heading">
          <LocalIcon name="coupon-o" size="18" color="#22c55e" />
          <span>03. VegCard — 果蔬卡片</span>
        </h3>

        <!-- 列表变体 -->
        <p class="demo-label-sub">列表模式 (variant="list") — 首页/菜篮子默认样式</p>
        <div class="card-demo-grid">
          <VegCard
            v-for="item in sampleItems.slice(0, 3)"
            :key="item.id"
            :item="item"
            variant="list"
            :showFreshness="true"
            :showNutrients="true"
          />
        </div>

        <!-- 网格变体 -->
        <p class="demo-label-sub">网格模式 (variant="grid") — 食材浏览/推荐瀑布流</p>
        <div class="card-demo-grid grid-2col">
          <VegCard
            v-for="item in sampleItems.slice(0, 2)"
            :key="'g-'+item.id"
            :item="item"
            variant="grid"
            :showFreshness="true"
            :showNutrients="true"
          />
        </div>

        <!-- 详情变体 -->
        <p class="demo-label-sub">详情 / 可删除模式</p>
        <VegCard
          :item="sampleItems[0]"
          variant="detail"
          :deletable="true"
          @delete="() => {}"
        />
      </section>

      <!-- ========== 4. 营养标签 NutriBadge ========== -->
      <section class="demo-section">
        <h3 class="demo-heading">
          <LocalIcon name="label-o" size="18" color="#22c55e" />
          <span>04. NutriBadge — 营养标签徽章</span>
        </h3>

        <!-- 小号 -->
        <p class="demo-label-sub">尺寸：sm / md / lg</p>
        <div class="badge-row">
          <NutriBadge type="vitamin" label="维C" :value="23" unit="mg" size="sm" />
          <NutriBadge type="fiber" label="纤维" :value="2.4" unit="g" size="sm" />
          <NutriBadge type="protein" label="蛋白" :value="8.0" unit="g" size="sm" />
          <NutriBadge type="mineral" label="铁" :value="2.7" unit="mg" size="sm" />
          <NutriBadge type="other" label="钾" :value="358" unit="mg" size="sm" />
        </div>

        <!-- 中等 -->
        <div class="badge-row" style="margin-top: 8px;">
          <NutriBadge type="vitamin" label="维生素C" :value="89" unit="mg" size="md" />
          <NutriBadge type="fiber" label="膳食纤维" :value="2.6" unit="g" size="md" />
          <NutriBadge type="protein" label="蛋白质" :value="20" unit="g" size="md" />
          <NutriBadge type="mineral" label="钙" :value="350" unit="mg" size="md" />
        </div>

        <!-- 大号 + 进度条 -->
        <p class="demo-label-sub">带进度条模式 (percent) — 营养摄入仪表</p>
        <div class="card-demo-grid grid-3col">
          <NutriBadge type="vitamin" label="维生素C" :value="65" unit="mg" :percent="65" size="lg" />
          <NutriBadge type="fiber" label="膳食纤维" :value="18" unit="g" :percent="72" size="lg" />
          <NutriBadge type="protein" label="蛋白质" :value="45" unit="g" :percent="75" size="lg" />
        </div>
      </section>

      <!-- ========== 5. 警告提示条 AlertBar ========== -->
      <section class="demo-section">
        <h3 class="demo-heading">
          <LocalIcon name="warning-o" size="18" color="#22c55e" />
          <span>05. AlertBar — 警告提示条</span>
        </h3>

        <div class="alert-demo-stack">
          <AlertBar type="warning"  message="警告：菠菜 + 黄瓜同食可能影响维生素C吸收" action="查看详情" />
          <AlertBar type="warning" message="警告：菠菜新鲜度降至75%，建议尽快食用" />
          <AlertBar type="info"    message="提示：本周维生素C摄入偏低，建议增加柑橘类水果" />
          <AlertBar type="success" message="成功：菜篮子健康状况良好！" />
          <AlertBar type="warning" message="紧凑模式示例" :compact="true" :closable="true" />
        </div>
      </section>

      <!-- ========== 6. 家庭成员头像 FamilyAvatar ========== -->
      <section class="demo-section">
        <h3 class="demo-heading">
          <LocalIcon name="friends-o" size="18" color="#22c55e" />
          <span>06. FamilyAvatar — 家庭成员头像</span>
        </h3>

        <!-- 单尺寸展示 -->
        <p class="demo-label-sub">尺寸：xs / sm / md / lg / xl</p>
        <div class="avatar-row">
          <FamilyAvatar :member="familyMembers[0]" size="xs" :showName="false" />
          <FamilyAvatar :member="familyMembers[0]" size="sm" :showName="true" />
          <FamilyAvatar v-for="m in familyMembers" :key="m.id" :member="m" size="md" :showName="true" />
        </div>

        <!-- 堆叠展示 -->
        <p class="demo-label-sub">堆叠模式 (stacked) — 协作成员展示</p>
        <div class="avatar-row" style="margin-top: 12px;">
          <FamilyAvatar
            v-for="(m, i) in familyMembers"
            :key="'s-'+m.id"
            :member="m"
            size="lg"
            :stacked="true"
            :index="i"
            :showName="false"
          />
        </div>

        <!-- 可选择模式 -->
        <p class="demo-label-sub">可选择模式 (selectable + selected)</p>
        <div class="avatar-row" style="margin-top: 12px;">
          <FamilyAvatar
            v-for="m in familyMembers"
            :key="'sel-'+m.id"
            :member="m"
            size="md"
            :selectable="true"
            :selected="m.id === selectedMember"
            :showName="true"
            @select="selectedMember = selectedMember === m.id ? null : m.id"
          />
        </div>
      </section>

      <!-- ========== 设计规范速查 ========== -->
      <section v-if="showSpec" class="demo-section spec-section">
        <h3 class="demo-heading">
          <LocalIcon name="brush-o" size="18" color="#22c55e" />
          <span>设计规范速查 Design Token</span>
        </h3>

        <div class="spec-color-grid">
          <div v-for="c in specColors" :key="c.label" class="spec-color-item">
            <div class="spec-swatch" :style="{ background: c.value }"></div>
            <div class="spec-info">
              <span class="spec-name">{{ c.label }}</span>
              <span class="spec-value">{{ c.value }}</span>
            </div>
          </div>
        </div>

        <div class="spec-section">
          <h4>字体层级</h4>
          <div v-for="t in specText" :key="t.label" class="spec-text-item">
            <span :style="{ fontSize: t.size, fontWeight: t.weight, color: t.color }">{{ t.label }}</span>
            <span class="spec-meta">{{ t.size }} / {{ t.weight === '700' ? 'Bold' : t.weight === '500' ? 'Medium' : 'Regular' }}</span>
          </div>
        </div>
      </section>

      <div style="height: 100px;"></div>
    </div>
  </div>
</template>

<script setup>
/**
 * DemoView - 组件库展示页
 * 展示所有公共组件及其变体，供团队统一审查视觉风格
 */
import { ref } from 'vue'
import AppNavbar from '@/components/AppNavbar.vue'
import AppTabbar from '@/components/AppTabbar.vue'
import VegCard from '@/components/VegCard.vue'
import NutriBadge from '@/components/NutriBadge.vue'
import AlertBar from '@/components/AlertBar.vue'
import FamilyAvatar from '@/components/FamilyAvatar.vue'

const showSpec = ref(false)
const activeTab = ref(0)
const selectedMember = ref(null)

const demoTabItems = [
  { name: 'home', label: '首页', icon: 'wap-home-o', iconActive: 'wap-home', path: '/' },
  { name: 'basket', label: '菜篮子', icon: 'shopping-cart-o', iconActive: 'shopping-cart', path: '/basket' },
  { name: 'analyze', label: '识材', icon: 'photo-o', iconActive: 'photo', path: '/analyze' },
  { name: 'meal', label: '食谱', icon: 'calendar-o', iconActive: 'records', path: '/meal-plan' },
  { name: 'shopping', label: '清单', icon: 'todo-list-o', iconActive: 'completed', path: '/shopping-list' },
]

const sampleItems = [
  { id: 1, name: '西红柿', category: '蔬菜', quantity: 3, unit: '个', freshness: 95, image: new URL('@/assets/images/vegetable/tomatoes.jpg', import.meta.url).href, nutrients: { vitaminC: 23, fiber: 1.2 }, addedBy: 'u1', addedAt: '2026-06-06' },
  { id: 2, name: '胡萝卜', category: '蔬菜', quantity: 2, unit: '根', freshness: 88, image: new URL('@/assets/images/vegetable/carrots.jpg', import.meta.url).href, nutrients: { vitaminA: 835, fiber: 2.8 }, addedBy: 'u2', addedAt: '2026-06-05' },
  { id: 3, name: '苹果', category: '水果', quantity: 5, unit: '个', freshness: 92, image: new URL('@/assets/images/fruit/apple.jpg', import.meta.url).href, nutrients: { vitaminC: 5, fiber: 2.4 }, addedBy: 'u3', addedAt: '2026-06-06' },
  { id: 4, name: '香蕉', category: '水果', quantity: 4, unit: '根', freshness: 70, image: new URL('@/assets/images/fruit/banana.jpg', import.meta.url).href, nutrients: { potassium: 358, vitaminC: 8.7 }, addedBy: 'u2', addedAt: '2026-06-03' },
]

const familyMembers = [
  { id: 'u1', name: '爸爸', avatar: '', role: 'admin', color: '#3b82f6' },
  { id: 'u2', name: '妈妈', avatar: '', role: 'member', color: '#ec4899' },
  { id: 'u3', name: '宝宝', avatar: '', role: 'member', color: '#f59e0b' },
]

const specColors = [
  { label: 'Primary 500', value: '#22c55e' },
  { label: 'Primary 600', value: '#16a34a' },
  { label: 'Secondary 500', value: '#f97316' },
  { label: 'Success', value: '#22c55e' },
  { label: 'Warning', value: '#f59e0b' },
  { label: 'Danger', value: '#ef4444' },
  { label: 'Info', value: '#3b82f6' },
  { label: '灰色 400', value: '#a3a3a3' },
]

const specText = [
  { label: '页面大标题 3xl', size: '24px', weight: '700', color: '#1a1a1a' },
  { label: '卡片标题 xl', size: '18px', weight: '700', color: '#1a1a1a' },
  { label: '列表标题 lg', size: '16px', weight: '500', color: '#1a1a1a' },
  { label: '正文 base', size: '14px', weight: '400', color: '#1a1a1a' },
  { label: '辅助文字 sm', size: '12px', weight: '400', color: '#666666' },
  { label: '标签文字 xs', size: '10px', weight: '500', color: '#999999' },
]
</script>

<style scoped lang="scss">
.demo-page {
  min-height: 100vh;
  background: transparent;
}

.demo-content {
  padding: var(--ab-space-4);
  padding-bottom: 120px;
}

.demo-intro {
  padding: var(--ab-space-4);
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  border-radius: var(--ab-radius-lg);
  margin-bottom: var(--ab-space-6);
}

.section-title {
  font-size: var(--ab-text-xl);
  font-weight: var(--ab-font-bold);
  color: var(--ab-brand-800);
  margin-bottom: var(--ab-space-1);
}

.section-desc {
  font-size: var(--ab-text-sm);
  color: var(--ab-brand-700);
  opacity: 0.8;
}

.demo-section {
  margin-bottom: var(--ab-space-8);
}

.demo-heading {
  display: flex;
  align-items: center;
  gap: var(--ab-space-2);
  font-size: var(--ab-text-lg);
  font-weight: var(--ab-font-bold);
  color: var(--ab-text-primary);
  margin-bottom: var(--ab-space-4);
  padding-bottom: var(--ab-space-2);
  border-bottom: 2px solid var(--ab-brand-100);
}

.demo-block {
  position: relative;
  border-radius: var(--ab-radius-lg);
  margin-bottom: var(--ab-space-3);
  overflow: hidden;

  &.bg-gray {
    background: var(--ab-gray-50);
  }

  &.bg-gradient {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    min-height: 60px;
  }
}

.demo-label {
  padding: var(--ab-space-2) var(--ab-space-3);
  font-size: var(--ab-text-xs);
  color: var(--ab-text-tertiary);
  font-weight: var(--ab-font-medium);
  text-transform: uppercase;
}

.demo-label-sub {
  padding: var(--ab-space-2) var(--ab-space-3);
  font-size: var(--ab-text-xs);
  color: var(--ab-text-secondary);
  font-weight: var(--ab-font-medium);
  margin-top: var(--ab-space-2);
  margin-bottom: var(--ab-space-2);
}

.tabbar-demo {
  background: var(--ab-bg-card);
  height: 70px;
  padding-top: 4px;
  border-radius: var(--ab-radius-lg);
  box-shadow: var(--ab-shadow-lg);
}

.card-demo-grid {
  padding: 0 var(--ab-space-3);
  display: flex;
  flex-direction: column;
  gap: var(--ab-space-3);
}

.grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.grid-3col {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--ab-space-2);
  padding: 0 var(--ab-space-3);
}

.alert-demo-stack {
  display: flex;
  flex-direction: column;
  gap: var(--ab-space-2);
  padding: 0 var(--ab-space-3);
}

.avatar-row {
  display: flex;
  align-items: flex-start;
  gap: var(--ab-space-3);
  padding: 0 var(--ab-space-3);
}

/* 设计规范速查 */
.spec-section {
  background: var(--ab-bg-card);
  border-radius: var(--ab-radius-lg);
  padding: var(--ab-space-4);
  box-shadow: var(--ab-clay-shadow-sm);
}

.spec-color-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--ab-space-2);
}

.spec-color-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.spec-swatch {
  width: 100%;
  height: 40px;
  border-radius: var(--ab-radius-sm);
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}

.spec-info {
  display: flex;
  flex-direction: column;
}

.spec-name {
  font-size: var(--ab-text-xs);
  color: var(--ab-text-secondary);
  font-weight: var(--ab-font-medium);
}

.spec-value {
  font-size: var(--ab-text-xs);
  color: var(--ab-text-tertiary);
  font-family: var(--ab-font-mono);
}

.spec-text-item {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding: var(--ab-space-2) 0;
  border-bottom: 1px solid var(--ab-border-light);
}

.spec-meta {
  font-size: var(--ab-text-xs);
  color: var(--ab-text-tertiary);
  font-family: var(--ab-font-mono);
}
</style>
