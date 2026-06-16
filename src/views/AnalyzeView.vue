<template>
  <!--
    AnalyzeView.vue - 拍照识材页
    拍照/选图 → AI识别 → 营养分析 → 加入菜篮子
  -->
  <div class="analyze-page">
    <AppNavbar title="拍照识材" />

    <div class="page-body">
      <!-- 上传区域 -->
      <div class="upload-area card-base" @click="handleUpload">
        <template v-if="!analyzing && !selectedImage">
          <div class="upload-icon">
            <van-icon name="photo" size="48" color="#22c55e" />
          </div>
          <p class="upload-title">拍照识别食材</p>
          <p class="upload-hint">支持拍照或从相册选择</p>
          <van-button type="primary" round size="small" style="margin-top: 12px;">拍照 / 选图</van-button>
        </template>

        <!-- 已选图片预览 -->
        <template v-if="selectedImage && !analyzing">
          <div class="preview-wrap">
            <img :src="selectedImage" alt="预览" class="preview-img" />
          </div>
          <div class="preview-actions">
            <van-button type="primary" round size="small" @click.stop="startAnalyze">开始分析</van-button>
            <van-button plain round size="small" @click.stop="selectedImage = ''">重新选择</van-button>
          </div>
        </template>

        <!-- 分析中 -->
        <template v-if="analyzing">
          <div class="analyzing-wrap">
            <van-loading type="spinner" size="48" color="#22c55e" />
            <p class="analyzing-text">AI 正在识别食材...</p>
            <van-progress :percentage="analyzeProgress" stroke-color="#22c55e" style="width: 200px;" />
          </div>
        </template>
      </div>

      <!-- 识别结果 -->
      <div v-if="results.length > 0" class="results-area">
        <h3 class="section-label">识别结果</h3>

        <div v-for="item in results" :key="item.name" class="result-card card-base">
          <div class="result-header">
            <img :src="item.image" :alt="item.name" class="result-img" />
            <div class="result-info">
              <h4 class="result-name">{{ item.name }}</h4>
              <span class="result-category">{{ item.category }}</span>
              <span class="result-confidence">置信度 {{ item.confidence }}%</span>
            </div>
            <van-button type="primary" size="small" round @click="addToBasket(item)">加入篮子</van-button>
          </div>
          <div class="result-nutrients">
            <NutriBadge
              v-for="(value, key) in item.nutrients"
              :key="key"
              :type="getType(key)"
              :label="getLabel(key)"
              :value="value"
              size="sm"
            />
          </div>
        </div>
      </div>

      <!-- 智能搭配建议 -->
      <div v-if="suggestions.length > 0" class="suggestions-area">
        <h3 class="section-label">搭配建议</h3>
        <div v-for="s in suggestions" :key="s.name" class="suggestion-card card-base">
          <div class="flex-between">
            <span class="sug-name">{{ s.name }}</span>
            <span class="sug-price">¥{{ s.price }}</span>
          </div>
          <p class="sug-reason">{{ s.reason }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppNavbar from '@/components/AppNavbar.vue'
import NutriBadge from '@/components/NutriBadge.vue'
import { useAppStore } from '@/stores'
import { analyzeFood } from '@/api'

const store = useAppStore()

const selectedImage = ref('')
const analyzing = ref(false)
const analyzeProgress = ref(0)
const results = ref([])
const suggestions = ref([])

const handleUpload = () => {
  if (analyzing.value) return
  // 模拟选择图片
  selectedImage.value = new URL('@/assets/images/fruit/apple.jpg', import.meta.url).href
}

const startAnalyze = async () => {
  analyzing.value = true
  analyzeProgress.value = 0

  // 模拟进度
  const progressInterval = setInterval(() => {
    analyzeProgress.value = Math.min(100, analyzeProgress.value + Math.random() * 20)
  }, 300)

  try {
    const res = await analyzeFood({ name: 'photo.jpg', size: 1024 * 500 })
    results.value = res.data.results

    // 搭配建议
    if (res.data.estimatedPrices) {
      suggestions.value = res.data.estimatedPrices.map(p => ({
        ...p,
        reason: p.price < 5 ? '性价比高，建议购买' : '时令新鲜，值得尝试'
      }))
    }

    // 禁忌提示
    res.data.alerts.forEach(alert => {
      store.alerts.unshift({ id: Date.now(), ...alert })
    })

    analyzeProgress.value = 100
    setTimeout(() => { analyzing.value = false }, 500)
  } catch (err) {
    analyzing.value = false
  }
  clearInterval(progressInterval)
}

const addToBasket = (item) => {
  store.addToBasket({
    name: item.name,
    category: item.category,
    quantity: 1,
    unit: '个',
    freshness: item.confidence ? Math.round(item.confidence) + 5 : 95,
    image: item.image,
    nutrients: item.nutrients,
  })
  Toast.success(`已加入菜篮子: ${item.name}`)
}

const getType = (key) => {
  const map = { vitaminC: 'vitamin', vitaminA: 'vitamin', vitaminK: 'vitamin', fiber: 'fiber', protein: 'protein', iron: 'mineral', potassium: 'mineral', calcium: 'mineral' }
  return map[key] || 'other'
}

const getLabel = (key) => {
  const map = { vitaminC: '维C', vitaminA: '维A', vitaminK: '维K', fiber: '纤维', protein: '蛋白', iron: '铁', potassium: '钾', calcium: '钙' }
  return map[key] || key
}
</script>

<script>
import { Toast } from 'vant'
</script>

<style scoped lang="scss">
.analyze-page {
  min-height: 100vh;
  background: var(--ab-bg-page);
}

.page-body {
  padding: var(--ab-space-4);
  padding-bottom: 80px;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 220px;
  text-align: center;
  border: 2px dashed var(--ab-primary-200);
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
}

.upload-icon {
  margin-bottom: var(--ab-space-3);
}

.upload-title {
  font-size: var(--ab-text-lg);
  font-weight: var(--ab-font-bold);
  color: var(--ab-primary-700);
}

.upload-hint {
  font-size: var(--ab-text-sm);
  color: var(--ab-text-tertiary);
  margin-top: 4px;
}

.preview-wrap {
  width: 100%;
  max-height: 200px;
  overflow: hidden;
  border-radius: var(--ab-radius-md);
}

.preview-img {
  width: 100%;
  object-fit: cover;
  border-radius: var(--ab-radius-md);
}

.preview-actions {
  display: flex;
  gap: var(--ab-space-3);
  margin-top: var(--ab-space-4);
}

.analyzing-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--ab-space-3);
}

