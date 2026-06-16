/**
 * 通用请求工具封装
 * 统一处理加载状态、错误提示、网络异常
 * 技术栈：Vue3 + Axios + Vant
 */

import axios from 'axios';
import { showToast, showDialog, showLoading, closeLoading } from 'vant';

// 创建 axios 实例
const instance = axios.create({
  baseURL: '/api',
  timeout: 30000,
  withCredentials: true
});

/**
 * 请求拦截器
 * 在发送请求前统一处理
 */
instance.interceptors.request.use(
  (config) => {
    // 如果是 FormData 类型，不需要设置 Content-Type
    if (!(config.data instanceof FormData)) {
      config.headers = {
        ...config.headers,
        'Content-Type': 'application/json;charset=UTF-8'
      };
    }
    
    // 如果配置了 showLoading，显示加载提示
    if (config.showLoading !== false) {
      showLoading({
        message: config.loadingText || '加载中...',
        forbidClick: config.forbidClick !== false
      });
    }
    
    return config;
  },
  (error) => {
    closeLoading();
    showToast({
      type: 'fail',
      message: '请求配置错误'
    });
    return Promise.reject(error);
  }
);

/**
 * 响应拦截器
 * 统一处理响应数据和错误
 */
instance.interceptors.response.use(
  (response) => {
    closeLoading();
    
    const { data } = response;
    
    // 如果返回的是 Blob 类型（如下载文件），直接返回
    if (data instanceof Blob) {
      return response;
    }
    
    // 检查业务状态码
    if (data.code === 200) {
      // 成功，返回数据
      return data;
    } else {
      // 业务错误
      const errorMessage = data.message || '操作失败';
      
      // 如果配置了 showError，显示错误提示
      if (response.config.showError !== false) {
        showToast({
          type: 'fail',
          message: errorMessage
        });
      }
      
      return Promise.reject(new Error(errorMessage));
    }
  },
  (error) => {
    closeLoading();
    
    // 判断错误类型
    if (error.response) {
      // 请求已发送，服务器返回了非 2xx 状态码
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          handleError(data?.message || '请求参数错误', error.response.config);
          break;
        case 401:
          handleError('请先登录', error.response.config);
          break;
        case 403:
          handleError('权限不足，无法操作', error.response.config);
          break;
        case 404:
          handleError('请求的资源不存在', error.response.config);
          break;
        case 500:
          handleError('服务器繁忙，请稍后再试', error.response.config);
          break;
        default:
          handleError(data?.message || `请求失败，状态码: ${status}`, error.response.config);
      }
    } else if (error.request) {
      // 请求已发送，但没有收到响应（网络错误）
      handleError('网络连接失败，请检查网络设置', error.config || {});
    } else {
      // 请求配置错误
      handleError(error.message || '请求配置错误', error.config || {});
    }
    
    return Promise.reject(error);
  }
);

/**
 * 统一错误处理函数
 * @param {string} message - 错误信息
 * @param {Object} config - 请求配置
 */
const handleError = (message, config) => {
  // 如果配置了 showError 为 false，则不显示错误提示
  if (config.showError === false) {
    return;
  }
  
  // 如果配置了 showRetry 为 true，显示带重试按钮的弹窗
  if (config.showRetry) {
    showDialog({
      title: '提示',
      message: message,
      confirmButtonText: '重试',
      cancelButtonText: '取消'
    }).then(() => {
      // 用户点击重试，重新发送请求
      if (config.retryCallback) {
        config.retryCallback();
      }
    }).catch(() => {
      // 用户点击取消
    });
  } else {
    // 默认显示 Toast 提示
    showToast({
      type: 'fail',
      message: message
    });
  }
};

/**
 * 封装常用的请求方法
 * @param {Object} options - 请求配置
 * @param {string} options.url - 请求地址
 * @param {string} options.method - 请求方法（get/post/put/delete）
 * @param {Object} options.data - 请求数据（post/put）
 * @param {Object} options.params - URL参数（get/delete）
 * @param {boolean} options.showLoading - 是否显示加载动画（默认true）
 * @param {string} options.loadingText - 加载提示文字
 * @param {boolean} options.forbidClick - 加载时是否禁止点击（默认true）
 * @param {boolean} options.showError - 是否显示错误提示（默认true）
 * @param {boolean} options.showRetry - 是否显示重试弹窗（默认false）
 * @param {Function} options.retryCallback - 重试回调函数
 * @returns {Promise}
 */
export const request = async (options) => {
  const {
    url,
    method = 'get',
    data = {},
    params = {},
    showLoading = true,
    loadingText = '加载中...',
    forbidClick = true,
    showError = true,
    showRetry = false,
    retryCallback = null
  } = options;
  
  try {
    const config = {
      url,
      method: method.toLowerCase(),
      showLoading,
      loadingText,
      forbidClick,
      showError,
      showRetry,
      retryCallback
    };
    
    // 根据请求方法设置数据
    if (config.method === 'get' || config.method === 'delete') {
      config.params = params;
    } else {
      config.data = data;
    }
    
    const response = await instance(config);
    return response;
  } catch (error) {
    throw error;
  }
};

/**
 * GET 请求封装
 * @param {string} url - 请求地址
 * @param {Object} params - URL参数
 * @param {Object} options - 其他配置
 * @returns {Promise}
 */
export const get = (url, params = {}, options = {}) => {
  return request({
    url,
    method: 'get',
    params,
    ...options
  });
};

/**
 * POST 请求封装
 * @param {string} url - 请求地址
 * @param {Object} data - 请求数据
 * @param {Object} options - 其他配置
 * @returns {Promise}
 */
export const post = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'post',
    data,
    ...options
  });
};

/**
 * PUT 请求封装
 * @param {string} url - 请求地址
 * @param {Object} data - 请求数据
 * @param {Object} options - 其他配置
 * @returns {Promise}
 */
export const put = (url, data = {}, options = {}) => {
  return request({
    url,
    method: 'put',
    data,
    ...options
  });
};

/**
 * DELETE 请求封装
 * @param {string} url - 请求地址
 * @param {Object} params - URL参数
 * @param {Object} options - 其他配置
 * @returns {Promise}
 */
export const del = (url, params = {}, options = {}) => {
  return request({
    url,
    method: 'delete',
    params,
    ...options
  });
};

export default instance;