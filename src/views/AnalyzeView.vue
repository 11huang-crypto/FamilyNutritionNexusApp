<template>
  <div class="analyze-page">
    <AppNavbar title="AI智能识图" />
    
    <div class="page-body">
      <div class="upload-area card-base" @click="handleUpload">
        <template v-if="!analyzing && !selectedImage">
          <div class="upload-icon-wrap">
            <van-icon name="camera" size="48" color="#22c55e" />
          </div>
          <p class="upload-title">拍照识别食材</p>
          <p class="upload-hint">支持拍照或从相册选择</p>
          <van-button type="primary" round size="small" style="margin-top: 12px;">拍照 / 选图</van-button>
        </template>

        <template v-if="selectedImage && !analyzing">
          <div class="preview-wrap">
            <img :src="selectedImage" alt="预览" class="preview-img" />
          </div>
          <div class="preview-actions">
            <van-button type="primary" round size="small" @click.stop="startAnalyze">开始分析</van-button>
            <van-button plain round size="small" @click.stop="selectedImage = ''">重新选择</van-button>
          </div>
        </template>

        <template v-if="analyzing">
          <div class="analyzing-wrap">
            <van-loading type="spinner" size="48" color="#22c55e" />
            <p class="analyzing-text">AI 正在识别食材...</p>
            <van-progress :percentage="analyzeProgress" stroke-color="#22c55e" style="width: 200px;" />
          </div>
        </template>
      </div>

      <div v-if="results.length > 0" class="results-area">
        <h3 class="section-label">识别结果</h3>
        <div v-for="item in results" :key="item.name" class="result-card card-base">
          <div class="result-header">
            <img :src="item.image" :alt="item.name" class="result-img" />
            <div class="result-info">
              <div class="result-name-row">
                <h4 class="result-name">{{ item.name }}</h4>
                <span class="food-emoji">{{ getEmoji(item.name) }}</span>
              </div>
              <span class="result-category">{{ item.category }}</span>
              <div class="confidence-bar">
                <div class="confidence-fill" :style="{ width: item.confidence + '%' }"></div>
                <span class="confidence-text">置信度 {{ item.confidence }}%</span>
              </div>
            </div>
            <van-button type="primary" size="small" round @click="addToBasket(item)">加入篮子</van-button>
          </div>
          
          <div class="nutrition-section">
            <div class="nutrition-title">营养成分</div>
            <div class="nutrition-grid">
              <div class="nutrition-item">
                <div class="nutrition-icon">🔥</div>
                <div class="nutrition-label">热量</div>
                <div class="nutrition-value">{{ item.calories || 0 }} kcal</div>
              </div>
              <div class="nutrition-item">
                <div class="nutrition-icon">💪</div>
                <div class="nutrition-label">蛋白质</div>
                <div class="nutrition-value">{{ item.nutrients?.protein || 0 }}g</div>
              </div>
              <div class="nutrition-item">
                <div class="nutrition-icon">🥦</div>
                <div class="nutrition-label">纤维</div>
                <div class="nutrition-value">{{ item.nutrients?.fiber || 0 }}g</div>
              </div>
              <div class="nutrition-item">
                <div class="nutrition-icon">🍬</div>
                <div class="nutrition-label">碳水</div>
                <div class="nutrition-value">{{ item.carbs || 0 }}g</div>
              </div>
            </div>
            
            <div class="vitamin-section">
              <div class="vitamin-title">维生素含量</div>
              <div class="vitamin-list">
                <div v-for="(value, key) in item.nutrients" :key="key" class="vitamin-item">
                  <span class="vitamin-name">{{ getLabel(key) }}</span>
                  <div class="vitamin-bar-wrap">
                    <div class="vitamin-bar" :style="{ width: Math.min(value * 2, 100) + '%' }" :class="getType(key)"></div>
                  </div>
                  <span class="vitamin-value">{{ value }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="suggestions.length > 0" class="suggestions-area">
        <h3 class="section-label">搭配建议</h3>
        <div v-for="(s, index) in suggestions" :key="index" class="suggestion-card card-base" @click="handleSuggestionClick(s)">
          <div class="suggestion-header">
            <span class="suggestion-icon">{{ getEmoji(s.name) }}</span>
            <span class="sug-name">{{ s.name }}</span>
            <span v-if="s.food" class="sug-pair" :class="{ 'conflict-pair': s.type === '食物相克' }">
              <span class="pair-arrow">{{ s.type === '食物相克' ? '✖️' : '→' }}</span>
              <span class="pair-food">{{ getEmoji(s.food) }} {{ s.food }}</span>
            </span>
          </div>
          <div class="suggestion-content">
            <div class="suggestion-tag" :class="getSuggestionType(s.type)">{{ s.type }}</div>
            <p class="sug-reason">{{ s.reason }}</p>
          </div>
          <div class="suggestion-footer" v-if="s.type !== '食物相克'">
            <span class="view-recipe">查看做法 →</span>
          </div>
        </div>
      </div>
    </div>

    <van-popup v-model:show="showRecipeModal" position="bottom" :style="{ height: '85%' }">
      <div class="recipe-modal">
        <div class="recipe-modal-header">
          <h3 class="recipe-modal-title">{{ currentRecipe?.name }}</h3>
          <van-button icon="cross" size="small" @click="showRecipeModal = false" />
        </div>
        
        <div class="recipe-modal-body" v-if="currentRecipe">
          <div class="recipe-info-row">
            <div class="recipe-info-item">
              <span class="recipe-info-icon">⏱️</span>
              <span class="recipe-info-text">{{ currentRecipe.cooking_time }}分钟</span>
            </div>
            <div class="recipe-info-item">
              <span class="recipe-info-icon">📊</span>
              <span class="recipe-info-text">{{ getDifficultyText(currentRecipe.difficulty) }}</span>
            </div>
            <div class="recipe-info-item">
              <span class="recipe-info-icon">🍽️</span>
              <span class="recipe-info-text">{{ currentRecipe.meal_type.join(' / ') }}</span>
            </div>
          </div>

          <div class="recipe-section">
            <h4 class="recipe-section-title">食材清单</h4>
            <div class="recipe-ingredients">
              <div v-for="(ing, idx) in currentRecipe.ingredients" :key="idx" class="recipe-ingredient-item">
                <span class="recipe-ingredient-name">{{ ing.name }}</span>
                <span class="recipe-ingredient-quantity">{{ ing.quantity }}{{ ing.unit }}</span>
              </div>
            </div>
          </div>

          <div class="recipe-section">
            <h4 class="recipe-section-title">营养成分</h4>
            <div class="recipe-nutrition">
              <div class="nutrition-tag">🔥 {{ currentRecipe.nutrition.calories }} kcal</div>
              <div class="nutrition-tag">💪 {{ currentRecipe.nutrition.protein }}g</div>
              <div class="nutrition-tag">🍬 {{ currentRecipe.nutrition.carbs }}g</div>
              <div class="nutrition-tag">🧈 {{ currentRecipe.nutrition.fat }}g</div>
            </div>
          </div>

          <div class="recipe-section">
            <h4 class="recipe-section-title">烹饪步骤</h4>
            <div class="recipe-steps">
              <div v-for="(step, idx) in currentRecipe.steps" :key="idx" class="recipe-step-item">
                <span class="step-number">{{ idx + 1 }}</span>
                <p class="step-text">{{ step }}</p>
              </div>
            </div>
          </div>

          <div class="recipe-section">
            <h4 class="recipe-section-title">适合人群</h4>
            <div class="recipe-suitable">
              <span v-for="s in currentRecipe.suitable_for" :key="s" class="suitable-tag">{{ s }}</span>
            </div>
          </div>
        </div>

        <div v-else class="recipe-empty">
          <van-icon name="search" size="48" color="#999" />
          <p>暂无相关食谱</p>
          <van-button type="primary" @click="showRecipeModal = false">关闭</van-button>
        </div>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppNavbar from '@/components/AppNavbar.vue'
import AppTabbar from '@/components/AppTabbar.vue'
import { useAppStore } from '@/stores'
import { analyzeImage } from '@/api'
import axios from '@/utils/axios'
import { Toast } from 'vant'

const store = useAppStore()
const router = useRouter()

const selectedImage = ref('')
const selectedFile = ref(null)
const analyzing = ref(false)
const analyzeProgress = ref(0)
const results = ref([])
const suggestions = ref([])
const showRecipeModal = ref(false)
const currentRecipe = ref(null)

const foodEmojis = {
  '番茄': '🍅', '西红柿': '🍅', '胡萝卜': '🥕', '西兰花': '🥦', '黄瓜': '🥒',
  '土豆': '🥔', '洋葱': '🧅', '辣椒': '🌶️', '茄子': '🍆', '白菜': '🥬',
  '菠菜': '🥬', '生菜': '🥬', '蘑菇': '🍄', '青椒': '🫑', '南瓜': '🎃',
  '苹果': '🍎', '香蕉': '🍌', '橙子': '🍊', '葡萄': '🍇', '草莓': '🍓',
  '西瓜': '🍉', '梨': '🍐', '桃子': '🍑', '芒果': '🥭', '蓝莓': '🫐',
  '鸡蛋': '🥚', '牛奶': '🥛', '面包': '🍞', '米饭': '🍚', '肉': '🥩',
  '鱼': '🐟', '虾': '🦐', '豆腐': '🧈', '坚果': '🥜'
}

const getEmoji = (name) => {
  for (const key in foodEmojis) {
    if (name.includes(key)) return foodEmojis[key]
  }
  return '🥗'
}

const handleUpload = () => {
  if (analyzing.value) return
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.capture = 'environment'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (file) {
      compressImage(file, 800, 0.8).then(compressedFile => {
        selectedImage.value = URL.createObjectURL(compressedFile)
        selectedFile.value = compressedFile
      })
    }
  }
  input.click()
}

