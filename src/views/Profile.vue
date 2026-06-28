<template>
  <div class="profile-page">
    <van-nav-bar title="个人中心" :showBack="false" />
    
    <div class="page-body">
      <div class="profile-header">
        <div class="avatar-wrap">
          <van-icon name="user" size="64" color="#fff" />
        </div>
        <div class="user-info">
          <h2 class="user-name">{{ userInfo.username }}</h2>
          <p class="user-email">{{ userInfo.email }}</p>
        </div>
      </div>

      <div class="section-card">
        <div class="section-title">
          <van-icon name="users" size="18" />
          <span>家庭成员</span>
        </div>
        <div class="family-members-list">
          <div v-for="member in familyMembers" :key="member.id" class="member-item">
            <div class="member-avatar">
              <van-icon name="user" size="24" color="#fff" />
            </div>
            <div class="member-info">
              <span class="member-name">{{ member.name }}</span>
              <span class="member-relation">{{ member.relation || '家庭成员' }}</span>
            </div>
          </div>
          <button v-if="!currentFamilyId" class="add-member-btn" @click="showCreateFamily = true">
            <van-icon name="plus" size="20" />
            <span>创建家庭</span>
          </button>
          <button class="add-member-btn" @click="showJoinFamily = true">
            <van-icon name="plus" size="20" />
            <span>加入家庭</span>
          </button>
          <button v-if="isAdmin" class="add-member-btn" @click="showInviteCode = true">
            <van-icon name="qr" size="20" />
            <span>邀请成员</span>
          </button>
        </div>
      </div>

      <div class="section-card">
        <div class="menu-list">
          <div class="menu-item" @click="$router.push('/basket')">
            <van-icon name="shopping-cart" size="20" color="#22c55e" />
            <span>我的菜篮子</span>
            <van-icon name="arrow" size="16" color="#999" />
          </div>
          <div class="menu-item" @click="$router.push('/meal-plan')">
            <van-icon name="calendar" size="20" color="#f97316" />
            <span>食谱推荐</span>
            <van-icon name="arrow" size="16" color="#999" />
          </div>
          <div class="menu-item" @click="$router.push('/shopping-list')">
            <van-icon name="list" size="20" color="#3b82f6" />
            <span>采购清单</span>
            <van-icon name="arrow" size="16" color="#999" />
          </div>
          <div class="menu-item" @click="$router.push('/family-health')">
            <van-icon name="heart" size="20" color="#ef4444" />
            <span>健康档案</span>
            <van-icon name="arrow" size="16" color="#999" />
          </div>
        </div>
      </div>

      <div class="section-card">
        <div class="menu-list">
          <div class="menu-item" @click="$router.push('/demo')">
            <van-icon name="app" size="20" color="#8b5cf6" />
            <span>组件展示</span>
            <van-icon name="arrow" size="16" color="#999" />
          </div>
        </div>
      </div>

      <div class="logout-section">
        <button class="logout-btn" @click="handleLogout">
          <van-icon name="arrow-left" size="18" />
          <span>退出登录</span>
        </button>
      </div>
    </div>

    <van-popup v-model:show="showCreateFamily" position="center" :style="{ width: '85%', borderRadius: '16px' }">
      <div class="add-member-modal">
        <h3 class="modal-title">创建家庭</h3>
        <van-form @submit="handleCreateFamily">
          <van-cell-group>
            <van-field
              v-model="familyName"
              name="name"
              label="家庭名称"
              placeholder="请输入家庭名称"
              :rules="[{ required: true, message: '请输入家庭名称' }]"
            />
          </van-cell-group>
          <div class="modal-button-group">
            <van-button round block type="primary" native-type="submit">
              创建
            </van-button>
            <van-button round block type="default" @click="showCreateFamily = false">
              取消
            </van-button>
          </div>
        </van-form>
      </div>
    </van-popup>

    <van-popup v-model:show="showJoinFamily" position="center" :style="{ width: '85%', borderRadius: '16px' }">
      <div class="add-member-modal">
        <h3 class="modal-title">加入家庭</h3>
        <van-form @submit="handleJoinFamily">
          <van-cell-group>
            <van-field
              v-model="inviteCode"
              name="invite_code"
              label="邀请码"
              placeholder="请输入6位邀请码"
              maxlength="6"
              :rules="[{ required: true, message: '请输入邀请码' }]"
            />
          </van-cell-group>
          <div class="modal-button-group">
            <van-button round block type="primary" native-type="submit">
              加入
            </van-button>
            <van-button round block type="default" @click="showJoinFamily = false">
              取消
            </van-button>
          </div>
        </van-form>
      </div>
    </van-popup>

    <van-popup v-model:show="showInviteCode" position="center" :style="{ width: '85%', borderRadius: '16px' }">
      <div class="add-member-modal">
        <h3 class="modal-title">邀请成员</h3>
        <div v-if="currentInviteCode" class="invite-code-section">
          <div class="invite-code-display">{{ currentInviteCode }}</div>
          <p class="invite-code-tip">邀请码有效期24小时</p>
          <van-button round block type="primary" @click="handleCopyCode">
            复制邀请码
          </van-button>
        </div>
        <div v-else>
          <van-button round block type="primary" @click="handleGenerateCode">
            生成邀请码
          </van-button>
        </div>
        <van-button round block type="default" @click="showInviteCode = false">
          关闭
        </van-button>
      </div>
    </van-popup>

    <!-- 底部导航栏 -->
    <AppTabbar :active="2" @change="handleTabChange" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores'
