<template>
  <div class="profile-page">
    <AppNavbar title="个人中心" :showBack="false" />

    <div class="page-body">
      <!-- 用户信息头部 — Clay 软糯大卡 + 立体头像 -->
      <div class="clay-card clay-card--feature clay-card--soft-brand profile-header">
        <div class="profile-avatar">
          <LocalIcon name="user-o" size="64" />
        </div>
        <div class="profile-info">
          <h2 class="user-name">{{ userInfo.username }}</h2>
          <p class="user-email">{{ userInfo.email }}</p>
          <div class="profile-tags">
            <span class="clay-badge clay-badge--brand">健康饮食</span>
            <span class="clay-badge clay-badge--peach">家庭版</span>
          </div>
        </div>
        <button class="profile-edit-btn">
          <LocalIcon name="setting-o" size="16" />
        </button>
      </div>

      <!-- 数据统计条 -->
      <div class="stats-row">
        <div class="stat-card stat-card--brand">
          <span class="stat-num">{{ basketCount }}</span>
          <span class="stat-label">食材</span>
        </div>
        <div class="stat-card stat-card--orange">
          <span class="stat-num">{{ familyMembers.length }}</span>
          <span class="stat-label">家人</span>
        </div>
        <div class="stat-card stat-card--blue">
          <span class="stat-num">{{ mealCount }}</span>
          <span class="stat-label">餐次</span>
        </div>
      </div>

      <!-- 家庭成员 -->
      <div class="clay-card section-card">
        <div class="section-title-row">
          <div>
            <span class="section-eyebrow">FAMILY</span>
            <h3 class="section-title">家庭成员</h3>
          </div>
          <span class="section-count">{{ familyMembers.length }} 位</span>
        </div>
        <div class="family-members-list">
          <div v-for="member in familyMembers" :key="member.id" class="member-item">
            <div class="member-avatar" :style="getMemberStyle(member)">
              <span class="member-emoji">{{ getMemberEmoji(member) }}</span>
            </div>
            <div class="member-info">
              <span class="member-name">{{ member.name }}</span>
              <span class="member-relation">{{ member.relation || '家庭成员' }}</span>
            </div>
            <LocalIcon name="arrow" size="14" color="var(--ab-text-disabled)" />
          </div>
          <div class="member-action-row">
            <button v-if="!currentFamilyId" class="add-member-btn add-member-btn--brand" @click="showCreateFamily = true">
              <LocalIcon name="plus" size="16" color="var(--ab-brand-600)" />
              <span>创建家庭</span>
            </button>
            <button class="add-member-btn add-member-btn--blue" @click="showInviteCode = true">
              <LocalIcon name="qr" size="16" color="var(--ab-blue-600)" />
              <span>邀请成员</span>
            </button>
          </div>
        </div>
      </div>

      <!-- 功能菜单 -->
      <div class="clay-card section-card">
        <div class="section-title-row">
          <div>
            <span class="section-eyebrow">MENU</span>
            <h3 class="section-title">功能</h3>
          </div>
        </div>
        <div class="menu-list">
          <div class="menu-item" @click="$router.push('/basket')">
            <ClayIcon color="brand" size="sm">
              <LocalIcon name="shopping-cart" size="16" color="var(--ab-brand-600)" />
            </ClayIcon>
            <span>我的菜篮子</span>
            <LocalIcon name="arrow" size="14" color="var(--ab-text-disabled)" />
          </div>
          <div class="menu-item" @click="$router.push('/meal-plan')">
            <ClayIcon color="orange" size="sm">
              <LocalIcon name="calendar" size="16" color="var(--ab-orange-600)" />
            </ClayIcon>
            <span>食谱推荐</span>
            <LocalIcon name="arrow" size="14" color="var(--ab-text-disabled)" />
          </div>
          <div class="menu-item" @click="$router.push('/shopping-list')">
            <ClayIcon color="blue" size="sm">
              <LocalIcon name="list" size="16" color="var(--ab-blue-600)" />
            </ClayIcon>
            <span>采购清单</span>
            <LocalIcon name="arrow" size="14" color="var(--ab-text-disabled)" />
          </div>
          <div class="menu-item" @click="$router.push('/family-health')">
            <ClayIcon color="peach" size="sm">
              <LocalIcon name="heart" size="16" color="var(--ab-peach-600)" />
            </ClayIcon>
            <span>健康档案</span>
            <LocalIcon name="arrow" size="14" color="var(--ab-text-disabled)" />
          </div>
          <div class="menu-item" @click="$router.push('/demo')">
            <ClayIcon color="lilac" size="sm">
              <LocalIcon name="app" size="16" color="var(--ab-lilac-600)" />
            </ClayIcon>
            <span>组件展示</span>
            <LocalIcon name="arrow" size="14" color="var(--ab-text-disabled)" />
          </div>
        </div>
      </div>

      <!-- 退出登录 -->
      <div class="logout-section">
        <button class="clay-btn clay-btn--danger clay-btn--block" @click="handleLogout">
          <LocalIcon name="arrow-left" size="16" />
          <span>退出登录</span>
        </button>
      </div>

      <div style="height: 100px;"></div>
    </div>

    <AppTabbar :active="2" @change="handleTabChange" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showSuccessToast, showFailToast, showDialog } from 'vant'
