<template>
  <div class="login-page">
    <!-- 背景光斑：Mintlify 风的渐变光晕 -->
    <div class="bg-deco">
      <div class="bg-blob bg-blob--1"></div>
      <div class="bg-blob bg-blob--2"></div>
      <div class="bg-blob bg-blob--3"></div>
    </div>

    <div class="login-container">
      <!-- Logo 区域 -->
      <div class="logo-section">
        <div class="logo-clay">
          <span class="logo-emoji">🥬</span>
        </div>
        <h1 class="app-title">AI 智能菜篮子</h1>
        <p class="app-subtitle">让健康饮食更简单</p>
      </div>

      <!-- 登录/注册 Tabs -->
      <div class="tabs-pill">
        <button
          v-for="tab in tabs"
          :key="tab.name"
          class="tab-trigger"
          :class="{ 'is-active': activeTab === tab.name }"
          @click="activeTab = tab.name"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- 登录表单 -->
      <div v-if="activeTab === 'login'" class="form-pane">
        <div class="clay-input">
          <span class="clay-input__prefix">
            <ClayIcon color="soft-brand" size="sm">
              <LocalIcon name="user-o" size="16" color="var(--ab-brand-600)" />
            </ClayIcon>
          </span>
          <input
            v-model="loginForm.username"
            type="text"
            placeholder="请输入用户名或邮箱"
            @keyup.enter="handleLogin"
          />
        </div>
        <div class="clay-input">
          <span class="clay-input__prefix">
            <ClayIcon color="soft-brand" size="sm">
              <LocalIcon name="lock" size="16" color="var(--ab-brand-600)" />
            </ClayIcon>
          </span>
          <input
            v-model="loginForm.password"
            :type="showPwd ? 'text' : 'password'"
            placeholder="请输入密码"
            @keyup.enter="handleLogin"
          />
          <span class="clay-input__suffix" @click="showPwd = !showPwd">
            <LocalIcon :name="showPwd ? 'eye-o' : 'closed-eye'" size="20" />
          </span>
        </div>

        <div class="forgot-link" @click="showForgotModal = true">忘记密码？</div>

        <button class="clay-btn clay-btn--primary clay-btn--lg clay-btn--block" :disabled="loading" @click="handleLogin">
          <van-loading v-if="loading" size="20" color="#fff" />
          <span v-else>登录</span>
        </button>

        <div class="oauth-row">
          <span class="oauth-divider">其他登录方式</span>
          <div class="oauth-buttons">
            <button class="oauth-btn oauth-btn--wechat">
              <span class="oauth-emoji">💬</span>
            </button>
            <button class="oauth-btn oauth-btn--apple">
              <span class="oauth-emoji">🍎</span>
            </button>
            <button class="oauth-btn oauth-btn--google">
              <span class="oauth-emoji">G</span>
            </button>
          </div>
        </div>
      </div>

      <!-- 注册表单 -->
      <div v-else class="form-pane">
        <div class="clay-input">
          <span class="clay-input__prefix">
            <ClayIcon color="soft-brand" size="sm">
              <LocalIcon name="user-o" size="16" color="var(--ab-brand-600)" />
            </ClayIcon>
          </span>
          <input v-model="registerForm.username" type="text" placeholder="请输入用户名（支持中文）" />
        </div>
        <div class="clay-input">
          <span class="clay-input__prefix">
            <ClayIcon color="soft-brand" size="sm">
              <LocalIcon name="envelop-o" size="16" color="var(--ab-brand-600)" />
            </ClayIcon>
          </span>
          <input v-model="registerForm.email" type="email" placeholder="请输入邮箱" />
        </div>
        <div class="clay-input">
          <span class="clay-input__prefix">
            <ClayIcon color="soft-brand" size="sm">
              <LocalIcon name="lock" size="16" color="var(--ab-brand-600)" />
            </ClayIcon>
          </span>
          <input
            v-model="registerForm.password"
            :type="showPwd ? 'text' : 'password'"
            placeholder="请输入密码（≥6位，不含中文）"
          />
          <span class="clay-input__suffix" @click="showPwd = !showPwd">
            <LocalIcon :name="showPwd ? 'eye-o' : 'closed-eye'" size="20" />
          </span>
        </div>
        <div class="clay-input">
          <span class="clay-input__prefix">
            <ClayIcon color="soft-brand" size="sm">
              <LocalIcon name="lock" size="16" color="var(--ab-brand-600)" />
            </ClayIcon>
          </span>
          <input
            v-model="registerForm.confirmPassword"
            :type="showPwd ? 'text' : 'password'"
            placeholder="请再次输入密码"
          />
        </div>

        <button class="clay-btn clay-btn--primary clay-btn--lg clay-btn--block" :disabled="loading" @click="handleRegister">
          <van-loading v-if="loading" size="20" color="#fff" />
          <span v-else>注册</span>
        </button>
      </div>
    </div>

    <!-- 忘记密码弹窗 -->
    <van-popup v-model:show="showForgotModal" position="center" :style="{ width: '85%', borderRadius: '24px' }">
      <div class="forgot-modal">
        <h3 class="modal-title">忘记密码</h3>
        <p class="modal-desc">输入注册邮箱，我们会发送验证码</p>
        <div class="clay-input" style="margin-bottom: 16px;">
          <span class="clay-input__prefix">
            <ClayIcon color="soft-brand" size="sm">
              <LocalIcon name="envelop-o" size="16" color="var(--ab-brand-600)" />
            </ClayIcon>
          </span>
          <input v-model="forgotForm.email" type="email" placeholder="请输入注册时的邮箱" />
        </div>
        <div class="modal-button-group">
          <button class="clay-btn clay-btn--primary clay-btn--block" :disabled="forgotLoading" @click="handleForgotSubmit">
            <van-loading v-if="forgotLoading" size="18" color="#fff" />
            <span v-else>获取验证码</span>
          </button>
          <button class="clay-btn clay-btn--secondary clay-btn--block" @click="showForgotModal = false">取消</button>
        </div>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showSuccessToast, showFailToast } from 'vant'
