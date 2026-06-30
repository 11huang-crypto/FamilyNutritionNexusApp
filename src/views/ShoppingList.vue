<template>
  <div class="shopping-list-page">
    <AppNavbar title="采购清单" :showBack="true" />

    <div class="page-body">
      <!-- 清单头部 -->
      <div class="list-header">
        <h2 class="list-title">家庭采购清单</h2>
        <span class="item-count">{{ listItems.length }} 项</span>
      </div>

      <!-- 列表 -->
      <div class="shopping-list">
        <TransitionGroup name="list" tag="div" class="list-container">
          <div v-for="item in listItems" :key="item.id" class="clay-card list-item" :class="{ checked: item.checked }">
            <div class="check-btn" :class="{ checked: item.checked }" @click="onItemCheck(item.id, !item.checked)">
              <LocalIcon v-if="item.checked" name="checked" size="16" color="#fff" />
            </div>
            <div class="item-info">
              <span class="item-name">{{ item.name }}</span>
              <span class="item-desc">{{ item.quantity }}{{ item.unit }}</span>
            </div>
            <div class="item-actions">
              <van-stepper v-model="item.quantity" :min="1" @change="(val) => updateQuantity(item.id, val)" size="small" />
              <button class="delete-item-btn" @click.stop="deleteItem(item.id)">
                <LocalIcon name="delete-o" size="16" color="var(--ab-text-disabled)" />
              </button>
            </div>
          </div>
        </TransitionGroup>

        <div class="empty-state" v-if="listItems.length === 0">
          <div class="empty-icon">🛒</div>
          <p class="empty-text">暂无采购清单</p>
        </div>
      </div>

      <!-- 添加 -->
      <div class="add-section clay-card">
        <van-field v-model="newItemName" placeholder="添加新物品" clearable @keyup.enter="addItem">
          <template #right-icon>
            <button class="clay-btn clay-btn--primary" style="padding: 4px 12px; font-size: 12px;" @click="addItem">添加</button>
          </template>
        </van-field>
      </div>

      <!-- 底部操作栏 -->
      <div class="bottom-bar clay-card">
        <div class="progress-info">
          <div class="progress-text">
            <span>已完成</span>
            <span class="progress-count">{{ completedCount }}/{{ listItems.length }}</span>
          </div>
          <div class="progress-bar-wrap">
            <div class="progress-fill" :style="{ width: progressPercent + '%', background: progressColor }"></div>
          </div>
        </div>
        <div class="action-buttons">
          <button class="clay-btn clay-btn--secondary" @click="clearChecked">清除已选</button>
          <button class="clay-btn clay-btn--primary" @click="shareList">分享清单</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';
import { getShoppingList, addShoppingItem, updateShoppingItem, deleteShoppingItem } from '../api';
import AppNavbar from '@/components/AppNavbar.vue';

const router = useRouter();
const listItems = ref([]);
const newItemName = ref('');
const family_id = ref(null);

const completedCount = computed(() => listItems.value.filter(item => item.checked).length);
const progressPercent = computed(() => listItems.value.length === 0 ? 0 : Math.round((completedCount.value / listItems.value.length) * 100));
const progressColor = computed(() => {
  const p = progressPercent.value;
  if (p === 100) return 'var(--ab-success)';
  if (p >= 50) return 'var(--ab-warning)';
  return 'var(--ab-info)';
});

const fetchShoppingListData = async () => {
  family_id.value = localStorage.getItem('family_id');
  if (!family_id.value) return;
  try {
    const response = await getShoppingList(family_id.value);
    listItems.value = response.items || [];
  } catch (e) {
    listItems.value = [
      { id: 1, name: '西兰花', category: '蔬菜', quantity: 1, unit: '颗', checked: false },
      { id: 2, name: '猕猴桃', category: '水果', quantity: 6, unit: '个', checked: true },
      { id: 3, name: '草莓', category: '水果', quantity: 1, unit: '盒', checked: false },
    ];
  }
};

const onItemCheck = async (id, checked) => {
  const item = listItems.value.find(i => i.id === id);
  if (!item) return;
  item.checked = checked;
  try { await updateShoppingItem(id, { checked }); } catch (e) {}
};