import AppTabbar from '@/components/AppTabbar.vue'
import axios from '@/utils/axios'
import { Toast } from 'vant'

const store = useAppStore()
const router = useRouter()

const userInfo = computed(() => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : { username: '用户', email: '' }
})

const familyMembers = ref([])
const isAdmin = ref(false)
const currentFamilyId = ref(null)
const currentInviteCode = ref('')

const showJoinFamily = ref(false)
const inviteCode = ref('')
const showInviteCode = ref(false)
const showCreateFamily = ref(false)
const familyName = ref('')

const handleLogout = () => {
  store.logout()
  router.push('/login')
}

const loadFamilyMembers = async () => {
  try {
    const response = await axios.get('/family/my')
    const families = response?.families || []
    if (families.length > 0) {
      const family = families[0]
      currentFamilyId.value = family.id
      isAdmin.value = family.role === 'admin'
      
      const membersResponse = await axios.get(`/family/${family.id}/members`)
      if (membersResponse && membersResponse.members) {
        familyMembers.value = membersResponse.members.map(m => ({
          id: m.user_id,
          name: m.username,
          relation: m.role === 'admin' ? '管理员' : '家庭成员'
        }))
      }
    }
  } catch (error) {
    console.error('加载家庭数据失败:', error)
  }
}

const handleCreateFamily = async () => {
  if (!familyName.value) {
    Toast.fail('请输入家庭名称')
    return
  }
  
  try {
    await axios.post('/family/create', { name: familyName.value })
    Toast.success('创建成功')
    showCreateFamily.value = false
    familyName.value = ''
    await loadFamilyMembers()
  } catch (error) {
    const msg = error.response?.data?.detail || '创建失败'
    Toast.fail(msg)
  }
}

const handleJoinFamily = async () => {
  if (!inviteCode.value) {
    Toast.fail('请输入邀请码')
    return
  }
  
  try {
    await axios.post('/family/join', null, {
      params: { invite_code: inviteCode.value }
    })
    showJoinFamily.value = false
    inviteCode.value = ''
    await loadFamilyMembers()
    setTimeout(() => {
      Toast.success('加入成功')
    }, 100)
  } catch (error) {
    const msg = error.response?.data?.detail || '加入失败'
    Toast.fail(msg)
  }
}

const handleGenerateCode = async () => {
  if (!currentFamilyId.value) {
    Toast.fail('请先创建或加入家庭')
    return
  }
  
  try {
    const response = await axios.post(`/family/${currentFamilyId.value}/generate-code`)
    currentInviteCode.value = response.invite_code
    Toast.success('邀请码已生成')
  } catch (error) {
    const msg = error.response?.data?.detail || '生成失败'
    Toast.fail(msg)
  }
}

const handleCopyCode = async () => {
  try {
    await navigator.clipboard.writeText(currentInviteCode.value)
    Toast.success('已复制到剪贴板')
  } catch (error) {
    Toast.fail('复制失败')
  }
}

