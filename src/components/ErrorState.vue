<template>
  <div class="error-state">
    <!-- 错误图标 -->
    <div class="error-icon" :class="iconClass">
      <van-icon :name="iconName" :size="iconSize" />
    </div>
    
    <!-- 错误标题 -->
    <h3 class="error-title">{{ title }}</h3>
    
    <!-- 错误描述 -->
    <p class="error-desc">{{ description }}</p>
    
    <!-- 操作按钮 -->
    <div class="error-actions">
      <van-button 
        v-if="showRetry" 
        type="primary" 
        round 
        @click="handleRetry"
        :loading="loading"
      >
        {{ loading ? '重试中...' : '重试' }}
      </van-button>
      
      <van-button 
        v-if="showBack" 
        type="default" 
        round 
        @click="handleBack"
      >
        返回
      </van-button>
    </div>
  </div>
</template>

<script setup>
/**
 * 通用错误状态组件
 * 用于展示各种错误状态：网络错误、服务器错误、权限错误等
 */

import { computed } from 'vue';
import { useRouter } from 'vue-router';

// 定义 props
const props = defineProps({
  /**
   * 错误类型
   * 可选值：network（网络错误）、server（服务器错误）、auth（权限错误）、custom（自定义）
   */
  type: {
    type: String,
    default: 'custom'
  },
  
  /**
   * 自定义标题（当 type 为 custom 时使用）
   */
  title: {
    type: String,
    default: '出错了'
  },
  
  /**
   * 自定义描述（当 type 为 custom 时使用）
   */
  description: {
    type: String,
    default: '请稍后重试'
  },
  
  /**
   * 是否显示重试按钮
   */
  showRetry: {
    type: Boolean,
    default: false
  },
  
  /**
   * 是否显示返回按钮
   */
  showBack: {
    type: Boolean,
    default: false
  },
  
  /**
   * 重试按钮加载状态
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
    default: 'warning-o'
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
const emit = defineEmits(['retry', 'back']);

// 路由实例
const router = useRouter();

/**
 * 根据错误类型获取图标名称
 */
const iconName = computed(() => {
  const iconMap = {
    network: 'wifi-o',
    server: 'server',
    auth: 'user-o',
    custom: props.icon
  };
  return iconMap[props.type] || props.icon;
});

/**
 * 根据错误类型获取图标样式类
 */
const iconClass = computed(() => {
  const classMap = {
    network: 'icon-network',
    server: 'icon-server',
    auth: 'icon-auth',
    custom: 'icon-custom'
  };
  return classMap[props.type] || 'icon-custom';
});

/**
 * 获取默认标题
 */
const defaultTitle = computed(() => {
  const titleMap = {
    network: '网络连接失败',
    server: '服务器出错',
    auth: '权限不足',
    custom: props.title
  };
  return titleMap[props.type] || props.title;
});

/**
 * 获取默认描述
 */
const defaultDescription = computed(() => {
  const descMap = {
    network: '请检查网络设置后重试',
    server: '服务器繁忙，请稍后再试',
    auth: '请登录后再进行操作',
    custom: props.description
  };
  return descMap[props.type] || props.description;
});

/**
 * 处理重试按钮点击
 */
const handleRetry = () => {
  emit('retry');
};

/**
 * 处理返回按钮点击
 */
const handleBack = () => {
  emit('back', router.back());
};
</script>

<style lang="scss" scoped>
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.error-icon {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  
  &.icon-network {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    color: #ff9800;
  }
  
  &.icon-server {
    background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    color: #f44336;
  }
  
  &.icon-auth {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    color: #2196F3;
  }
  
  &.icon-custom {
    background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
    color: #999;
  }
}

.error-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0 0 8px 0;
}

.error-desc {
  font-size: 14px;
  color: #999;
  margin: 0 0 24px 0;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 12px;
  
  .van-button {
    min-width: 120px;
    height: 44px;
  }
}
</style>