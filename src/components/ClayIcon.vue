<template>
  <div
    class="clay-icon"
    :class="[`clay-icon--${color}`, sizeClass, { 'clay-icon--pulse': pulse }]"
  >
    <slot />
  </div>
</template>

<style scoped lang="scss">
/* LocalIcon 子元素（PNG）撑满容器 75%（你要的"占边框 70~80%"） */
.clay-icon :slotted(.local-icon) {
  width: 75% !important;
  height: 75% !important;
  object-fit: contain;
}
</style>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  color: {
    type: String,
    default: 'brand',
    validator: v => [
      'brand', 'peach', 'blue', 'mint', 'lilac', 'orange',
      'pink', 'yellow', 'gray',
      // 浅色变体
      'soft-brand', 'soft-peach', 'soft-blue', 'soft-mint',
      'soft-lilac', 'soft-orange', 'soft-pink', 'soft-yellow', 'soft-gray'
    ].includes(v)
  },
  size: {
    type: String,
    default: 'md',
    validator: v => ['xs', 'sm', 'md', 'lg', 'xl'].includes(v)
  },
  pulse: { type: Boolean, default: false }
})

const sizeClass = computed(() => {
  if (props.size === 'xs') return 'clay-icon--xs'
  if (props.size === 'sm') return 'clay-icon--sm'
  if (props.size === 'lg') return 'clay-icon--lg'
  if (props.size === 'xl') return 'clay-icon--xl'
  return 'clay-icon--md'
})
</script>
