<template>
  <div class="family-health-page">
    <van-nav-bar title="家庭健康档案" left-arrow @click-left="goBack" />

    <div class="page-body">
      <div class="stats-card">
        <div class="stat-item">
          <van-icon name="users" size="24" color="#3b82f6" />
          <span class="stat-count">{{ profiles.length }}</span>
          <span class="stat-label">已建档成员</span>
        </div>
        <div class="stat-item">
          <van-icon name="alert-circle-o" size="24" color="#ef4444" />
          <span class="stat-count">{{ totalAllergies }}</span>
          <span class="stat-label">过敏记录</span>
        </div>
        <div class="stat-item">
          <van-icon name="heart-o" size="24" color="#f97316" />
          <span class="stat-count">{{ totalConditions }}</span>
          <span class="stat-label">健康状况</span>
        </div>
      </div>

      <div class="section-header">
        <span class="section-title">家庭成员健康档案</span>
        <van-button type="primary" size="small" @click="handleAddMember">
          <van-icon name="plus" />
          添加成员
        </van-button>
      </div>

      <div class="profiles-list">
        <div 
          v-for="profile in profiles" 
          :key="profile.id" 
          class="profile-card"
          @click="editProfile(profile)"
        >
          <div class="profile-header">
            <div class="avatar-wrapper">
              <van-icon name="user" size="28" color="#fff" />
            </div>
            <div class="profile-info">
              <span class="profile-name">{{ profile.name }}</span>
              <span class="profile-meta">ID: {{ profile.user_id || '-' }}</span>
            </div>
            <van-icon name="arrow" size="16" color="#999" />
          </div>
          
          <div class="profile-details">
            <div v-if="profile.allergens && profile.allergens.length > 0" class="detail-row">
              <van-icon name="alert-circle-o" size="14" color="#ef4444" />
              <span class="detail-label">过敏:</span>
              <span class="detail-value danger">{{ profile.allergens.join('、') }}</span>
            </div>
            <div v-if="profile.conditions && profile.conditions.length > 0" class="detail-row">
              <van-icon name="heart-o" size="14" color="#f97316" />
              <span class="detail-label">状况:</span>
              <span class="detail-value warning">{{ profile.conditions.join('、') }}</span>
            </div>
            <div v-if="profile.taboos && profile.taboos.length > 0" class="detail-row">
              <van-icon name="forbidden" size="14" color="#8b5cf6" />
              <span class="detail-label">忌口:</span>
              <span class="detail-value purple">{{ profile.taboos.join('、') }}</span>
            </div>
            <div v-if="!profile.allergens.length && !profile.conditions.length && !profile.taboos.length" class="detail-row">
              <van-icon name="check-circle-o" size="14" color="#22c55e" />
              <span class="detail-value success">健康状况良好</span>
            </div>
          </div>

          <div class="profile-actions">
            <van-button type="default" size="mini" @click.stop="editProfile(profile)">编辑</van-button>
            <van-button type="danger" size="mini" @click.stop="deleteProfile(profile.id)">删除</van-button>
          </div>
        </div>
      </div>

      <div v-if="profiles.length === 0" class="empty-state">
        <van-icon name="heart-o" size="48" color="#ccc" />
        <p>暂无健康档案</p>
        <van-button type="primary" @click="showAddModal = true">添加第一个成员</van-button>
      </div>
    </div>

    <van-popup v-model:show="showAddModal" position="bottom" :style="{ height: '85%' }">
      <div class="modal-header">
        <span>{{ editingProfile ? '编辑健康档案' : '添加健康档案' }}</span>
        <van-icon name="close" size="20" @click="showAddModal = false" />
      </div>
      
      <div class="modal-body">
        <van-form @submit="submitProfile">
          <van-cell-group>
            <van-field 
              v-model="formName" 
              label="姓名" 
              placeholder="请输入成员姓名"
              required
            />
            
            <div class="form-section">
              <span class="section-label">过敏史</span>
              <div class="tags-container">
                <span 
                  v-for="(allergen, index) in formAllergens" 
                  :key="index" 
                  class="custom-tag"
                >
                  {{ allergen }}
                  <span class="tag-close" @click.stop="removeAllergen(index)">×</span>
                </span>
              </div>
              <div class="add-tag-row">
                <van-field 
                  v-model="newAllergen" 
                  placeholder="输入过敏原"
                  size="small"
                />
                <van-button type="primary" size="small" @click="addAllergen">添加</van-button>
              </div>
            </div>

            <div class="form-section">
              <span class="section-label">慢性疾病</span>
              <div class="tags-container">
                <span 
                  v-for="(condition, index) in formConditions" 
                  :key="index" 
                  class="custom-tag"
                >
                  {{ condition }}
                  <span class="tag-close" @click.stop="removeCondition(index)">×</span>
                </span>
              </div>
              <div class="add-tag-row">
                <van-field 
                  v-model="newCondition" 
                  placeholder="输入疾病名称"
                  size="small"
                />
                <van-button type="primary" size="small" @click="addCondition">添加</van-button>
              </div>
            </div>

            <div class="form-section">
              <span class="section-label">忌口</span>
              <div class="tags-container">
                <span 
                  v-for="(taboo, index) in formTaboos" 
                  :key="index" 
                  class="custom-tag"
                >
                  {{ taboo }}
                  <span class="tag-close" @click.stop="removeTaboo(index)">×</span>
                </span>
              </div>
              <div class="add-tag-row">
                <van-field 
                  v-model="newTaboo" 
                  placeholder="输入忌口食物"
                  size="small"
                />
                <van-button type="primary" size="small" @click="addTaboo">添加</van-button>
              </div>
            </div>
          </van-cell-group>

          <div class="modal-actions">
            <van-button type="default" block @click="showAddModal = false">取消</van-button>
            <van-button type="primary" native-type="submit" block :loading="submitting">
              {{ editingProfile ? '保存修改' : '保存档案' }}
            </van-button>
          </div>
        </van-form>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';