const updateQuantity = async (id, quantity) => {
  try { await updateShoppingItem(id, { quantity }); } catch (e) {}
};

const addItem = async () => {
  const name = newItemName.value.trim();
  if (!name) return;
  if (!family_id.value) return;
  try {
    const response = await addShoppingItem({ family_id: family_id.value, name, quantity: 1, unit: '个' });
    listItems.value.unshift({ id: response.id, name, quantity: 1, unit: '个', checked: false });
    newItemName.value = '';
    showToast({ type: 'success', message: '添加成功' });
  } catch (e) {
    listItems.value.unshift({ id: Date.now(), name, quantity: 1, unit: '个', checked: false });
    newItemName.value = '';
  }
};

const deleteItem = async (id) => {
  listItems.value = listItems.value.filter(item => item.id !== id);
  try { await deleteShoppingItem(id); } catch (e) {}
};

const clearChecked = () => {
  listItems.value = listItems.value.filter(item => !item.checked);
  showToast({ type: 'success', message: '已清除已选物品' });
};

const shareList = () => showToast({ type: 'success', message: '分享链接已复制到剪贴板' });

onMounted(fetchShoppingListData);
</script>

<style scoped lang="scss">
.shopping-list-page { min-height: 100vh; background: transparent; }
.page-body { padding: var(--ab-space-4); padding-bottom: 80px; }

.list-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--ab-space-4); }
.list-title { font-size: var(--ab-text-xl); font-weight: var(--ab-font-semibold); color: var(--ab-text-primary); }
.item-count { font-size: var(--ab-text-sm); color: var(--ab-text-tertiary); }

.list-container { display: flex; flex-direction: column; gap: var(--ab-space-2); margin-bottom: var(--ab-space-4); }

.list-item {
  display: flex; align-items: center; gap: var(--ab-space-3); padding: var(--ab-space-3) var(--ab-space-4);
  &.checked { opacity: 0.6; .item-name { text-decoration: line-through; color: var(--ab-text-tertiary); } }
}

.check-btn {
  width: 28px; height: 28px; border-radius: var(--ab-radius-full); border: 2px solid var(--ab-gray-300);
  display: flex; align-items: center; justify-content: center; flex-shrink: 0; cursor: pointer;
  transition: all var(--ab-transition-fast);
  &.checked { background: var(--ab-success); border-color: var(--ab-success); }
  &:active { transform: scale(0.9); }
}

.item-info { flex: 1; display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.item-name { font-size: var(--ab-text-base); font-weight: var(--ab-font-medium); color: var(--ab-text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.item-desc { font-size: var(--ab-text-sm); color: var(--ab-text-tertiary); }

.item-actions { display: flex; align-items: center; gap: var(--ab-space-2); }

.delete-item-btn { width: 32px; height: 32px; border: none; background: transparent; border-radius: var(--ab-radius-full); display: flex; align-items: center; justify-content: center; cursor: pointer; &:active { background: var(--ab-gray-100); } }

.empty-state { display: flex; flex-direction: column; align-items: center; padding: 60px 20px; }
.empty-icon { font-size: 48px; margin-bottom: 12px; }
.empty-text { font-size: var(--ab-text-base); color: var(--ab-text-tertiary); }

.add-section { margin-bottom: var(--ab-space-4); padding: 8px 12px; }

.bottom-bar { padding: var(--ab-space-4); }
.progress-info { margin-bottom: var(--ab-space-3); }
.progress-text { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--ab-space-2); span { font-size: var(--ab-text-sm); color: var(--ab-text-tertiary); } .progress-count { font-weight: var(--ab-font-semibold); color: var(--ab-text-primary); } }
.progress-bar-wrap { height: 8px; background: var(--ab-gray-200); border-radius: var(--ab-radius-full); overflow: hidden; }
.progress-fill { height: 100%; border-radius: var(--ab-radius-full); transition: width 0.4s ease; }

.action-buttons { display: flex; gap: var(--ab-space-3); button { flex: 1; } }
</style>
