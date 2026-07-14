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
            <button v-if="!currentFamilyId" class="add-member-btn add-member-btn--lilac" @click="showJoinFamily = true">
              <LocalIcon name="friends-o" size="16" color="var(--ab-lilac-600)" />
              <span>加入家庭</span>
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

    <!-- 创建家庭弹窗 -->
    <van-popup v-model:show="showCreateFamily" position="center" :style="{ width: '85%', borderRadius: '24px' }">
      <div class="modal-card">
        <h3 class="modal-card-title">创建新家庭</h3>
        <p class="modal-card-desc">输入家庭名称，开启智能营养生活</p>
        <div class="clay-input" style="margin-bottom: 16px;">
          <input v-model="familyName" type="text" placeholder="请输入家庭名称" @keyup.enter="handleCreateFamily" />
        </div>
        <div class="modal-btn-group">
          <button class="clay-btn clay-btn--primary clay-btn--block" :disabled="creatingFamily" @click="handleCreateFamily">
            <van-loading v-if="creatingFamily" size="18" color="#fff" />
            <span v-else>确认创建</span>
          </button>
          <button class="clay-btn clay-btn--secondary clay-btn--block" @click="showCreateFamily = false">取消</button>
        </div>
      </div>
    </van-popup>

    <!-- 邀请成员弹窗 -->
    <van-popup v-model:show="showInviteCode" position="center" :style="{ width: '85%', borderRadius: '24px' }">
      <div class="modal-card">
        <h3 class="modal-card-title">邀请成员</h3>
        <p class="modal-card-desc">通过邀请码或邮箱邀请家人加入</p>

        <!-- 邀请码显示区 -->
        <div v-if="currentInviteCode" class="invite-code-display">
          <span class="invite-code-label">邀请码</span>
          <div class="invite-code-value">{{ currentInviteCode }}</div>
          <span class="invite-code-hint">分享此邀请码给家人，输入后即可加入</span>
        </div>

        <!-- 生成邀请码按钮 -->
        <button v-if="!currentInviteCode && currentFamilyId" class="clay-btn clay-btn--primary clay-btn--block" style="margin-bottom: 12px;" :disabled="generatingCode" @click="handleGenerateCode">
          <van-loading v-if="generatingCode" size="18" color="#fff" />
          <span v-else>生成邀请码</span>
        </button>
        <p v-if="!currentFamilyId" class="modal-card-desc" style="color: var(--ab-warning);">请先创建或加入一个家庭</p>

        <!-- 邮箱邀请 -->
        <div class="invite-divider"><span>或通过邮箱邀请</span></div>
        <div class="clay-input" style="margin-bottom: 12px;">
          <input v-model="inviteEmail" type="email" placeholder="输入家人邮箱地址" />
        </div>
        <div class="modal-btn-group">
          <button class="clay-btn clay-btn--primary clay-btn--block" :disabled="invitingMember" @click="handleInviteByEmail">
            <van-loading v-if="invitingMember" size="18" color="#fff" />
            <span v-else>发送邀请</span>
          </button>
          <button class="clay-btn clay-btn--secondary clay-btn--block" @click="showInviteCode = false">关闭</button>
        </div>
      </div>
    </van-popup>

    <!-- 加入家庭弹窗 -->
    <van-popup v-model:show="showJoinFamily" position="center" :style="{ width: '85%', borderRadius: '24px' }">
      <div class="modal-card">
        <h3 class="modal-card-title">加入家庭</h3>
        <p class="modal-card-desc">输入邀请码加入家人的家庭</p>
        <div class="clay-input" style="margin-bottom: 16px;">
          <input v-model="joinCode" type="text" placeholder="请输入邀请码" @keyup.enter="handleJoinFamily" />
        </div>
        <div class="modal-btn-group">
          <button class="clay-btn clay-btn--primary clay-btn--block" :disabled="joiningFamily" @click="handleJoinFamily">
            <van-loading v-if="joiningFamily" size="18" color="#fff" />
            <span v-else>加入家庭</span>
          </button>
          <button class="clay-btn clay-btn--secondary clay-btn--block" @click="showJoinFamily = false">取消</button>
        </div>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showSuccessToast, showFailToast, showDialog } from 'vant'