import { getHealthProfiles, addHealthProfile, updateHealthProfile, deleteHealthProfile } from '../api';

const router = useRouter();

const profiles = ref([]);
const showAddModal = ref(false);
const submitting = ref(false);
const editingProfile = ref(null);
const family_id = ref(null);

const formName = ref('');
const formAllergens = ref([]);
const formConditions = ref([]);
const formTaboos = ref([]);

const newAllergen = ref('');
const newCondition = ref('');
const newTaboo = ref('');

const totalAllergies = computed(() => {
  return profiles.value.reduce((sum, p) => sum + (p.allergens?.length || 0), 0);
});

const totalConditions = computed(() => {
  return profiles.value.reduce((sum, p) => sum + (p.conditions?.length || 0), 0);
});

const goBack = () => {
  router.back();
};

const getFamilyId = () => {
  const storedId = localStorage.getItem('family_id');
  if (storedId) {
    family_id.value = parseInt(storedId);
    return true;
  }
  return false;
};

const fetchHealthProfiles = async () => {
  if (!family_id.value) {
    showToast({ type: 'warning', message: '请先加入或创建家庭' });
    return;
  }

  try {
    const response = await getHealthProfiles(family_id.value);
    console.log('DEBUG: fetchHealthProfiles response:', response);
    const profilesData = response.profiles || response;
    profiles.value = Array.isArray(profilesData) ? profilesData : [];
    console.log('DEBUG: profiles.value updated:', profiles.value);
  } catch (error) {
    console.error('获取健康档案失败:', error);
    showToast({ type: 'fail', message: '获取健康档案失败' });
    profiles.value = [];
  }
};

const resetForm = () => {
  formName.value = '';
  formAllergens.value = [];
  formConditions.value = [];
  formTaboos.value = [];
  newAllergen.value = '';
  newCondition.value = '';
  newTaboo.value = '';
  editingProfile.value = null;
};

const handleAddMember = () => {
  resetForm();
  showAddModal.value = true;
};

const editProfile = (profile) => {
  editingProfile.value = profile;
  formName.value = profile.name;
  formAllergens.value = [...(profile.allergens || [])];
  formConditions.value = [...(profile.conditions || [])];
  formTaboos.value = [...(profile.taboos || [])];
  showAddModal.value = true;
};

const addAllergen = () => {
  const value = newAllergen.value.trim();
  if (value && !formAllergens.value.includes(value)) {
    formAllergens.value.push(value);
    newAllergen.value = '';
  }
};

const removeAllergen = (index) => {
  formAllergens.value.splice(index, 1);
};

const addCondition = () => {
  const value = newCondition.value.trim();
  if (value && !formConditions.value.includes(value)) {
    formConditions.value.push(value);
    newCondition.value = '';
  }
};

const removeCondition = (index) => {
  formConditions.value.splice(index, 1);
};

const addTaboo = () => {
  const value = newTaboo.value.trim();
  if (value && !formTaboos.value.includes(value)) {
    formTaboos.value.push(value);
    newTaboo.value = '';
  }
};

