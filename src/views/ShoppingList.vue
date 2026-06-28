<template>
  <div class="shopping-list-page">
    <van-nav-bar title="采购清单" left-arrow @click-left="goBack" />

    <div class="list-header">
      <span class="list-title">家庭采购清单</span>
      <span class="item-count">{{ listItems.length }} 项</span>
    </div>

    <div class="shopping-list">
      <div class="list-container">
        <div 
          v-for="item in listItems" 
          :key="item.id" 
          class="list-item"
          :class="{ checked: item.checked }"
        >
          <div 
            class="check-btn" 
            :class="{ checked: item.checked }"
            @click="onItemCheck(item.id, !item.checked)"
          >
            <van-icon v-if="item.checked" name="checked" size="20" color="#fff" />
          </div>
          <div class="item-info">
            <span class="item-name">{{ item.name }}</span>
            <span class="item-desc">{{ item.quantity }}{{ item.unit }}</span>
          </div>
          <div class="item-actions">
            <van-stepper 
              v-model="item.quantity" 
              :min="1"
              @change="(val) => updateQuantity(item.id, val)"
              size="small"
            />
            <van-button 
              type="danger" 
              size="small" 
              icon="delete-o"
              @click="deleteItem(item.id)"
            />
          </div>
        </div>
      </div>
      
      <div class="empty-state" v-if="listItems.length === 0">
        <van-icon name="shopping-cart-o" size="48" color="#ccc" />
        <p>暂无采购清单</p>
      </div>
    </div>

    <div class="add-section">
      <van-field 
        v-model="newItemName" 
        placeholder="添加新物品"
        right-icon="plus"
        @click-right-icon="addItem"
      />
    </div>

    <div class="bottom-bar">
      <div class="progress-info">
        <div class="progress-text">
          <span>已完成</span>
          <span class="progress-count">{{ completedCount }}/{{ listItems.length }}</span>
        </div>
        <van-progress 
          :percentage="progressPercent" 
          :show-info="false" 
          :color="progressColor"
        />
      </div>
      
      <div class="action-buttons">
        <van-button type="default" @click="clearChecked">清除已选</van-button>
        <van-button type="primary" @click="shareList">分享清单</van-button>
      </div>
    </div>

    <van-loading 
      v-if="initialLoading" 
      class="loading-mask"
      text="加载中..."
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';
import { getShoppingList, addShoppingItem, updateShoppingItem, deleteShoppingItem } from '../api';

const router = useRouter();

const initialLoading = ref(true);
const listItems = ref([]);
const newItemName = ref('');
const family_id = ref(null);

const completedCount = computed(() => {
  return listItems.value.filter(item => item.checked).length;
});

const progressPercent = computed(() => {
  if (listItems.value.length === 0) return 0;
  return Math.round((completedCount.value / listItems.value.length) * 100);
});

const progressColor = computed(() => {
  const percent = progressPercent.value;
  if (percent === 100) return '#22c55e';
  if (percent >= 50) return '#f97316';
  return '#3b82f6';
});

const goBack = () => {
  router.back();
};

const getFamilyId = () => {
  const storedId = localStorage.getItem('family_id');
  if (storedId) {
    family_id.value = parseInt(storedId);
    return true;
  }
  return false;
};

const fetchShoppingListData = async () => {
  if (!family_id.value) {
    initialLoading.value = false;
    showToast({
      type: 'warning',
      message: '请先加入或创建家庭'
    });
    return;
  }

  try {
    initialLoading.value = true;
    const response = await getShoppingList(family_id.value);
    listItems.value = response.items || [];
  } catch (error) {
    console.error('获取采购清单失败:', error);
    showToast({
      type: 'fail',
      message: '获取采购清单失败'
    });
    listItems.value = [];
  } finally {
    initialLoading.value = false;
  }
};

const onItemCheck = async (id, checked) => {
  const item = listItems.value.find(i => i.id === id);
  if (!item) return;
  
  item.checked = checked;
  
  try {
    await updateShoppingItem(id, { checked });
    showToast({
      type: 'success',
      message: checked ? '已标记为已购' : '已标记为待购'
    });
  } catch (error) {
    console.error('更新勾选状态失败:', error);
    item.checked = !checked;
    showToast({
      type: 'fail',
      message: '更新失败'
    });
  }
};

