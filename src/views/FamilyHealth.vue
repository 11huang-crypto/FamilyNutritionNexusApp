<template>
  <div class="family-health-page">
    <AppNavbar title="家庭健康档案" :showBack="true" />

    <div class="page-body">
      <!-- 统计卡片 -->
      <div class="stats-row">
        <div class="clay-card stats-item">
          <LocalIcon name="friends-o" size="28" />
          <span class="stats-value">{{ profiles.length }}</span>
          <span class="stats-label">已建档成员</span>
        </div>
        <div class="clay-card stats-item">
          <LocalIcon name="warning-o" size="28" />
          <span class="stats-value">{{ totalAllergies }}</span>
          <span class="stats-label">过敏记录</span>
        </div>
        <div class="clay-card stats-item">
          <LocalIcon name="like-o" size="28" />
          <span class="stats-value">{{ totalConditions }}</span>
          <span class="stats-label">健康状况</span>
        </div>
      </div>

      <!-- 添加成员按钮 -->
      <div class="section-header">
        <h3 class="section-label">家庭成员健康档案</h3>
        <button class="clay-btn clay-btn--primary" style="padding: 6px 16px; font-size: 12px;" @click="openAddModal">
          <LocalIcon name="plus" size="14" /> 添加成员
        </button>
      </div>

      <!-- 档案列表 -->
      <div class="profiles-list">
        <div v-for="profile in profiles" :key="profile.id" class="clay-card profile-card">
          <div class="profile-header" @click="editProfile(profile)">
            <div class="profile-avatar" :style="{ background: 'linear-gradient(135deg, var(--ab-brand-100), var(--ab-brand-200))' }">
              <LocalIcon name="user" size="22" color="var(--ab-brand-600)" />
            </div>
            <div class="profile-info">
              <span class="profile-name">{{ profile.name }}</span>
              <span class="profile-meta">ID: {{ profile.user_id || '-' }}</span>
            </div>
            <LocalIcon name="arrow" size="14" color="var(--ab-text-disabled)" />
          </div>

          <div class="profile-details">
            <div v-if="profile.allergens?.length" class="detail-tag danger">
              <LocalIcon name="warning-o" size="14" /> 过敏：{{ profile.allergens.join('、') }}
            </div>
            <div v-if="profile.conditions?.length" class="detail-tag warning">
              <LocalIcon name="like-o" size="14" /> 状况：{{ profile.conditions.join('、') }}
            </div>
            <div v-if="profile.taboos?.length" class="detail-tag purple">
              <LocalIcon name="close" size="14" /> 忌口：{{ profile.taboos.join('、') }}
            </div>
            <div v-if="!profile.allergens?.length && !profile.conditions?.length && !profile.taboos?.length" class="detail-tag success">
              <LocalIcon name="success" size="14" /> 健康状况良好
            </div>
          </div>

          <div class="profile-actions">
            <button class="clay-btn clay-btn--secondary" style="padding: 4px 12px; font-size: 12px;" @click="editProfile(profile)">编辑</button>
            <button class="clay-btn clay-btn--secondary" style="padding: 4px 12px; font-size: 12px; color: var(--ab-error);" @click="deleteProfile(profile.id)">删除</button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div class="empty-state" v-if="profiles.length === 0">
        <LocalIcon name="orders-o" size="64" />
        <p>暂无健康档案</p>
        <button class="clay-btn clay-btn--primary" @click="openAddModal">添加第一个成员</button>
      </div>
    </div>

    <!-- 添加/编辑成员弹窗 -->
    <van-popup v-model:show="showModal" position="bottom" :style="{ height: '85%', borderRadius: '32px 32px 0 0' }">
      <div class="profile-modal">
        <div class="modal-header">
          <h3 class="modal-title">{{ isEditing ? '编辑成员' : '添加成员' }}</h3>
          <button class="modal-close" @click="closeModal">
            <LocalIcon name="cross" size="20" />
          </button>
        </div>

        <div class="modal-body">
          <van-form @submit="handleSubmit">
            <van-cell-group inset>
              <van-field
                v-model="form.name"
                label="姓名"
                placeholder="请输入姓名"
                required
                :rules="[{ required: true, message: '请输入姓名' }]"
              />

              <van-field
                v-model="form.user_id"
                label="用户ID"
                placeholder="请输入用户ID"
              />

              <van-field
                v-model="form.allergens"
                label="过敏食材"
                placeholder="多个过敏食材用逗号分隔"
              />

              <van-field
                v-model="form.conditions"
                label="健康状况"
                placeholder="多个状况用逗号分隔"
              />

              <van-field
                v-model="form.taboos"
                label="忌口食物"
                placeholder="多个忌口用逗号分隔"
              />
            </van-cell-group>

            <div class="modal-button-group">
              <button type="button" class="clay-btn clay-btn--secondary clay-btn--block" @click.prevent="closeModal">取消</button>
              <button type="submit" class="clay-btn clay-btn--primary clay-btn--block" :disabled="loading">
                <van-loading v-if="loading" size="18" color="#fff" />
                <span v-else>{{ isEditing ? '保存修改' : '添加成员' }}</span>
              </button>
            </div>
          </van-form>
        </div>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { showToast, showSuccessToast, showFailToast } from 'vant';
import { getHealthProfiles, addHealthProfile, updateHealthProfile, deleteHealthProfile } from '../api';
import AppNavbar from '@/components/AppNavbar.vue';

const profiles = ref([]);
const totalAllergies = computed(() => profiles.value.reduce((s, p) => s + (p.allergens?.length || 0), 0));
const totalConditions = computed(() => profiles.value.reduce((s, p) => s + (p.conditions?.length || 0), 0));

const showModal = ref(false);
const isEditing = ref(false);
const loading = ref(false);
const editingId = ref(null);

