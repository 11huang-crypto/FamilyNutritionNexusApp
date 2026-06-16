<template>
  <!--
    ShoppingListView.vue - 采购清单页
    带实时协同功能标记（WebSocket待对接）
  -->
  <div class="shopping-page">
    <AppNavbar title="采购清单" rightIcon="add-o" @right-click="showAddDialog = true" />

    <div class="page-body">
      <!-- 协同状态提示 -->
      <div v-if="collabUsers.length > 0" class="collab-bar">
        <div class="collab-avatars">
          <FamilyAvatar
            v-for="(u, i) in collabUsers"
            :key="u.id"
            :member="u"
            size="xs"
            :showName="false"
            :stacked="i > 0"
            :index="i"
            :status="u.status"
          />
        </div>
        <span class="collab-text">{{ collabUsers.length }} 人在线编辑</span>
      </div>

      <!-- 进度条 -->
      <div class="progress-bar-wrap card-base">
        <div class="flex-between" style="margin-bottom: 8px;">
          <span class="progress-label">采购进度</span>
          <span class="progress-value">{{ completedCount }}/{{ store.shoppingList.length }}</span>
        </div>
        <van-progress
          :percentage="completionPercent"
          stroke-width="8"
          :stroke-color="{ from: '#22c55e', to: '#16a34a' }"
        />
      </div>

      <!-- 清单列表 -->
      <div class="section-header flex-between">
        <h3 class="section-label">待购清单</h3>
        <span class="section-count">{{ store.pendingShoppingCount }} 项</span>
      </div>

      <div v-if="store.shoppingList.length === 0" class="empty-state">
        <van-empty description="清单为空" />
      </div>

      <TransitionGroup name="check" tag="div" class="shopping-items">
        <div
          v-for="item in store.shoppingList"
          :key="item.id"
          class="shopping-item card-base"
          :class="{ 'is-checked': item.checked }"
          @click="store.toggleShoppingItem(item.id)"
        >
          <div class="item-left">
            <div class="checkbox-wrap" :class="{ checked: item.checked }">
              <van-icon v-if="item.checked" name="success" size="14" color="#fff" />
            </div>
            <div class="item-info">
              <span class="item-name" :class="{ 'text-line': item.checked }">{{ item.name }}</span>
              <span class="item-meta">
                {{ item.quantity }}{{ item.unit }}
                <span class="item-category">· {{ item.category }}</span>
              </span>
            </div>
          </div>
          <FamilyAvatar
            v-if="member(item.assignedTo)"
            :member="member(item.assignedTo)"
            size="xs"
            :showName="true"
          />
        </div>
      </TransitionGroup>

      <!-- 已完成 -->
      <div v-if="completedCount > 0" class="completed-section">
        <h3 class="section-label completed-label">已完成 {{ completedCount }} 项</h3>
        <div
          v-for="item in completedItems"
          :key="item.id"
          class="shopping-item card-base is-checked"
        >
          <div class="item-left">
            <div class="checkbox-wrap checked">
              <van-icon name="success" size="14" color="#fff" />
            </div>
            <div class="item-info">
              <span class="item-name text-line">{{ item.name }}</span>
              <span class="item-meta">{{ item.quantity }}{{ item.unit }} · {{ item.category }}</span>
            </div>
          </div>
        </div>
      </div>

      <div style="height: 20px;"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import AppNavbar from '@/components/AppNavbar.vue'
import FamilyAvatar from '@/components/FamilyAvatar.vue'
import { useAppStore } from '@/stores'

const store = useAppStore()
const showAddDialog = ref(false)

const completedCount = computed(() => store.shoppingList.filter(i => i.checked).length)
const completedItems = computed(() => store.shoppingList.filter(i => i.checked))
const completionPercent = computed(() =>
  store.shoppingList.length > 0
    ? Math.round((completedCount.value / store.shoppingList.length) * 100)
    : 0
)

const member = (id) => store.family.members.find(m => m.id === id)

// WebSocket 协同模拟
const collabUsers = ref([
  { id: 'u2', name: '妈妈', avatar: '', color: '#ec4899', status: 'online' },
])
</script>

<style scoped lang="scss">
.shopping-page {
  min-height: 100vh;
  background: var(--ab-bg-page);
}

.page-body {
  padding: var(--ab-space-4);
  padding-bottom: 80px;
}

.collab-bar {
  display: flex;
  align-items: center;
  gap: var(--ab-space-2);
  padding: var(--ab-space-2) var(--ab-space-3);
  background: var(--ab-info-light);
  border-radius: var(--ab-radius-md);
  margin-bottom: var(--ab-space-3);
}

.collab-avatars {
  display: flex;
  align-items: center;
}

.collab-text {
  font-size: var(--ab-text-xs);
  color: var(--ab-info);
  font-weight: var(--ab-font-medium);
}

.progress-bar-wrap {
  margin-bottom: var(--ab-space-4);
}

.progress-label {
  font-size: var(--ab-text-sm);
  color: var(--ab-text-secondary);
}

.progress-value {
  font-size: var(--ab-text-sm);
  font-weight: var(--ab-font-bold);
  color: var(--ab-primary-600);
}

.section-header {
  margin-bottom: var(--ab-space-3);
}

.section-label {
  font-size: var(--ab-text-base);
  font-weight: var(--ab-font-bold);
  color: var(--ab-text-primary);
}

.section-count {
  font-size: var(--ab-text-sm);
  color: var(--ab-text-tertiary);
}

.shopping-items {
  display: flex;
  flex-direction: column;
  gap: var(--ab-space-2);
}

.shopping-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--ab-space-3);
  cursor: pointer;
  transition: all var(--ab-transition-fast);

  &.is-checked {
    opacity: 0.5;
    background: var(--ab-gray-50);
  }

  &:active {
    transform: scale(0.98);
  }
}

.item-left {
  display: flex;
  align-items: center;
  gap: var(--ab-space-3);
  flex: 1;
  min-width: 0;
}

.checkbox-wrap {
  width: 22px;
  height: 22px;
  border: 2px solid var(--ab-gray-300);
  border-radius: var(--ab-radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all var(--ab-transition-fast);

  &.checked {
    background: var(--ab-primary-500);
    border-color: var(--ab-primary-500);
  }
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.item-name {
  font-size: var(--ab-text-base);
  font-weight: var(--ab-font-medium);
  color: var(--ab-text-primary);

  &.text-line {
    text-decoration: line-through;
    color: var(--ab-text-tertiary);
  }
}

.item-meta {
  font-size: var(--ab-text-xs);
  color: var(--ab-text-tertiary);
}

.item-category {
  color: var(--ab-text-tertiary);
}

.completed-section {
  margin-top: var(--ab-space-4);
}

.completed-label {
  color: var(--ab-text-tertiary);
  margin-bottom: var(--ab-space-3);
}

.empty-state {
  padding-top: var(--ab-space-8);
}

/* 勾选动画 */
.check-enter-active,
.check-leave-active {
  transition: all 0.3s ease;
}

.check-enter-from,
.check-leave-to {
  opacity: 0;
  transform: scale(0.96);
}
</style>