import { login, register } from '../api'
import ClayIcon from '@/components/ClayIcon.vue'

const router = useRouter()
const activeTab = ref('login')
const loading = ref(false)
const showPwd = ref(false)

const tabs = [
  { name: 'login', label: '登录' },
  { name: 'register', label: '注册' }
]

const loginForm = ref({ username: '', password: '' })
const registerForm = ref({ username: '', email: '', password: '', confirmPassword: '' })
const showForgotModal = ref(false)
const forgotStep = ref(1)
const forgotLoading = ref(false)
const forgotForm = ref({ email: '', code: '', newPassword: '', confirmPassword: '' })

const validatePassword = (val) => {
  if (/[\u4e00-\u9fff]/.test(val)) return '密码不能包含中文'
  if (val.length < 6) return '密码长度至少6位'
  return true
}
const validateConfirmPassword = (val) => {
  if (val !== registerForm.value.password) return '两次输入的密码不一致'
  return true
}

const handleLogin = async () => {
  if (!loginForm.value.username) { showFailToast('请输入用户名'); return }
  if (!loginForm.value.password) { showFailToast('请输入密码'); return }
  loading.value = true
  try {
    await login({ username: loginForm.value.username, password: loginForm.value.password })
    showSuccessToast('登录成功')
    router.replace('/')
  } catch (error) {
    showFailToast(error.response?.data?.detail || '登录失败')
  } finally { loading.value = false }
}

const handleRegister = async () => {
  if (!registerForm.value.username) { showFailToast('请输入用户名'); return }
  if (!registerForm.value.email) { showFailToast('请输入邮箱'); return }
  if (validatePassword(registerForm.value.password) !== true) {
    showFailToast(validatePassword(registerForm.value.password))
    return
  }
  if (validateConfirmPassword(registerForm.value.confirmPassword) !== true) {
    showFailToast(validateConfirmPassword(registerForm.value.confirmPassword))
    return
  }
  loading.value = true
  try {
    await register({ username: registerForm.value.username, email: registerForm.value.email, password: registerForm.value.password })
    showSuccessToast('注册成功')
    activeTab.value = 'login'
  } catch (error) {
    showFailToast(error.response?.data?.detail || '注册失败')
  } finally { loading.value = false }
}

