<template>
  <img
    :src="iconSrc"
    :class="['local-icon', { 'local-icon--active': active }]"
    :style="iconStyle"
    :alt="name"
    @click="$emit('click', $event)"
  />
</template>

<script setup>
import { computed, useAttrs } from 'vue'

// 用 import.meta.glob 一次性把所有 PNG 全部导入
// 编译时 Vite 会自动生成所有图标的 URL
const icons = import.meta.glob('../assets/icons/*.png', {
  eager: true,
  import: 'default',
})

// 文件名（不含扩展名） → URL
const iconMap = {}
for (const path in icons) {
  // path 形如 "../assets/icons/flower-o.png"
  const fileName = path.split('/').pop().replace(/\.png$/, '')
  iconMap[fileName] = icons[path]
}

// 别名映射：Codex 用的 van-icon 名字 → 实际 PNG 文件名
// （用于我们没有同名 PNG 的 Codex 专用图标）
const aliasMap = {
  'arrow': 'arrow-righ',            // arrow → arrow-righ（少个 t 的那个）
  'arrow-right': 'arrow-righ',
  'bell': 'info-o',                 // 通知铃铛 → 用 info-o 代替
  'lock': 'user-o',                 // 锁 → 用 user-o 代替
  'photograph': 'camera',           // 拍照图标 → 用 camera
  'envelop-o': 'message-o',         // 邮件 → 用 message-o
  'setting-o': 'info-o',            // 设置 → 用 info-o
  'delete-o': 'cross',              // 删除 → 用 cross
  'qr': 'wap-nav',                  // 二维码 → 用 wap-nav
  'app': 'apps-o',                  // 应用 → apps-o
  'checked': 'success',             // 勾选 → success
  'shopping-cart': 'shopping-cart-o', // 已激活购物车
  'camera-o': 'camera',             // 相机描边 → camera
  'home-o': 'wap-home-o',           // 首页 → wap-home-o
  'home': 'wap-home-o',             // 首页激活态 → wap-home-o
  'user-circle-o': 'user-o',        // 用户圆 → user-o
  'records': 'calendar-o',          // 记录 → calendar-o
  'completed': 'todo-list-o',       // 完成 → todo-list-o
}

// 合并：先用原名查，再用别名查
function resolveIcon(name) {
  if (iconMap[name]) return iconMap[name]
  if (aliasMap[name] && iconMap[aliasMap[name]]) return iconMap[aliasMap[name]]
  return null
}

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  // 兼容 van-icon 的 size 属性：'24'、'24px'、'0.5rem' 都行
  size: {
    type: [String, Number],
    default: '1em',
  },
  // 兼容 van-icon 的 color 属性（CSS color 值）
  color: {
    type: String,
    default: '',
  },
  // 激活态（Tabbar 切换、AlertBar 激活等）
  active: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['click'])

// 找图标，找不到就 fallback 到第一个（避免空白）
const iconSrc = computed(() => {
  return resolveIcon(props.name) || iconMap['inbox'] || ''
})

const iconStyle = computed(() => {
  // size 归一化（处理字符串纯数字、单位缺失等情况）
  const resolveSize = (s) => {
    if (typeof s === 'number') return `${s}px`
    const str = String(s).trim()
    if (!str) return '1em'
    if (/^-?\d+(\.\d+)?$/.test(str)) return `${str}px`
    return str
  }
  const w = resolveSize(props.size)
  const style = {
    width: w,
    height: w,
  }
  if (props.color) {
    // 染色：白名单颜色才用滤镜（避免非 hex 颜色被 brightness(0) 涂黑）
    const filterVal = cssColorToFilter(props.color)
    if (filterVal) {
      style.filter = filterVal
    }
    // 没匹配到的颜色 → 不染色，保持原色
  }
  return style
})

// 把 CSS 颜色转成 SVG 滤镜（粗暴但有效）
// 支持基础色，其他用 hue-rotate
function cssColorToFilter(color) {
  const colorMap = {
    '#1989fa': 'invert(34%) sepia(85%) saturate(2476%) hue-rotate(196deg) brightness(98%) contrast(97%)', // 蓝
    '#07c160': 'invert(46%) sepia(85%) saturate(1234%) hue-rotate(94deg) brightness(95%) contrast(101%)', // 绿
    '#ee0a24': 'invert(20%) sepia(95%) saturate(7460%) hue-rotate(354deg) brightness(95%) contrast(112%)', // 红
    '#ff976a': 'invert(64%) sepia(59%) saturate(498%) hue-rotate(338deg) brightness(101%) contrast(101%)', // 橙
    '#f5a623': 'invert(74%) sepia(38%) saturate(2000%) hue-rotate(0deg) brightness(102%) contrast(104%)', // 黄
    '#999': 'invert(67%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(95%) contrast(91%)', // 灰
    '#666': 'invert(43%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(94%) contrast(88%)',
    '#333': 'invert(20%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(94%) contrast(85%)',
  }
  return colorMap[color] || ''
}
</script>

<style scoped>
.local-icon {
  display: inline-block;
  vertical-align: middle;
  object-fit: contain;
  user-select: none;
  -webkit-user-drag: none;
  transition: filter 0.2s ease, transform 0.2s ease;
}

.local-icon--active {
  transform: scale(1.05);
}
</style>