import axios from '../utils/axios'
import { useAppStore } from '@/stores'
import AppNavbar from '@/components/AppNavbar.vue'
import AppTabbar from '@/components/AppTabbar.vue'
import ClayIcon from '@/components/ClayIcon.vue'

const router = useRouter()
const store = useAppStore()

const userInfo = ref({ username: '用户', email: 'user@example.com' })
const familyMembers = ref([])
const basketCount = ref(0)
const mealCount = ref(0)
const currentFamilyId = ref(null)
const showCreateFamily = ref(false)
const showInviteCode = ref(false)
const familyName = ref('')
const inviteCode = ref('')
const currentInviteCode = ref('')

const memberEmojiMap = { '爸爸': '👨', '妈妈': '👩', '儿子': '👦', '女儿': '👧', '爷爷': '👴', '奶奶': '👵', '我': '😊' }
const memberColorMap = ['brand', 'orange', 'blue', 'lilac', 'peach', 'mint', 'pink']

const getMemberEmoji = (m) => memberEmojiMap[m.name] || '😊'
const getMemberStyle = (m) => {
  const idx = familyMembers.value.indexOf(m) % memberColorMap.length
  const colorMap = {
    brand: 'linear-gradient(135deg, var(--ab-brand-200), var(--ab-brand-400))',
    orange: 'linear-gradient(135deg, var(--ab-orange-200), var(--ab-orange-400))',
    blue: 'linear-gradient(135deg, var(--ab-blue-200), var(--ab-blue-400))',
    lilac: 'linear-gradient(135deg, var(--ab-lilac-200), var(--ab-lilac-400))',
    peach: 'linear-gradient(135deg, var(--ab-peach-200), var(--ab-peach-400))',
    mint: 'linear-gradient(135deg, var(--ab-mint-200), var(--ab-mint-400))',
    pink: 'linear-gradient(135deg, var(--ab-pink-200), var(--ab-pink-400))',
  }
  return { background: colorMap[memberColorMap[idx]] }
}

const loadFamilyMembers = async () => {
  try {
    const res = await axios.get('/family/my')
    const families = res.families || res
    if (families && families.length > 0) {
      currentFamilyId.value = families[0].id
      familyMembers.value = families[0].members || []
    }
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    if (user.username) userInfo.value = user
    basketCount.value = store.basketCount || 0
    mealCount.value = 12
  } catch (e) {
    familyMembers.value = [
      { id: 1, name: '爸爸', relation: '父亲' },
      { id: 2, name: '妈妈', relation: '母亲' },
    ]
    basketCount.value = 8
    mealCount.value = 12
  }
}

const handleCreateFamily = async () => {
  try {
    const res = await store.createFamily({ name: familyName.value })
    if (res && res.id) {
      showSuccessToast('创建成功')
      showCreateFamily.value = false
      await loadFamilyMembers()
    }
  } catch (e) {
    showFailToast('创建失败')
  }
}

const handleLogout = () => {
  showDialog({ message: '确定退出登录？' }).then(() => {
    store.logout()
    router.replace('/login')
  })
}

const handleTabChange = (index, item) => {
  if (item.path) router.push(item.path)
}

onMounted(() => { loadFamilyMembers() })
</script>

<style scoped lang="scss">
.profile-page {
  min-height: 100vh;
  background: transparent;
}

.page-body {
  padding: var(--ab-space-4);
  padding-bottom: 80px;
  display: flex;
  flex-direction: column;
  gap: var(--ab-space-4);
}

