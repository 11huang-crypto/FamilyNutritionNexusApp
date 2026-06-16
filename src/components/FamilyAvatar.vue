<template>
  <!--
    组件：FamilyAvatar 家庭成员头像组件
    用途：展示家庭成员头像，支持多种尺寸和状态
    Props:
      - member: 成员对象 { id, name, avatar, role?, color? }
      - size: 尺寸 'xs' | 'sm' | 'md' | 'lg' | 'xl'
      - showName: 是否显示名字
      - showRole: 是否显示角色标签
      - selectable: 是否可选择
      - selected: 是否被选中
      - stacked: 是否堆叠显示（用于群像）
      - index: 堆叠时的索引（控制z-index和偏移）
    Events:
      - click: 点击时触发
      - select: 选择/取消选择时触发
  -->
  <div
    class="family-avatar"
    :class="[
      `size-${size}`,
      { 'is-selectable': selectable, 'is-selected': selected, 'is-stacked': stacked, 'is-editable': editable }
    ]"
    :style="stackedStyle"
    @click="handleClick"
  >
    <!-- 头像图片 -->
    <div class="avatar-wrap">
      <!-- 自定义图片 -->
      <img
        v-if="member.avatar && !imgError"
        :src="member.avatar"
        :alt="member.name"
        class="avatar-img"
        loading="lazy"
        @error="imgError = true"
      />
      <!-- 首字母回退 -->
      <div v-else class="avatar-fallback" :style="fallbackStyle">
        {{ member.name ? member.name.charAt(0) : '?' }}
      </div>

      <!-- 在线/状态指示点 -->
      <span v-if="showStatus" class="status-dot" :class="statusClass"></span>

      <!-- 选中勾选 -->
      <div v-if="selected" class="selected-overlay">
        <van-icon name="success" size="14" color="#fff" />
      </div>

      <!-- 角色徽章 -->
      <div v-if="showRole && member.role === 'admin'" class="role-badge">
        <van-icon name="manager-o" size="10" />
      </div>

      <!-- 编辑按钮：点击换头像 -->
      <input
        v-if="editable"
        ref="fileInput"
        type="file"
        accept="image/*"
        class="file-input"
        @change="handleFileChange"
      />
      <div v-if="editable" class="edit-overlay" @click.stop="openFilePicker">
        <van-icon name="photo-o" size="14" color="#fff" />
      </div>
    </div>

    <!-- 名字 -->
    <span v-if="showName" class="avatar-name">{{ member.name }}</span>
  </div>
</template>

<script setup>
/**
 * FamilyAvatar - 家庭成员头像
 * 支持 SVG 头像、首字母回退、堆叠展示、选择模式、用户自定义上传
 */
import { ref, computed } from 'vue'

const props = defineProps({
  member: {
    type: Object,
    required: true,
    default: () => ({ name: '', avatar: '', role: 'member', color: '#22c55e' })
  },
  size: {
    type: String,
    default: 'md',
    validator: v => ['xs', 'sm', 'md', 'lg', 'xl'].includes(v)
  },
  showName: { type: Boolean, default: true },
  showRole: { type: Boolean, default: false },
  selectable: { type: Boolean, default: false },
  selected: { type: Boolean, default: false },
  stacked: { type: Boolean, default: false },
  index: { type: Number, default: 0 },
  status: { type: String, default: 'online' },
  /** 是否允许用户自行更换头像（显示拍照图标） */
  editable: { type: Boolean, default: false }
})

const emit = defineEmits(['click', 'select', 'avatar-change'])

const imgError = ref(false)
const fileInput = ref(null)

// 回退样式（使用成员颜色）
const fallbackStyle = computed(() => ({
  backgroundColor: props.member.color || '#22c55e',
  color: '#fff'
}))

// 堆叠样式
const stackedStyle = computed(() => {
  if (!props.stacked) return {}
  return {
    zIndex: 10 - props.index,
    marginLeft: props.index > 0 ? '-10px' : '0'
  }
})

