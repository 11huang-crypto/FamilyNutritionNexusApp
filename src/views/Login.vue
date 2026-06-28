<template>
  <div class="login-page">
    <van-nav-bar title="登录" left-arrow @click-left="$router.back()" />

    <div class="login-container">
      <div class="logo-section">
        <van-icon name="shopping-cart" size="64" color="#667eea" />
        <h1 class="app-title">AI智能菜篮子</h1>
        <p class="app-subtitle">让健康饮食更简单</p>
      </div>

      <van-tabs v-model:active="activeTab" animated>
        <van-tab title="登录" name="login">
          <van-form @submit="handleLogin">
            <van-cell-group inset>
              <van-field
                v-model="loginForm.username"
                name="username"
                label="用户名"
                placeholder="请输入用户名或邮箱"
                :rules="[{ required: true, message: '请输入用户名' }]"
              />
              <van-field
                v-model="loginForm.password"
                type="password"
                name="password"
                label="密码"
                placeholder="请输入密码"
                :rules="[{ required: true, message: '请输入密码' }]"
              />
            </van-cell-group>
            <div class="forgot-link">
              <span @click="showForgotModal = true">忘记密码？</span>
            </div>
            <div class="button-group">
              <van-button round block type="primary" native-type="submit" :loading="loading">
                登录
              </van-button>
            </div>
          </van-form>
        </van-tab>

        <van-tab title="注册" name="register">
          <van-form @submit="handleRegister">
            <van-cell-group inset>
              <van-field
                v-model="registerForm.username"
                name="username"
                label="用户名"
                placeholder="请输入用户名（支持中文）"
                :rules="[{ required: true, message: '请输入用户名' }]"
              />
              <van-field
                v-model="registerForm.email"
                name="email"
                label="邮箱"
                type="email"
                placeholder="请输入邮箱"
                :rules="[
                  { required: true, message: '请输入邮箱' },
                  { pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: '请输入正确的邮箱格式' }
                ]"
              />
              <van-field
                v-model="registerForm.password"
                type="password"
                name="password"
                label="密码"
                placeholder="请输入密码（不含中文）"
                :rules="[
                  { required: true, message: '请输入密码' },
                  { validator: validatePassword }
                ]"
              />
              <van-field
                v-model="registerForm.confirmPassword"
                type="password"
                name="confirmPassword"
                label="确认密码"
                placeholder="请再次输入密码"
                :rules="[
                  { required: true, message: '请确认密码' },
                  { validator: validateConfirmPassword }
                ]"
              />
            </van-cell-group>
            <div class="button-group">
              <van-button round block type="primary" native-type="submit" :loading="loading">
                注册
              </van-button>
            </div>
          </van-form>
        </van-tab>
      </van-tabs>
    </div>

    <!-- 忘记密码弹窗 -->
    <van-popup v-model:show="showForgotModal" position="center" :style="{ width: '85%', borderRadius: '16px' }">
      <div class="forgot-modal">
        <h3 class="modal-title">忘记密码</h3>
        
        <van-form v-if="forgotStep === 1" @submit="handleForgotSubmit">
          <van-cell-group>
            <van-field
              v-model="forgotForm.email"
              name="email"
              label="邮箱"
              type="email"
              placeholder="请输入注册时的邮箱"
              :rules="[
                { required: true, message: '请输入邮箱' },
                { pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: '请输入正确的邮箱格式' }
              ]"
            />
          </van-cell-group>
          <div class="modal-button-group">
            <van-button round block type="primary" native-type="submit" :loading="forgotLoading">
              获取验证码
            </van-button>
            <van-button round block type="default" @click="showForgotModal = false">
              取消
            </van-button>
          </div>
        </van-form>

        <van-form v-if="forgotStep === 2" @submit="handleResetSubmit">
          <van-cell-group>
            <van-field
              v-model="forgotForm.code"
              name="code"
              label="验证码"
              placeholder="请输入验证码"
              :rules="[
                { required: true, message: '请输入验证码' },
                { pattern: /^\d{6}$/, message: '请输入6位数字验证码' }
              ]"
            />
            <van-field
              v-model="forgotForm.newPassword"
              type="password"
              name="newPassword"
              label="新密码"
              placeholder="请输入新密码"
              :rules="[
                { required: true, message: '请输入新密码' },
                { validator: validatePassword }
              ]"
            />
            <van-field
              v-model="forgotForm.confirmPassword"
              type="password"
              name="confirmPassword"
              label="确认密码"
              placeholder="请再次输入新密码"
              :rules="[
                { required: true, message: '请确认密码' },
                { validator: validateResetConfirmPassword }
              ]"
            />
          </van-cell-group>
          <div class="modal-button-group">
            <van-button round block type="primary" native-type="submit" :loading="forgotLoading">
              重置密码
            </van-button>
            <van-button round block type="default" @click="forgotStep = 1">
              返回
            </van-button>
          </div>
        </van-form>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { showToast, showSuccessToast, showFailToast } from 'vant';