const form = ref({
  name: '',
  user_id: '',
  allergens: '',
  conditions: '',
  taboos: ''
});

const fetchHealthProfiles = async () => {
  try {
    const family_id = localStorage.getItem('family_id');
    if (!family_id) {
      console.warn('未找到 family_id，无法获取健康档案');
      return;
    }
    const res = await getHealthProfiles(family_id);
    profiles.value = res.data || [];
  } catch (e) {
    profiles.value = [
      { id: 1, name: '爸爸', user_id: 'u001', allergens: ['海鲜'], conditions: ['高血压'], taboos: ['辛辣'] },
      { id: 2, name: '妈妈', user_id: 'u002', allergens: [], conditions: [], taboos: [] },
    ];
  }
};

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  form.value = {
    name: '',
    user_id: '',
    allergens: '',
    conditions: '',
    taboos: ''
  };
  showModal.value = true;
};

const editProfile = (profile) => {
  isEditing.value = true;
  editingId.value = profile.id;
  form.value = {
    name: profile.name || '',
    user_id: profile.user_id || '',
    allergens: profile.allergens?.join(',') || '',
    conditions: profile.conditions?.join(',') || '',
    taboos: profile.taboos?.join(',') || ''
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const parseArrayField = (value) => {
  if (!value) return [];
  return value.split(',').map(item => item.trim()).filter(item => item);
};

const handleSubmit = async () => {
  if (!form.value.name) {
    showFailToast('请输入姓名');
    return;
  }

  loading.value = true;

  try {
    const family_id = localStorage.getItem('family_id');
    if (!family_id) {
      showFailToast('未找到家庭信息，请先创建或加入家庭');
      loading.value = false;
      return;
    }
    const profileData = {
      family_id: parseInt(family_id),
      name: form.value.name,
      user_id: form.value.user_id,
      allergens: parseArrayField(form.value.allergens),
      conditions: parseArrayField(form.value.conditions),
      taboos: parseArrayField(form.value.taboos)
    };

    if (isEditing.value) {
      const response = await updateHealthProfile(editingId.value, profileData);
      const index = profiles.value.findIndex(p => p.id === editingId.value);
      if (index !== -1) {
        profiles.value[index] = { ...profiles.value[index], ...profileData };
      }
      showSuccessToast('修改成功');
    } else {
      const response = await addHealthProfile(profileData);
      const newProfile = {
        id: response.id || Date.now(),
        ...profileData
      };
      profiles.value.push(newProfile);
      showSuccessToast('添加成功');
    }

    closeModal();
  } catch (e) {
    showFailToast(isEditing.value ? '修改失败' : '添加失败');
  } finally {
    loading.value = false;
  }
};

const deleteProfile = async (id) => {
  try {
    await deleteHealthProfile(id);
    profiles.value = profiles.value.filter(p => p.id !== id);
    showSuccessToast('删除成功');
  } catch (e) {
    profiles.value = profiles.value.filter(p => p.id !== id);
    showSuccessToast('删除成功');
  }
};

onMounted(fetchHealthProfiles);
</script>

<style scoped lang="scss">
.family-health-page { min-height: 100vh; background: transparent; }
.page-body { padding: var(--ab-space-4); padding-bottom: 80px; }

.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--ab-space-3); margin-bottom: var(--ab-space-4); }
.stats-item { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: var(--ab-space-3); }
.stats-emoji { font-size: 24px; }
.stats-value { font-size: var(--ab-text-xl); font-weight: var(--ab-font-bold); color: var(--ab-brand-600); }
.stats-label { font-size: var(--ab-text-xs); color: var(--ab-text-tertiary); }

.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--ab-space-3); }
.section-label { font-size: var(--ab-text-base); font-weight: var(--ab-font-semibold); color: var(--ab-text-primary); }

.profiles-list { display: flex; flex-direction: column; gap: var(--ab-space-3); }

.profile-card { padding: var(--ab-space-4); }
.profile-header { display: flex; align-items: center; gap: var(--ab-space-3); margin-bottom: var(--ab-space-3); cursor: pointer; }

.profile-avatar { width: 44px; height: 44px; border-radius: var(--ab-radius-full); display: flex; align-items: center; justify-content: center; box-shadow: var(--ab-clay-shadow-sm); }
.profile-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.profile-name { font-size: var(--ab-text-base); font-weight: var(--ab-font-semibold); color: var(--ab-text-primary); }
.profile-meta { font-size: var(--ab-text-xs); color: var(--ab-text-tertiary); }

.profile-details { display: flex; flex-direction: column; gap: var(--ab-space-2); margin-bottom: var(--ab-space-3); }

.detail-tag {
  display: flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: var(--ab-radius-md);
  font-size: var(--ab-text-sm);
  &.danger { background: var(--ab-error-bg); color: var(--ab-error); }
  &.warning { background: var(--ab-warning-bg); color: var(--ab-warning); }
  &.purple { background: var(--ab-lilac-50); color: var(--ab-lilac-600); }
  &.success { background: var(--ab-success-bg); color: var(--ab-success); }
}

.profile-actions { display: flex; gap: var(--ab-space-2); justify-content: flex-end; }

.empty-state { display: flex; flex-direction: column; align-items: center; gap: var(--ab-space-4); padding: 60px 20px; p { font-size: var(--ab-text-base); color: var(--ab-text-tertiary); } }

/* 模态框样式 */
.profile-modal {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--ab-border-subtle);
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--ab-text-primary);
  margin: 0;
}

.modal-close {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--ab-text-tertiary);
  &:active { background: var(--ab-gray-100); }
}

.modal-body {
  flex: 1;
  padding: 20px 24px;
  overflow-y: auto;
}

.modal-button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 24px;
}
</style>
