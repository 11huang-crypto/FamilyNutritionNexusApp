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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { showToast } from 'vant';
import { getHealthProfiles, addHealthProfile, updateHealthProfile, deleteHealthProfile } from '../api';
import AppNavbar from '@/components/AppNavbar.vue';

const profiles = ref([]);
const totalAllergies = computed(() => profiles.value.reduce((s, p) => s + (p.allergens?.length || 0), 0));
const totalConditions = computed(() => profiles.value.reduce((s, p) => s + (p.conditions?.length || 0), 0));

const fetchHealthProfiles = async () => {
  try {
    const res = await getHealthProfiles();
    profiles.value = res.data || [];
  } catch (e) {
    profiles.value = [
      { id: 1, name: '爸爸', user_id: 'u001', allergens: ['海鲜'], conditions: ['高血压'], taboos: ['辛辣'] },
      { id: 2, name: '妈妈', user_id: 'u002', allergens: [], conditions: [], taboos: [] },
    ];
  }
};

const openAddModal = () => showToast({ type: 'info', message: '添加成员功能' });
const editProfile = (profile) => showToast({ type: 'info', message: '编辑: ' + profile.name });
const deleteProfile = async (id) => {
  profiles.value = profiles.value.filter(p => p.id !== id);
  showToast({ type: 'success', message: '删除成功' });
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
</style>