import { login, register, forgotPassword, resetPassword } from '../api';

const router = useRouter();
const activeTab = ref('login');
const loading = ref(false);

const loginForm = ref({
  username: '',
  password: ''
});

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

const showForgotModal = ref(false);
const forgotStep = ref(1);
const forgotLoading = ref(false);
const forgotForm = ref({
  email: '',
  code: '',
  newPassword: '',
  confirmPassword: ''
});

const validatePassword = (val) => {
  if (/[\u4e00-\u9fff]/.test(val)) {
    return '密码不能包含中文';
  }
  if (val.length < 6) {
    return '密码长度至少6位';
  }
  return true;
};

const validateConfirmPassword = (val) => {
  if (val !== registerForm.value.password) {
    return '两次输入的密码不一致';
  }
  return true;
};

const validateResetConfirmPassword = (val) => {
  if (val !== forgotForm.value.newPassword) {
    return '两次输入的密码不一致';
  }
  return true;
};

const handleLogin = async () => {
  loading.value = true;
  try {
    const response = await login({
      username: loginForm.value.username,
      password: loginForm.value.password
    });
    showSuccessToast('登录成功');
    router.replace('/');
  } catch (error) {
    showFailToast(error.response?.data?.detail || '登录失败');
  } finally {
    loading.value = false;
  }
};

const handleRegister = async () => {
  loading.value = true;
  try {
    const response = await register({
      username: registerForm.value.username,
      email: registerForm.value.email,
      password: registerForm.value.password
    });
    showSuccessToast('注册成功');
    activeTab.value = 'login';
  } catch (error) {
    showFailToast(error.response?.data?.detail || '注册失败');
  } finally {
    loading.value = false;
  }
};

const handleForgotSubmit = async () => {
  forgotLoading.value = true;
  try {
    await forgotPassword(forgotForm.value.email);
    showSuccessToast('验证码已发送，请查收邮箱');
    forgotStep.value = 2;
  } catch (error) {
    showFailToast(error.response?.data?.detail || '获取验证码失败');
  } finally {
    forgotLoading.value = false;
  }
};

const handleResetSubmit = async () => {
  forgotLoading.value = true;
  try {
    await resetPassword({
      email: forgotForm.value.email,
      code: forgotForm.value.code,
      new_password: forgotForm.value.newPassword
    });
    showSuccessToast('密码重置成功');
    showForgotModal.value = false;
    forgotStep.value = 1;
    forgotForm.value = {
      email: '',
      code: '',
      newPassword: '',
      confirmPassword: ''
    };
    activeTab.value = 'login';
  } catch (error) {
    showFailToast(error.response?.data?.detail || '重置密码失败');
  } finally {
    forgotLoading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-container {
  padding: 40px 20px;
}

.logo-section {
  text-align: center;
  margin-bottom: 40px;
  color: white;
}

.app-title {
  font-size: 28px;
  font-weight: bold;
  margin: 20px 0 10px;
}

.app-subtitle {
  font-size: 16px;
  opacity: 0.9;
}

.forgot-link {
  text-align: right;
  padding: 0 16px;
  margin-bottom: 20px;
}

.forgot-link span {
  color: #ffd700;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  text-decoration: underline;
}

.forgot-link span:hover {
  color: #fffacd;
}

.button-group {
  margin-top: 30px;
  padding: 0 16px;
}

.forgot-modal {
  padding: 24px;
}

.modal-title {
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.modal-button-group {
  margin-top: 20px;
}

.modal-button-group .van-button {
  margin-bottom: 12px;
}

:deep(.van-tabs__nav) {
  background: transparent;
}

:deep(.van-tab) {
  color: rgba(255, 255, 255, 0.7);
}

:deep(.van-tab--active) {
  color: white;
  font-weight: bold;
}

:deep(.van-tabs__line) {
  background: white;
}

:deep(.van-cell-group) {
  background: white;
  border-radius: 16px;
  overflow: hidden;
}
</style>