const compressImage = (file, maxWidth, quality) => {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => {
        let width = img.width
        let height = img.height
        if (width > maxWidth) {
          height = height * (maxWidth / width)
          width = maxWidth
        }
        const canvas = document.createElement('canvas')
        canvas.width = width
        canvas.height = height
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0, width, height)
        canvas.toBlob((blob) => {
          const compressedFile = new File([blob], file.name, { type: 'image/jpeg' })
          resolve(compressedFile)
        }, 'image/jpeg', quality)
      }
      img.src = e.target.result
    }
    reader.readAsDataURL(file)
  })
}

const startAnalyze = async () => {
  if (!selectedFile.value) return
  analyzing.value = true
  analyzeProgress.value = 0

  const progressInterval = setInterval(() => {
    analyzeProgress.value = Math.min(100, analyzeProgress.value + Math.random() * 20)
  }, 300)

  try {
    const formData = new FormData()
    formData.append('image', selectedFile.value)
    const res = await analyzeImage(formData)
    
    results.value = (res.ingredients || []).map(item => ({
      name: item.name,
      category: '蔬菜',
      confidence: item.confidence,
      calories: item.nutrition?.calories || 0,
      carbs: item.nutrition?.carbs || 0,
      image: `https://neeko-copilot.bytedance.net/api/text_to_image?prompt=fresh%20${encodeURIComponent(item.name)}%20vegetable%20on%20white%20background&image_size=square`,
      nutrients: {
        vitaminC: item.nutrition?.vitamins?.C || 0,
        vitaminA: item.nutrition?.vitamins?.A || 0,
        vitaminK: item.nutrition?.vitamins?.K || 0,
        fiber: item.nutrition?.fiber || 0,
        protein: item.nutrition?.protein || 0,
        iron: 0,
        potassium: 0,
        calcium: 0
      }
    }))

    if (res.recommendations) {
      suggestions.value = res.recommendations.map(r => ({
        name: r.ingredient,
        food: r.food,
        reason: r.reason,
        type: r.type || '营养搭配'
      }))
    }

    analyzeProgress.value = 100
    setTimeout(() => { analyzing.value = false }, 500)
  } catch (err) {
    analyzing.value = false
    Toast.fail('识别服务暂不可用，请稍后重试')
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

const getSuggestionType = (type) => {
  const map = { '营养搭配': 'nutri', '食用建议': 'diet', '烹饪建议': 'cook', '美味搭配': 'taste', '食物相克': 'conflict' }
  return map[type] || 'default'
}

const handleSuggestionClick = async (suggestion) => {
  if (suggestion.type === '食物相克') {
    return
  }
  
  const ingredient = suggestion.food || suggestion.name
  try {
    const response = await axios.get(`/recipes/search?ingredient=${encodeURIComponent(ingredient)}`)
    
    if (response.recipes && response.recipes.length > 0) {
      currentRecipe.value = response.recipes[0]
      showRecipeModal.value = true
    } else {
      currentRecipe.value = null
      showRecipeModal.value = true
    }
  } catch (error) {
    console.error('获取食谱失败:', error)
    Toast.fail('获取食谱失败')
  }
}

const getDifficultyText = (difficulty) => {
  const map = { 'easy': '简单', 'medium': '中等', 'hard': '困难' }
  return map[difficulty] || difficulty
}

const handleTabChange = (index, item) => {
  if (item.path) {
    router.push(item.path)
  }
}
</script>

<style scoped lang="scss">
.analyze-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-body {
  padding: 16px;
  padding-bottom: 80px;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 240px;
  text-align: center;
  border: none;
  border-radius: 20px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%);
  box-shadow: 0 4px 20px rgba(34, 197, 94, 0.15);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;

  &:active {
    transform: scale(0.98);
  }
}

.upload-icon-wrap {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
  margin-bottom: 16px;
}

.upload-title {
  font-size: 18px;
  font-weight: 700;
  color: #15803d;
  margin-bottom: 8px;
}

.upload-hint {
  font-size: 14px;
  color: #16a34a;
  opacity: 0.8;
}

.preview-wrap {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.preview-img {
  width: 100%;
  height: auto;
  object-fit: contain;
}

.preview-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.analyzing-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 24px 0;
}

.analyzing-text {
  font-size: 18px;
  color: #15803d;
  font-weight: 600;
}

.results-area,
.suggestions-area {
  margin-top: 24px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 16px;

  &::before {
    content: '';
    width: 4px;
    height: 20px;
    background: linear-gradient(180deg, #22c55e, #86efac);
    border-radius: 2px;
  }
}

.result-card {
  margin-bottom: 16px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #ffffff, #f0fdf4);
}

.result-img {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.result-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.result-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.result-name {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
}

.food-emoji {
  font-size: 24px;
}

.result-category {
  font-size: 14px;
  color: #6b7280;
  background: #f0fdf4;
  padding: 3px 10px;
  border-radius: 12px;
  width: fit-content;
}

.confidence-bar {
  position: relative;
  height: 20px;
  background: #f3f4f6;
  border-radius: 10px;
  overflow: hidden;
}

.confidence-fill {
  height: 100%;
  background: linear-gradient(90deg, #22c55e, #4ade80);
  border-radius: 10px;
  transition: width 0.5s ease;
}

.confidence-text {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  color: #166534;
  line-height: 20px;
}

.nutrition-section {
  padding: 16px;
  background: #fafbfc;
  border-top: 1px solid #e5e7eb;
}

.nutrition-title {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;
}

.nutrition-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.nutrition-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 8px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.nutrition-icon {
  font-size: 24px;
  margin-bottom: 6px;
}

.nutrition-label {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.nutrition-value {
  font-size: 14px;
  font-weight: 700;
  color: #1f2937;
}

.vitamin-section {
  background: #ffffff;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.vitamin-title {
  font-size: 14px;
  font-weight: 600;
  color: #4b5563;
  margin-bottom: 12px;
}

.vitamin-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.vitamin-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.vitamin-name {
  width: 30px;
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
}

.vitamin-bar-wrap {
  flex: 1;
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}

.vitamin-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;

  &.vitamin {
    background: linear-gradient(90deg, #f59e0b, #fbbf24);
  }
  &.fiber {
    background: linear-gradient(90deg, #10b981, #34d399);
  }
  &.protein {
    background: linear-gradient(90deg, #3b82f6, #60a5fa);
  }
  &.mineral {
    background: linear-gradient(90deg, #8b5cf6, #a78bfa);
  }
  &.other {
    background: linear-gradient(90deg, #6b7280, #9ca3af);
  }
}

.vitamin-value {
  width: 45px;
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
  text-align: right;
}

.suggestion-card {
  margin-bottom: 12px;
  padding: 16px;
  border-radius: 16px;
  background: linear-gradient(135deg, #fffbeb, #fef3c7);
  border-left: 4px solid #f59e0b;
}

.suggestion-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.suggestion-icon {
  font-size: 20px;
}

.sug-name {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.sug-pair {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: auto;
  padding: 4px 10px;
  background: rgba(34, 197, 94, 0.1);
  border-radius: 12px;
}

.pair-arrow {
  color: #22c55e;
  font-weight: 700;
}

.pair-food {
  font-size: 14px;
  font-weight: 600;
  color: #166534;
}

.suggestion-content {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.suggestion-tag {
  padding: 3px 8px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;

  &.nutri {
    background: #dbeafe;
    color: #1d4ed8;
  }
  &.diet {
    background: #dcfce7;
    color: #166534;
  }
  &.cook {
    background: #fce7f3;
    color: #9d174d;
  }
  &.taste {
    background: #fef3c7;
    color: #92400e;
  }
  &.conflict {
    background: #fee2e2;
    color: #991b1b;
  }
  &.default {
    background: #f3f4f6;
    color: #6b7280;
  }
}

.sug-reason {
  flex: 1;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
}

.suggestion-footer {
  margin-top: 10px;
  text-align: right;
}

.view-recipe {
  font-size: 13px;
  color: #22c55e;
  font-weight: 600;
}

.conflict-pair {
  background: rgba(239, 68, 68, 0.1);
  
  .pair-arrow {
    color: #ef4444;
    font-weight: 700;
  }
  
  .pair-food {
    color: #991b1b;
  }
}

.recipe-modal {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
}

.recipe-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
}

.recipe-modal-title {
  font-size: 18px;
  font-weight: 700;
  color: #166534;
}

.recipe-modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.recipe-info-row {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.recipe-info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 12px;
}

.recipe-info-icon {
  font-size: 16px;
}

.recipe-info-text {
  font-size: 13px;
  color: #4b5563;
  font-weight: 500;
}

.recipe-section {
  margin-bottom: 20px;
}

.recipe-section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  
  &::before {
    content: '';
    width: 4px;
    height: 16px;
    background: #22c55e;
    border-radius: 2px;
  }
}

.recipe-ingredients {
  background: #f8fafc;
  border-radius: 12px;
  padding: 12px;
}

.recipe-ingredient-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e5e7eb;
  
  &:last-child {
    border-bottom: none;
  }
}

.recipe-ingredient-name {
  font-size: 14px;
  color: #374151;
}

.recipe-ingredient-quantity {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.recipe-nutrition {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.nutrition-tag {
  padding: 6px 12px;
  background: #f0fdf4;
  border-radius: 20px;
  font-size: 13px;
  color: #166534;
  font-weight: 500;
}

.recipe-steps {
  background: #f8fafc;
  border-radius: 12px;
  padding: 12px;
}

.recipe-step-item {
  display: flex;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #e5e7eb;
  
  &:last-child {
    border-bottom: none;
  }
}

.step-number {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #22c55e;
  color: #fff;
  border-radius: 50%;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
}

.step-text {
  flex: 1;
  font-size: 14px;
  color: #374151;
  line-height: 1.6;
  margin: 0;
}

.recipe-suitable {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.suitable-tag {
  padding: 5px 12px;
  background: #dbeafe;
  border-radius: 12px;
  font-size: 12px;
  color: #1d4ed8;
}

.recipe-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #9ca3af;
}
</style>