const handleTabChange = (index, item) => {
  if (item.path) {
    router.push(item.path)
  }
}

onMounted(() => {
  loadFamilyMembers()
})
</script>

<style scoped lang="scss">
.profile-page {
  min-height: 100vh;
  background: var(--ab-bg-page);
}

.page-body {
  padding: var(--ab-space-4);
  padding-bottom: 80px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: var(--ab-space-4);
  background: linear-gradient(135deg, var(--ab-primary-500) 0%, var(--ab-primary-600) 100%);
  border-radius: var(--ab-radius-xl);
  padding: var(--ab-space-6);
  margin-bottom: var(--ab-space-4);
  color: #fff;
}

.avatar-wrap {
  width: 72px;
  height: 72px;
  border-radius: var(--ab-radius-full);
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: var(--ab-text-xl);
  font-weight: var(--ab-font-bold);
  margin-bottom: var(--ab-space-1);
}

.user-email {
  font-size: var(--ab-text-sm);
  opacity: 0.8;
}

.section-card {
  background: var(--ab-bg-card);
  border-radius: var(--ab-radius-lg);
  padding: var(--ab-space-4);
  margin-bottom: var(--ab-space-4);
  box-shadow: var(--ab-shadow-sm);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--ab-space-2);
  font-size: var(--ab-text-base);
  font-weight: var(--ab-font-bold);
  color: var(--ab-text-primary);
  margin-bottom: var(--ab-space-3);
  padding-bottom: var(--ab-space-2);
  border-bottom: 1px solid var(--ab-border-light);
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
}

.member-avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--ab-radius-full);
  background: var(--ab-primary-100);
  display: flex;
  align-items: center;
  justify-content: center;
}

.member-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.member-name {
  font-size: var(--ab-text-base);
  font-weight: var(--ab-font-medium);
  color: var(--ab-text-primary);
}

.member-relation {
  font-size: var(--ab-text-xs);
  color: var(--ab-text-tertiary);
}

.add-member-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--ab-space-2);
  padding: var(--ab-space-3);
  border: 2px dashed var(--ab-border);
  border-radius: var(--ab-radius-md);
  background: transparent;
  color: var(--ab-text-tertiary);
  font-size: var(--ab-text-sm);
  cursor: pointer;
  transition: all var(--ab-transition-fast);

  &:active {
    background: var(--ab-primary-50);
    border-color: var(--ab-primary-300);
    color: var(--ab-primary-600);
  }
}

.menu-list {
  display: flex;
  flex-direction: column;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: var(--ab-space-3);
  padding: var(--ab-space-4) 0;
  border-bottom: 1px solid var(--ab-border-light);
  cursor: pointer;
  transition: background var(--ab-transition-fast);

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background: var(--ab-bg-surface);
  }

  span {
    flex: 1;
    font-size: var(--ab-text-base);
    color: var(--ab-text-primary);
  }
}

.logout-section {
  margin-top: var(--ab-space-6);
}

.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--ab-space-2);
  width: 100%;
  padding: var(--ab-space-4);
  border: 1px solid var(--ab-danger);
  border-radius: var(--ab-radius-md);
  background: transparent;
  color: var(--ab-danger);
  font-size: var(--ab-text-base);
  font-weight: var(--ab-font-medium);
  cursor: pointer;
  transition: all var(--ab-transition-fast);

  &:active {
    background: var(--ab-danger-light);
  }
}

.add-member-modal {
  padding: var(--ab-space-4);
}

.modal-title {
  font-size: var(--ab-text-xl);
  font-weight: var(--ab-font-bold);
  text-align: center;
  margin-bottom: var(--ab-space-4);
  color: var(--ab-text-primary);
}

.modal-button-group {
  display: flex;
  flex-direction: column;
  gap: var(--ab-space-3);
  margin-top: var(--ab-space-4);
}

.invite-code-section {
  text-align: center;
  padding: var(--ab-space-4);
}

.invite-code-display {
  font-size: 48px;
  font-weight: bold;
  letter-spacing: 8px;
  color: var(--ab-primary-600);
  margin-bottom: var(--ab-space-3);
  font-family: monospace;
}

.invite-code-tip {
  font-size: var(--ab-text-sm);
  color: var(--ab-text-tertiary);
  margin-bottom: var(--ab-space-4);
}
</style>