/* Profile 头部 — 大 Clay 卡 */
.profile-header {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--ab-space-4);
  padding: var(--ab-space-5);
}
.profile-avatar {
  width: 72px;
  height: 72px;
  border-radius: 24px;
  background: linear-gradient(135deg, var(--ab-brand-200), var(--ab-brand-400));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--ab-shadow-float);
  flex-shrink: 0;
}
.profile-emoji {
  font-size: 38px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.10));
  line-height: 1;
}
.profile-info {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.user-name {
  font-size: 24px;
  font-weight: 700;
  color: var(--ab-text-primary);
  letter-spacing: -0.02em;
  line-height: 1.1;
}
.user-email {
  font-size: 12px;
  color: var(--ab-text-tertiary);
  font-weight: 500;
}
.profile-tags {
  display: flex;
  gap: 6px;
  margin-top: 4px;
}
.profile-edit-btn {
  width: 40px;
  height: 40px;
  border-radius: 14px;
  background: #ffffff;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--ab-shadow-float-sm);
  color: var(--ab-text-secondary);
  transition: transform var(--ab-transition-fast);
  flex-shrink: 0;
  &:active { transform: scale(0.92); }
}

/* 统计条 */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
.stat-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 14px 8px;
  border-radius: 18px;
  background: #ffffff;
  box-shadow: var(--ab-shadow-float-sm);
  border: 1px solid var(--ab-border-subtle);
  position: relative;
  overflow: hidden;

  &--brand  { background: linear-gradient(135deg, var(--ab-brand-50) 0%, #fff 100%); }
  &--orange { background: linear-gradient(135deg, var(--ab-orange-50) 0%, #fff 100%); }
  &--blue   { background: linear-gradient(135deg, var(--ab-blue-50) 0%, #fff 100%); }
}
.stat-num {
  font-size: 26px;
  font-weight: 700;
  color: var(--ab-text-primary);
  letter-spacing: -0.02em;
  line-height: 1;
}
.stat-label {
  font-size: 11px;
  color: var(--ab-text-tertiary);
  font-weight: 600;
  margin-top: 2px;
}

/* Section 卡 */
.section-card {
  padding: var(--ab-space-5);
}
.section-title-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: var(--ab-space-4);
}
.section-eyebrow {
  display: block;
  font-size: 10px;
  font-weight: 700;
  color: var(--ab-brand-600);
  letter-spacing: 0.12em;
  margin-bottom: 4px;
}
.section-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--ab-text-primary);
  letter-spacing: -0.02em;
  line-height: 1.1;
}
.section-count {
  font-size: 12px;
  color: var(--ab-text-tertiary);
  font-weight: 600;
  padding: 4px 10px;
  background: var(--ab-brand-50);
  border-radius: 9999px;
}

.family-members-list {
  display: flex;
  flex-direction: column;
  gap: var(--ab-space-3);
}
.member-item {
  display: flex;
  align-items: center;
  gap: var(--ab-space-3);
  padding: 8px 0;
}
.member-avatar {
  width: 44px;
  height: 44px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--ab-shadow-float-sm);
}
.member-emoji {
  font-size: 22px;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.08));
  line-height: 1;
}
.member-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  .member-name { font-size: 15px; font-weight: 600; color: var(--ab-text-primary); letter-spacing: -0.01em; }
  .member-relation { font-size: 11px; color: var(--ab-text-tertiary); font-weight: 500; }
}
.member-action-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-top: 4px;
}
.add-member-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 12px;
  border-radius: 14px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--ab-transition-fast);
  background: #ffffff;
  box-shadow: var(--ab-shadow-float-sm);
  font-family: inherit;

  &--brand {
    background: var(--ab-brand-50);
    color: var(--ab-brand-700);
    border: 1.5px solid var(--ab-brand-200);
  }
  &--blue {
    background: var(--ab-blue-50);
    color: var(--ab-blue-700);
    border: 1.5px solid var(--ab-blue-200);
  }
  &:active { transform: scale(0.97); }
}

.menu-list {
  display: flex;
  flex-direction: column;
}
.menu-item {
  display: flex;
  align-items: center;
  gap: var(--ab-space-3);
  padding: 12px 0;
  border-bottom: 1px solid var(--ab-border-subtle);
  cursor: pointer;
  transition: opacity var(--ab-transition-fast);
  &:last-child { border-bottom: none; }
  &:active { opacity: 0.6; }
  span { flex: 1; font-size: 14px; color: var(--ab-text-primary); font-weight: 600; letter-spacing: -0.01em; }
}

.logout-section {
  margin-top: var(--ab-space-4);
}
</style>
