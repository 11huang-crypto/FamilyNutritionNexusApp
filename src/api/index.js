/**
 * API 接口封装
 * 所有后端接口统一在此管理
 */

import axios from '../utils/axios';

/**
 * 用户注册
 * POST /auth/register
 */
export const register = async (data) => {
  try {
    const response = await axios.post('/auth/register', data);
    if (response.access_token) {
      localStorage.setItem('token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
    }
    return response;
  } catch (error) {
    console.error('注册失败:', error);
    throw error;
  }
};

/**
 * 用户登录
 * POST /auth/login
 * 注意：后端使用 OAuth2PasswordRequestForm，需要发送表单格式
 */
export const login = async (data) => {
  try {
    // 创建表单数据
    const formData = new URLSearchParams();
    formData.append('username', data.username);
    formData.append('password', data.password);
    
    const response = await axios.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    if (response.access_token) {
      localStorage.setItem('token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
    }
    return response;
  } catch (error) {
    console.error('登录失败:', error);
    throw error;
  }
};

/**
 * 忘记密码 - 获取验证码
 * POST /auth/forgot-password
 */
export const forgotPassword = async (email) => {
  try {
    const response = await axios.post('/auth/forgot-password', { email });
    return response;
  } catch (error) {
    console.error('获取验证码失败:', error);
    throw error;
  }
};

/**
 * 重置密码
 * POST /auth/reset-password
 */
export const resetPassword = async (data) => {
  try {
    const response = await axios.post('/auth/reset-password', data);
    return response;
  } catch (error) {
    console.error('重置密码失败:', error);
    throw error;
  }
};

/**
 * 获取当前用户家庭列表
 * GET /family/my
 */
export const getMyFamilies = async () => {
  try {
    const response = await axios.get('/family/my');
    return response;
  } catch (error) {
    console.error('获取家庭列表失败:', error);
    throw error;
  }
};

/**
 * 创建家庭
 * POST /family/create
 */
export const createFamily = async (data) => {
  try {
    const response = await axios.post('/family/create', data);
    if (response && response.id) {
      localStorage.setItem('family_id', response.id.toString());
    }
    return response;
  } catch (error) {
    console.error('创建家庭失败:', error);
    throw error;
  }
};

/**
 * 获取家庭成员列表
 * GET /family/{family_id}/members
 */
export const getFamilyMembers = async (family_id) => {
  try {
    const response = await axios.get(`/family/${family_id}/members`);
    return response;
  } catch (error) {
    console.error('获取家庭成员失败:', error);
    throw error;
  }
};

/**
 * 生成邀请码
 * POST /family/{family_id}/generate-code
 */
export const generateInviteCode = async (family_id) => {
  try {
    const response = await axios.post(`/family/${family_id}/generate-code`);
    return response;
  } catch (error) {
    console.error('生成邀请码失败:', error);
    throw error;
  }
};

/**
 * 邀请成员（通过邮箱）
 * POST /family/{family_id}/invite
 */
export const inviteMember = async (family_id, data) => {
  try {
    const response = await axios.post(`/family/${family_id}/invite`, data);
    return response;
  } catch (error) {
    console.error('邀请成员失败:', error);
    throw error;
  }
};

/**
 * 加入家庭（通过邀请码）
 * POST /family/join
 */
export const joinFamily = async (data) => {
  try {
    const response = await axios.post('/family/join', data);
    return response;
  } catch (error) {
    console.error('加入家庭失败:', error);
    throw error;
  }
};

/**
 * 添加健康档案
 * POST /health/profile
 */
export const addHealthProfile = async (data) => {
  try {
    const response = await axios.post('/health/profile', data);
    return response;
  } catch (error) {
    console.error('添加健康档案失败:', error);
    throw error;
  }
};

/**
 * 获取家庭健康档案
 * GET /health/family/{family_id}
 */
export const getHealthProfiles = async (family_id) => {
  try {
    const response = await axios.get(`/health/family/${family_id}`);
    return response;
  } catch (error) {
    console.error('获取健康档案失败:', error);
    throw error;
  }
};

/**
 * 更新健康档案
 * PUT /health/profile/{profile_id}
 */
export const updateHealthProfile = async (profile_id, data) => {
  try {
    const response = await axios.put(`/health/profile/${profile_id}`, data);
    return response;
  } catch (error) {
    console.error('更新健康档案失败:', error);
    throw error;
  }
};

/**
 * 删除健康档案
 * DELETE /health/profile/{profile_id}
 */
export const deleteHealthProfile = async (profile_id) => {
  try {
    const response = await axios.delete(`/health/profile/${profile_id}`);
    return response;
  } catch (error) {
    console.error('删除健康档案失败:', error);
    throw error;
  }
};

/**
 * 添加菜篮子项目
 * POST /basket/item
 */
export const addBasketItem = async (data) => {
  try {
    const response = await axios.post('/basket/item', data);
    return response;
  } catch (error) {
    console.error('添加菜篮子项目失败:', error);
    throw error;
  }
};

/**
 * 获取家庭菜篮子数据
 * GET /basket/family/{family_id}
 */
export const getFamilyBasket = async (family_id) => {
  try {
    const response = await axios.get(`/basket/family/${family_id}`);
    return response;
  } catch (error) {
    console.error('获取菜篮子数据失败:', error);
    throw error;
  }
};

/**
 * 检查食材禁忌
 * GET /basket/check?family_id={family_id}
 */
export const checkFoodConflict = async (family_id) => {
  try {
    const response = await axios.get(`/basket/check?family_id=${family_id}`);
    return response;
  } catch (error) {
    console.error('检查食材禁忌失败:', error);
    throw error;
  }
};

/** 菜篮子冲突检查（别名） */
export const checkBasketConflict = checkFoodConflict

/**
 * 图片识别接口
 * POST /analyze
 */
export const analyzeImage = async (formData) => {
  if (!(formData instanceof FormData)) {
    throw new Error('参数必须是 FormData 类型');
  }
  if (!formData.has('image')) {
    throw new Error('FormData 中必须包含 image 字段');
  }
  try {
    const response = await axios.post('/analyze', formData, {
      headers: {
        'Content-Type': undefined
      }
    });
    return response;
  } catch (error) {
    console.error('图片识别接口调用失败:', error);
    throw error;
  }
};

/**
 * 快速识别（仅需食材名称）
 * POST /api/analyze
 */
export const analyzeFood = async (data) => {
  try {
    const response = await axios.post('/api/analyze', data)
    return response
  } catch (error) {
    console.error('食材识别失败:', error)
    throw error
  }
}

/**
 * 生成一周食谱
 * POST /meal-plan/generate
 * @param {Object} data - 食谱生成参数
 * @param {number} data.family_id - 家庭ID
 * @returns {Promise<Object>} - 食谱数据
 */
export const generateMealPlan = async (data) => {
  try {
    const response = await axios.post('/meal-plan/generate', data);
    return response;
  } catch (error) {
    console.error('生成食谱失败:', error);
    throw error;
  }
};

/**
 * 获取采购清单
 * GET /shopping-list/realtime?family_id={family_id}
 * @param {number} family_id - 家庭ID
 * @returns {Promise<Object>} - 采购清单数据
 */
export const getShoppingList = async (family_id) => {
  try {
    const response = await axios.get(`/shopping-list/realtime?family_id=${family_id}`);
    return response;
  } catch (error) {
    console.error('获取采购清单失败:', error);
    throw error;
  }
};

/**
 * 添加采购项
 * POST /shopping-list/item
 * @param {Object} data - 采购项数据
 * @param {number} data.family_id - 家庭ID
 * @param {string} data.name - 食材名称
 * @param {number} data.quantity - 数量
 * @param {string} data.unit - 单位
 * @returns {Promise<Object>} - 添加的采购项
 */
export const addShoppingItem = async (data) => {
  try {
    const response = await axios.post('/shopping-list/item', data);
    return response;
  } catch (error) {
    console.error('添加采购项失败:', error);
    throw error;
  }
};

/**
 * 更新采购项
 * PUT /shopping-list/item/{item_id}
 * @param {number} item_id - 采购项ID
 * @param {Object} data - 更新数据
 * @param {string} [data.name] - 食材名称
 * @param {number} [data.quantity] - 数量
 * @param {string} [data.unit] - 单位
 * @param {boolean} [data.checked] - 勾选状态
 * @returns {Promise<Object>} - 更新后的采购项
 */
export const updateShoppingItem = async (item_id, data) => {
  try {
    const response = await axios.put(`/shopping-list/item/${item_id}`, data);
    return response;
  } catch (error) {
    console.error('更新采购项失败:', error);
    throw error;
  }
};

/**
 * 删除采购项
 * DELETE /shopping-list/item/{item_id}
 * @param {number} item_id - 采购项ID
 * @returns {Promise<Object>} - 删除结果
 */
export const deleteShoppingItem = async (item_id) => {
  try {
    const response = await axios.delete(`/shopping-list/item/${item_id}`);
    return response;
  } catch (error) {
    console.error('删除采购项失败:', error);
    throw error;
  }
};

/**
 * WebSocket 管理器
 * 用于采购清单实时协同编辑
 */
export class WebSocketManager {
  constructor(url) {
    this.url = url;
    this.socket = null;
    this.callbacks = {};
  }
  
  /**
   * 连接 WebSocket
   * @returns {Promise} - 连接成功的 Promise
   */
  connect() {
    return new Promise((resolve, reject) => {
      // 构建完整的 WebSocket URL
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.host;
      const fullUrl = `${protocol}//${host}${this.url}`;
      
      this.socket = new WebSocket(fullUrl);
      
      this.socket.onopen = () => {
        console.log('WebSocket connected:', fullUrl);
        resolve();
      };
      
      this.socket.onclose = (event) => {
        console.log('WebSocket closed:', event);
        // 可以在这里实现重连逻辑
      };
      
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      };
      
      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (this.callbacks[data.type]) {
            this.callbacks[data.type](data.payload);
          }
        } catch (parseError) {
          console.error('WebSocket message parse error:', parseError);
        }
      };
    });
  }
  
  /**
   * 注册消息回调
   * @param {string} type - 消息类型
   * @param {Function} callback - 回调函数
   */
  on(type, callback) {
    this.callbacks[type] = callback;
  }
  
  /**
   * 发送消息
   * @param {string} type - 消息类型
   * @param {Object} payload - 消息内容
   */
  send(type, payload) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type, payload }));
    } else {
      console.warn('WebSocket not connected, message not sent');
    }
  }
  
  /**
   * 关闭连接
   */
  close() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}