// 状态显示
const showStatus = computed(() => props.status !== 'offline')
const statusClass = computed(() => `status-${props.status}`)

/** 触发文件选择器 */
const openFilePicker = () => {
  fileInput.value?.click()
}

/** 用户更换头像，转为 base64 并通过事件传出 */
const handleFileChange = (e) => {
  const file = e.target.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    emit('avatar-change', {
      memberId: props.member.id,
      dataUrl: reader.result
    })
    imgError.value = false
  }
  reader.readAsDataURL(file)

  // 重置 input 以便再次选择同一文件
  e.target.value = ''
}

const handleClick = () => {
  if (props.selectable) {
    emit('select', !props.selected)
  }
  emit('click', props.member)
}
</script>

<style scoped lang="scss">
.family-avatar {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: all var(--ab-transition-fast);

  &.is-selectable {
    cursor: pointer;
  }

  &.is-selected {
    .avatar-wrap {
      box-shadow: 0 0 0 3px var(--ab-primary-400);
    }
  }

  &.is-stacked {
    margin-left: -10px;

    &:first-child {
      margin-left: 0;
    }

    .avatar-wrap {
      border: 2px solid var(--ab-bg-card);
    }
  }

  &:active:not(.is-stacked) {
    transform: scale(0.95);
  }
}

.avatar-wrap {
  position: relative;
  flex-shrink: 0;
  border-radius: var(--ab-radius-full);
  overflow: hidden;
  transition: all var(--ab-transition-fast);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.avatar-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--ab-font-bold);
}

.avatar-name {
  font-size: var(--ab-text-xs);
  color: var(--ab-text-secondary);
  max-width: 60px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 状态指示点 */
.status-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 10px;
  height: 10px;
  border-radius: var(--ab-radius-full);
  border: 2px solid var(--ab-bg-card);

  &.status-online { background: var(--ab-success); }
  &.status-away { background: var(--ab-warning); }
  &.status-offline { background: var(--ab-gray-400); }
}

/* 选中遮罩 */
.selected-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(34, 197, 94, 0.7);
  border-radius: var(--ab-radius-full);
}

/* 编辑覆盖层：点击换头像 */
.file-input {
  display: none;
}

.edit-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0);
  border-radius: var(--ab-radius-full);
  transition: background var(--ab-transition-fast);
  cursor: pointer;
  opacity: 0;

  .avatar-wrap:hover & {
    background: rgba(0, 0, 0, 0.4);
    opacity: 1;
  }
}

/* 角色徽章 */
.role-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--ab-warning);
  color: #fff;
  border-radius: var(--ab-radius-full);
  border: 2px solid var(--ab-bg-card);
}

/* ========== 尺寸变体 ========== */
.size-xs {
  .avatar-wrap { width: 24px; height: 24px; }
  .avatar-fallback { font-size: 10px; }
  .avatar-name { display: none; }
  .status-dot { width: 8px; height: 8px; bottom: 0; right: 0; border-width: 1px; }
}

.size-sm {
  .avatar-wrap { width: 32px; height: 32px; }
  .avatar-fallback { font-size: 12px; }
  .avatar-name { font-size: 10px; max-width: 40px; }
  .status-dot { width: 9px; height: 9px; }
}

.size-md {
  .avatar-wrap { width: 40px; height: 40px; }
  .avatar-fallback { font-size: 14px; }
  .avatar-name { font-size: var(--ab-text-xs); max-width: 50px; }
}

.size-lg {
  .avatar-wrap { width: 48px; height: 48px; }
  .avatar-fallback { font-size: 16px; }
  .avatar-name { font-size: var(--ab-text-sm); max-width: 56px; }
}

.size-xl {
  .avatar-wrap { width: 64px; height: 64px; }
  .avatar-fallback { font-size: 20px; }
  .avatar-name { font-size: var(--ab-text-sm); max-width: 72px; }
}
</style>
