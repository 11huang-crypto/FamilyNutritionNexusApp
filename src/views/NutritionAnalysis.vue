<template>
  <div class="nutrition-analysis">
    <!-- 页面头部 -->
    <van-nav-bar title="营养分析" left-arrow @click-left="handleBack" />
    
    <!-- 加载状态 -->
    <van-loading v-if="loading" class="loading" />
    
    <!-- 错误状态 -->
    <ErrorState 
      v-else-if="error" 
      :type="errorType"
      :showRetry="true"
      :loading="retryLoading"
      @retry="loadNutritionData"
    />
    
    <!-- 空状态 -->
    <EmptyState 
      v-else-if="!error && !nutritionData" 
      type="list"
      :showAction="true"
      actionText="去分析"
      @action="goToRecognize"
    />
    
    <!-- 内容区域 -->
    <van-scroll-view v-else scroll-y class="content">
      <!-- 食物基本信息 -->
      <van-card>
        <div class="food-header">
          <van-image 
            :src="nutritionData.image" 
            mode="aspectFill" 
            class="food-image"
          />
          <div class="food-info">
            <h3 class="food-name">{{ nutritionData.name }}</h3>
            <p class="food-category">{{ nutritionData.category }}</p>
          </div>
        </div>
      </van-card>
      
      <!-- 营养成分概览 -->
      <van-card title="营养成分概览">
        <van-grid :column-num="4" border="false">
          <van-grid-item 
            v-for="item in nutritionOverview" 
            :key="item.label"
            class="nutrition-item"
          >
            <div class="nutrition-value">{{ item.value }}</div>
            <div class="nutrition-label">{{ item.label }}</div>
          </van-grid-item>
        </van-grid>
      </van-card>
      
      <!-- 详细营养数据 -->
      <van-card title="详细营养数据">
        <van-cell-group inset>
          <van-cell 
            v-for="(value, key) in nutritionData.details" 
            :key="key"
            :title="key"
            :value="value"
            class="detail-item"
          />
        </van-cell-group>
      </van-card>
      
      <!-- 健康建议 -->
      <van-card title="健康建议">
        <van-tag 
          v-for="(tag, index) in nutritionData.healthTags" 
          :key="index"
          :type="getTagType(tag)"
          class="health-tag"
        >
          {{ tag }}
        </van-tag>
        <p class="health-desc">{{ nutritionData.healthTips }}</p>
      </van-card>
    </van-scroll-view>
  </div>
</template>

<script setup>
/**
 * 营养分析页示例
 * 展示如何使用通用的请求工具、错误状态组件、空状态组件
 */

import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { vanLoading, vanImage } from 'vant';
import { get } from '@/utils/request';
import ErrorState from '@/components/ErrorState.vue';
import EmptyState from '@/components/EmptyState.vue';

// 路由实例
const router = useRouter();

// 响应式状态
const loading = ref(false);           // 加载状态
const error = ref(false);             // 错误状态
const errorType = ref('network');     // 错误类型
const retryLoading = ref(false);      // 重试加载状态
const nutritionData = ref(null);      // 营养数据

/**
 * 营养概览数据（用于展示在网格中）
 */
const nutritionOverview = computed(() => {
  if (!nutritionData.value) return [];
  
  const data = nutritionData.value;
  return [
    { label: '热量', value: data.calories + ' kcal' },
    { label: '蛋白质', value: data.protein + 'g' },
    { label: '碳水', value: data.carbs + 'g' },
    { label: '脂肪', value: data.fat + 'g' }
  ];
});

/**
 * 获取标签类型
 */
const getTagType = (tag) => {
  if (tag.includes('高')) return 'danger';
  if (tag.includes('低')) return 'success';
  if (tag.includes('适宜')) return 'primary';
  return 'default';
};

/**
 * 加载营养数据
 */
const loadNutritionData = async () => {
  // 设置加载状态
  loading.value = true;
  error.value = false;
  
  try {
    // 使用封装的 get 方法请求数据
    const response = await get(
      '/nutrition/analysis',
      { id: '123' }, // 示例参数
      {
        showLoading: true,           // 显示加载动画（默认）
        loadingText: '分析中...',    // 自定义加载文字
        forbidClick: true,           // 加载时禁止点击（默认）
        showError: true,             // 显示错误提示（默认）
        showRetry: true,             // 显示重试弹窗
        retryCallback: loadNutritionData // 重试回调
      }
    );
    
    // 成功获取数据
    nutritionData.value = response.data;
  } catch (err) {
    // 捕获错误，设置错误状态
    error.value = true;
    
    // 根据错误类型设置对应的错误提示
    if (err.message.includes('网络')) {
      errorType.value = 'network';
    } else if (err.message.includes('权限')) {
      errorType.value = 'auth';
    } else {
      errorType.value = 'server';
    }
  } finally {
    loading.value = false;
  }
};

/**
 * 返回上一页
 */
const handleBack = () => {
  router.back();
};

/**
 * 跳转到识别页
 */
const goToRecognize = () => {
  router.push('/recognize');
};

/**
 * 页面挂载时加载数据
 */
onMounted(() => {
  loadNutritionData();
});
</script>

<style lang="scss" scoped>
.nutrition-analysis {
  min-height: 100vh;
  background: #f5f5f5;
}

.loading {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.content {
  height: calc(100vh - 46px);
  padding: 16px;
}

.food-header {
  display: flex;
  gap: 16px;
}

.food-image {
  width: 100px;
  height: 100px;
  border-radius: 8px;
}

.food-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.food-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0 0 8px 0;
}

.food-category {
  font-size: 14px;
  color: #999;
  margin: 0;
}

.nutrition-item {
  text-align: center;
}

.nutrition-value {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.nutrition-label {
  font-size: 12px;
  color: #999;
}

.detail-item {
  font-size: 14px;
}

.health-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.health-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin: 12px 0 0 0;
}
</style>