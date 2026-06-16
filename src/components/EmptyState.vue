<template>
  <div class="empty-state">
    <!-- 空状态图标 -->
    <div class="empty-icon">
      <van-icon :name="iconName" :size="iconSize" />
    </div>
    
    <!-- 空状态标题 -->
    <h3 class="empty-title">{{ title }}</h3>
    
    <!-- 空状态描述 -->
    <p class="empty-desc">{{ description }}</p>
    
    <!-- 操作按钮 -->
    <div class="empty-actions">
      <van-button 
        v-if="showAction" 
        type="primary" 
        round 
        @click="handleAction"
        :loading="loading"
      >
        {{ loading ? '加载中...' : actionText }}
      </van-button>
    </div>
  </div>
</template>

<script setup>
/**
 * 通用空数据状态组件
 * 用于展示各种空数据场景：暂无订单、暂无消息、暂无收藏等
 */

import { computed } from 'vue';

// 定义 props
const props = defineProps({
  /**
   * 空状态类型
   * 可选值：list（列表空）、order（订单空）、message（消息空）、favorite（收藏空）、custom（自定义）
   */
  type: {
    type: String,
    default: 'list'
  },
  
  /**
   * 自定义标题（当 type 为 custom 时使用）
   */
  title: {
    type: String,
    default: '暂无数据'
  },
  
  /**
   * 自定义描述（当 type 为 custom 时使用）
   */
  description: {
    type: String,
    default: '快去添加一些吧'
  },
  
  /**
   * 是否显示操作按钮
   */
  showAction: {
    type: Boolean,
    default: false
  },
  
  /**
   * 操作按钮文字
   */
  actionText: {
    type: String,
    default: '去添加'
  },
  
  /**
   * 按钮加载状态
   */
  loading: {
    type: Boolean,
    default: false
  },
  
  /**
   * 自定义图标名称（当 type 为 custom 时使用）
   */
  icon: {
    type: String,
    default: 'inbox'
  },
  
  /**
   * 图标大小
   */
  iconSize: {
    type: [Number, String],
    default: 64
  }
});

// 定义 emit
const emit = defineEmits(['action']);

/**
 * 根据类型获取图标名称
 */
const iconName = computed(() => {
  const iconMap = {
    list: 'inbox',
    order: 'shopping-cart-o',
    message: 'message-o',
    favorite: 'heart-o',
    search: 'search',
    custom: props.icon
  };
  return iconMap[props.type] || props.icon;
});

/**
 * 获取默认标题
 */
const defaultTitle = computed(() => {
  const titleMap = {
    list: '暂无数据',
    order: '暂无订单',
    message: '暂无消息',
    favorite: '暂无收藏',
    search: '没有找到相关结果',
    custom: props.title
  };
  return titleMap[props.type] || props.title;
});

/**
 * 获取默认描述
 */
const defaultDescription = computed(() => {
  const descMap = {
    list: '快去添加一些吧',
    order: '快去下单吧',
    message: '暂无新消息',
    favorite: '快去收藏喜欢的内容吧',
    search: '换个关键词试试',
    custom: props.description
  };
  return descMap[props.type] || props.description;
});

/**
 * 处理操作按钮点击
 */
const handleAction = () => {
  emit('action');
};
</script>

<style lang="scss" scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  color: #ccc;
}

.empty-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0 0 8px 0;
}

.empty-desc {
  font-size: 14px;
  color: #999;
  margin: 0 0 24px 0;
}

.empty-actions {
  .van-button {
    min-width: 120px;
    height: 44px;
  }
}
</style>