const removeTaboo = (index) => {
  formTaboos.value.splice(index, 1);
};

const submitProfile = async () => {
  if (!formName.value.trim()) {
    showToast({ type: 'fail', message: '请输入成员姓名' });
    return;
  }

  console.log('DEBUG: submitProfile called');
  console.log('DEBUG: form data:', JSON.stringify({
    name: formName.value,
    conditions: formConditions.value,
    allergens: formAllergens.value,
    taboos: formTaboos.value
  }));

  try {
    submitting.value = true;
    
    let data;
    if (editingProfile.value) {
      data = {
        name: formName.value,
        conditions: formConditions.value,
        allergens: formAllergens.value,
        taboos: formTaboos.value
      };
    } else {
      data = {
        family_id: family_id.value,
        name: formName.value,
        conditions: formConditions.value,
        allergens: formAllergens.value,
        taboos: formTaboos.value
      };
    }

    if (editingProfile.value) {
      await updateHealthProfile(editingProfile.value.id, data);
      showToast({ type: 'success', message: '更新成功' });
    } else {
      await addHealthProfile(data);
      showToast({ type: 'success', message: '添加成功' });
    }

    showAddModal.value = false;
    resetForm();
    await fetchHealthProfiles();
  } catch (error) {
    console.error('保存健康档案失败:', error);
    showToast({ type: 'fail', message: '保存失败' });
  } finally {
    submitting.value = false;
  }
};

const deleteProfile = async (id) => {
  try {
    await deleteHealthProfile(id);
    profiles.value = profiles.value.filter(p => p.id !== id);
    showToast({ type: 'success', message: '删除成功' });
  } catch (error) {
    console.error('删除健康档案失败:', error);
    showToast({ type: 'fail', message: '删除失败' });
  }
};

onMounted(() => {
  getFamilyId();
  fetchHealthProfiles();
});
</script>

<style lang="scss" scoped>
.family-health-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
}

.page-body {
  flex: 1;
  padding: 16px;
  padding-bottom: 20px;
}

.stats-card {
  display: flex;
  justify-content: space-around;
  background: #fff;
  border-radius: 12px;
  padding: 20px 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;

    .stat-count {
      font-size: 24px;
      font-weight: bold;
      color: #333;
    }

    .stat-label {
      font-size: 12px;
      color: #999;
    }
  }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;

  .section-title {
    font-size: 16px;
    font-weight: bold;
    color: #333;
  }
}

.profiles-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.profile-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  transition: all 0.3s ease;

  &:active {
    transform: scale(0.98);
  }

  .profile-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;

    .avatar-wrapper {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .profile-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2px;

      .profile-name {
        font-size: 16px;
        font-weight: 600;
        color: #333;
      }

      .profile-meta {
        font-size: 12px;
        color: #999;
      }
    }
  }

  .profile-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding-left: 56px;
    margin-bottom: 12px;

    .detail-row {
      display: flex;
      align-items: center;
      gap: 6px;

      .detail-label {
        font-size: 13px;
        color: #666;
      }

      .detail-value {
        font-size: 13px;

        &.danger {
          color: #ef4444;
        }

        &.warning {
          color: #f97316;
        }

        &.purple {
          color: #8b5cf6;
        }

        &.success {
          color: #22c55e;
        }
      }
    }
  }

  .profile-actions {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
    padding-left: 56px;

    .van-button {
      min-width: 60px;
    }
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #999;

  p {
    margin: 12px 0 24px;
    font-size: 14px;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #eee;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.modal-body {
  padding: 16px;
  height: calc(100% - 52px);
  overflow-y: auto;
}

.form-section {
    margin-bottom: 16px;

    .section-label {
      display: block;
      font-size: 14px;
      font-weight: 600;
      color: #333;
      margin-bottom: 8px;
    }

    .tags-container {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .custom-tag {
      display: inline-flex;
      align-items: center;
      padding: 4px 10px;
      background-color: #fff;
      border: 1px solid #ebedf0;
      border-radius: 4px;
      font-size: 13px;
      color: #646566;
      position: relative;

      .tag-close {
        margin-left: 6px;
        color: #999;
        font-size: 16px;
        cursor: pointer;
        line-height: 1;

        &:hover {
          color: #ff4d4f;
        }
      }
    }
  }

.add-tag-row {
  display: flex;
  gap: 8px;
  margin-top: 8px;

  .van-field {
    flex: 1;
  }
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;

  .van-button {
    flex: 1;
    height: 44px;
  }
}
</style>