import axios from '../utils/axios'
import { generateInviteCode, inviteMember, joinFamily } from '../api'
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
const showJoinFamily = ref(false)
const familyName = ref('')
const inviteCode = ref('')
const currentInviteCode = ref('')
const inviteEmail = ref('')
const joinCode = ref('')
const creatingFamily = ref(false)
const generatingCode = ref(false)
const invitingMember = ref(false)
const joiningFamily = ref(false)

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
  if (!familyName.value.trim()) {
    showFailToast('请输入家庭名称');
    return;
  }
  creatingFamily.value = true;
  try {
    const res = await store.createFamily({ name: familyName.value.trim() });
    if (res && res.id) {
      showSuccessToast('创建成功');
      showCreateFamily.value = false;
      familyName.value = '';
      await loadFamilyMembers();
      await store.loadFamilyData();   // 同步更新首页 Store
    }
  } catch (e) {
    showFailToast('创建失败');
  } finally {
    creatingFamily.value = false;
  }
};

const handleGenerateCode = async () => {
  if (!currentFamilyId.value) return;
  generatingCode.value = true;
  try {
    const res = await generateInviteCode(currentFamilyId.value);
    currentInviteCode.value = res.invite_code || '';
    if (currentInviteCode.value) {
      showSuccessToast('邀请码已生成');
    }
  } catch (e) {
    showFailToast('生成邀请码失败');
  } finally {
    generatingCode.value = false;
  }
};

const handleInviteByEmail = async () => {
  if (!inviteEmail.value.trim()) {
    showFailToast('请输入邮箱地址');
    return;
  }
  if (!currentFamilyId.value) {
    showFailToast('请先创建或加入家庭');
    return;
  }
  invitingMember.value = true;
  try {
    await inviteMember(currentFamilyId.value, { email: inviteEmail.value.trim() });
    showSuccessToast('邀请已发送');
    inviteEmail.value = '';
  } catch (e) {
    showFailToast('邀请发送失败');
  } finally {
    invitingMember.value = false;
  }
};

const handleJoinFamily = async () => {
  if (!joinCode.value.trim()) {
    showFailToast('请输入邀请码');
    return;
  }
  joiningFamily.value = true;
  try {
    const res = await joinFamily({ invite_code: joinCode.value.trim() });
    if (res && res.family_id) {
      showSuccessToast('加入成功');
      showJoinFamily.value = false;
      joinCode.value = '';
      await loadFamilyMembers();
      await store.loadFamilyData();   // 同步更新首页 Store 中的家庭成员
    }
  } catch (e) {
    showFailToast('加入失败，请检查邀请码');
  } finally {
    joiningFamily.value = false;
  }
};

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
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
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
  &--lilac {
    background: var(--ab-lilac-50);
    color: var(--ab-lilac-700);
    border: 1.5px solid var(--ab-lilac-200);
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

/* 弹窗通用样式 */
.modal-card {
  padding: 28px 24px;
}
.modal-card-title {
  text-align: center;
  font-size: 22px;
  font-weight: 700;
  color: var(--ab-text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 6px;
}
.modal-card-desc {
  text-align: center;
  font-size: 13px;
  color: var(--ab-text-tertiary);
  margin-bottom: 20px;
}
.modal-btn-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 4px;
}

/* 邀请码展示 */
.invite-code-display {
  background: var(--ab-brand-50);
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  margin-bottom: 16px;
}
.invite-code-label {
  font-size: 12px;
  color: var(--ab-text-tertiary);
  font-weight: 500;
}
.invite-code-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--ab-brand-600);
  letter-spacing: 0.08em;
  margin: 8px 0;
  font-family: monospace;
}
.invite-code-hint {
  font-size: 11px;
  color: var(--ab-text-tertiary);
}
.invite-divider {
  text-align: center;
  font-size: 12px;
  color: var(--ab-text-tertiary);
  margin: 16px 0;
  position: relative;
  &::before, &::after {
    content: '';
    position: absolute;
    top: 50%;
    width: calc(50% - 60px);
    height: 1px;
    background: var(--ab-border-medium);
  }
  &::before { left: 0; }
  &::after { right: 0; }
}

.logout-section {
  margin-top: var(--ab-space-4);
}
</style>