const updateQuantity = async (id, quantity) => {
  try {
    await updateShoppingItem(id, { quantity });
  } catch (error) {
    console.error('更新数量失败:', error);
    const item = listItems.value.find(i => i.id === id);
    if (item) item.quantity = quantity;
    showToast({
      type: 'fail',
      message: '更新失败'
    });
  }
};

const addItem = async () => {
  const name = newItemName.value.trim();
  if (!name) {
    showToast({
      type: 'fail',
      message: '请输入物品名称'
    });
    return;
  }

  if (!family_id.value) {
    showToast({
      type: 'warning',
      message: '请先加入或创建家庭'
    });
    return;
  }

  try {
    const response = await addShoppingItem({
      family_id: family_id.value,
      name,
      quantity: 1,
      unit: '个'
    });
    
    listItems.value.unshift({
      id: response.id,
      name: response.name,
      quantity: response.quantity,
      unit: response.unit,
      checked: response.checked,
      added_at: response.added_at
    });
    
    newItemName.value = '';
    
    showToast({
      type: 'success',
      message: '添加成功'
    });
  } catch (error) {
    console.error('添加采购项失败:', error);
    showToast({
      type: 'fail',
      message: '添加失败'
    });
  }
};

const deleteItem = async (id) => {
  try {
    await deleteShoppingItem(id);
    listItems.value = listItems.value.filter(item => item.id !== id);
    showToast({
      type: 'success',
      message: '删除成功'
    });
  } catch (error) {
    console.error('删除采购项失败:', error);
    showToast({
      type: 'fail',
      message: '删除失败'
    });
  }
};

const clearChecked = async () => {
  const checkedIds = listItems.value.filter(item => item.checked).map(item => item.id);
  if (checkedIds.length === 0) {
    showToast({
      type: 'warning',
      message: '没有已勾选的物品'
    });
    return;
  }

  try {
    for (const id of checkedIds) {
      await deleteShoppingItem(id);
    }
    
    listItems.value = listItems.value.filter(item => !item.checked);
    
    showToast({
      type: 'success',
      message: '已清除已选物品'
    });
  } catch (error) {
    console.error('删除采购项失败:', error);
    showToast({
      type: 'fail',
      message: '删除失败'
    });
  }
};

const shareList = () => {
  showToast({
    type: 'success',
    message: '分享链接已复制到剪贴板'
  });
};

onMounted(async () => {
  getFamilyId();
  await fetchShoppingListData();
});
</script>

<style lang="scss" scoped>
.shopping-list-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
}

.list-header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .list-title {
    font-size: 18px;
    font-weight: bold;
    color: #333;
  }
  
  .item-count {
    font-size: 14px;
    color: #999;
  }
}

.shopping-list {
  flex: 1;
  padding: 0 16px;
  
  .list-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .list-item {
    background: #fff;
    padding: 16px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.3s ease;
    
    &.checked {
      opacity: 0.6;
      
      .item-name {
        text-decoration: line-through;
        color: #999;
      }
      
      .item-desc {
        color: #ccc;
      }
    }
  }
  
  .check-btn {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid #d9d9d9;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.3s ease;
    cursor: pointer;
    
    &.checked {
      background: #22c55e;
      border-color: #22c55e;
    }
    
    &:active {
      transform: scale(0.95);
    }
  }
  
  .item-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
  }
  
  .item-name {
    font-size: 16px;
    font-weight: 500;
    color: #333;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .item-desc {
    font-size: 14px;
    color: #999;
  }
  
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    color: #999;
    
    p {
      margin-top: 12px;
      font-size: 14px;
    }
  }
}

.item-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.add-section {
  padding: 16px;
}

.bottom-bar {
  background: #fff;
  padding: 16px;
  border-top: 1px solid #eee;
  
  .progress-info {
    margin-bottom: 12px;
    
    .progress-text {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      
      span {
        font-size: 14px;
        color: #666;
      }
      
      .progress-count {
        font-weight: bold;
        color: #333;
      }
    }
    
    .van-progress {
      height: 8px;
      border-radius: 4px;
    }
  }
  
  .action-buttons {
    display: flex;
    gap: 12px;
    
    .van-button {
      flex: 1;
      height: 44px;
    }
  }
}

.loading-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}
</style>