.analyzing-text {
  font-size: var(--ab-text-base);
  color: var(--ab-primary-700);
  font-weight: var(--ab-font-medium);
}

.results-area,
.suggestions-area {
  margin-top: var(--ab-space-6);
}

.section-label {
  font-size: var(--ab-text-base);
  font-weight: var(--ab-font-bold);
  color: var(--ab-text-primary);
  margin-bottom: var(--ab-space-3);
}

.result-card {
  margin-bottom: var(--ab-space-3);
}

.result-header {
  display: flex;
  align-items: center;
  gap: var(--ab-space-3);
  margin-bottom: var(--ab-space-3);
}

.result-img {
  width: 64px;
  height: 64px;
  border-radius: var(--ab-radius-md);
  object-fit: cover;
}

.result-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.result-name {
  font-size: var(--ab-text-lg);
  font-weight: var(--ab-font-bold);
  color: var(--ab-text-primary);
}

.result-category {
  font-size: var(--ab-text-sm);
  color: var(--ab-text-secondary);
}

.result-confidence {
  font-size: var(--ab-text-xs);
  color: var(--ab-success);
  font-weight: var(--ab-font-medium);
}

.result-nutrients {
  display: flex;
  gap: var(--ab-space-2);
  flex-wrap: wrap;
  padding-top: var(--ab-space-3);
  border-top: 1px solid var(--ab-border-light);
}

.suggestion-card {
  margin-bottom: var(--ab-space-2);
}

.sug-name {
  font-size: var(--ab-text-base);
  font-weight: var(--ab-font-medium);
  color: var(--ab-text-primary);
}

.sug-price {
  font-size: var(--ab-text-base);
  font-weight: var(--ab-font-bold);
  color: var(--ab-danger);
}

.sug-reason {
  font-size: var(--ab-text-sm);
  color: var(--ab-text-secondary);
  margin-top: 4px;
}
</style>