const handleForgotSubmit = async () => {
  forgotLoading.value = true
  setTimeout(() => {
    showSuccessToast('验证码已发送，请查收邮箱')
    forgotStep.value = 2
    forgotLoading.value = false
  }, 1000)
}
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 背景渐变光晕 */
.bg-deco {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  background: linear-gradient(180deg, #f4f8f2 0%, #eaf3e7 100%);
}
.bg-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
  &--1 {
    top: -100px; left: -80px;
    width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(24, 226, 153, 0.35) 0%, transparent 70%);
  }
  &--2 {
    top: 30%; right: -120px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(129, 95, 240, 0.25) 0%, transparent 70%);
  }
  &--3 {
    bottom: -100px; left: 30%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(255, 107, 53, 0.18) 0%, transparent 70%);
  }
}

.login-container {
  position: relative;
  z-index: 1;
  padding: 56px 24px 40px;
}

/* Logo */
.logo-section {
  text-align: center;
  margin-bottom: 36px;
}
.logo-clay {
  width: 88px;
  height: 88px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #5feab2 0%, #18e299 60%, #14b87c 100%);
  border-radius: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    inset 0 -4px 0 rgba(0, 0, 0, 0.10),
    inset 0 4px 8px rgba(255, 255, 255, 0.6),
    0 12px 28px rgba(24, 226, 153, 0.35),
    0 4px 8px rgba(24, 226, 153, 0.20);
  animation: clayFloat 4s ease-in-out infinite;
}
.logo-emoji {
  font-size: 44px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.12));
  line-height: 1;
}
.app-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--ab-text-primary);
  letter-spacing: -0.04em;
  line-height: 1.1;
  margin-bottom: 8px;
}
.app-subtitle {
  font-size: 14px;
  color: var(--ab-text-tertiary);
  font-weight: 500;
  letter-spacing: -0.01em;
}

/* 药丸 Tab */
.tabs-pill {
  display: flex;
  background: #ffffff;
  padding: 4px;
  border-radius: 9999px;
  box-shadow: var(--ab-shadow-float-sm);
  margin-bottom: 24px;
}
.tab-trigger {
  flex: 1;
  height: 40px;
  border: none;
  background: transparent;
  border-radius: 9999px;
  font-size: 14px;
  font-weight: 600;
  color: var(--ab-text-tertiary);
  cursor: pointer;
  transition: all var(--ab-transition-normal);
  font-family: inherit;
  letter-spacing: -0.01em;
  &.is-active {
    background: linear-gradient(135deg, #18e299, #14b87c);
    color: #fff;
    box-shadow:
      inset 0 -2px 0 rgba(0, 0, 0, 0.08),
      inset 0 2px 4px rgba(255, 255, 255, 0.4),
      0 4px 12px rgba(24, 226, 153, 0.30);
  }
}

/* 表单 */
.form-pane {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.forgot-link {
  text-align: right;
  padding: 4px 4px;
  font-size: 13px;
  color: var(--ab-brand-600);
  cursor: pointer;
  font-weight: 600;
  &:active { opacity: 0.7; }
}

/* OAuth 区 */
.oauth-row {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
.oauth-divider {
  font-size: 12px;
  color: var(--ab-text-tertiary);
  position: relative;
  width: 100%;
  text-align: center;
  &::before, &::after {
    content: '';
    position: absolute;
    top: 50%;
    width: calc(50% - 70px);
    height: 1px;
    background: var(--ab-border-medium);
  }
  &::before { left: 0; }
  &::after { right: 0; }
}
.oauth-buttons {
  display: flex;
  gap: 16px;
}
.oauth-btn {
  width: 52px;
  height: 52px;
  border: none;
  background: #ffffff;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--ab-shadow-float-sm);
  transition: transform var(--ab-transition-normal);
  &:active { transform: scale(0.94); }
}
.oauth-emoji {
  font-size: 24px;
  font-weight: 700;
  color: var(--ab-text-primary);
  line-height: 1;
}
.oauth-btn--wechat .oauth-emoji { color: #07c160; }
.oauth-btn--apple .oauth-emoji { color: #000; }

/* 弹窗 */
.forgot-modal {
  padding: 28px 24px;
}
.modal-title {
  text-align: center;
  font-size: 22px;
  font-weight: 700;
  color: var(--ab-text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 6px;
}
.modal-desc {
  text-align: center;
  font-size: 13px;
  color: var(--ab-text-tertiary);
  margin-bottom: 20px;
}
.modal-button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 4px;
}
</style>
