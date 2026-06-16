/**
 * Axios 请求封装
 * 统一处理请求头、拦截器、错误处理
 */

import axios from 'axios';
import { showToast } from 'vant';

// 创建 axios 实例
const instance = axios.create({
  baseURL: '/api',        // 基础URL，配合 Vite 代理
  timeout: 30000,         // 请求超时时间 30秒
  withCredentials: true   // 携带凭证（如需登录态）
});

/**
 * 请求拦截器
 * 在发送请求前做一些处理
 */
instance.interceptors.request.use(
  (config) => {
    // 如果是 FormData 类型，不需要设置 Content-Type，浏览器会自动处理
    if (!(config.data instanceof FormData)) {
      config.headers = {
        ...config.headers,
        'Content-Type': 'application/json;charset=UTF-8'
      };
    }
    return config;
  },
  (error) => {
    // 请求错误处理
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
    /**
     * 响应成功处理
     * 后端返回格式：{ code, data, message }
     */
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
      // 业务错误，显示错误信息
      showToast({
        type: 'fail',
        message: data.message || '操作失败'
      });
      return Promise.reject(new Error(data.message || '业务错误'));
    }
  },
  (error) => {
    /**
     * 响应错误处理
     * 处理 HTTP 状态码错误和网络错误
     */
    console.error('HTTP Error:', error);
    
    // 判断错误类型
    if (error.response) {
      // 请求已发送，服务器返回了非 2xx 状态码
      const { status, data } = error.response;
      
      // 根据不同状态码给出不同提示
      switch (status) {
        case 400:
          // 请求参数错误
          showToast({
            type: 'fail',
            message: data?.message || '图片格式错误，请重新上传'
          });
          break;
        case 401:
          // 未授权
          showToast({
            type: 'fail',
            message: '请先登录'
          });
          // 可以在这里跳转到登录页
          break;
        case 403:
          // 权限不足
          showToast({
            type: 'fail',
            message: '权限不足，无法操作'
          });
          break;
        case 404:
          // 资源未找到
          showToast({
            type: 'fail',
            message: '请求的资源不存在'
          });
          break;
        case 500:
          // 服务器错误
          showToast({
            type: 'fail',
            message: '服务器繁忙，请稍后再试'
          });
          break;
        default:
          // 其他错误
          showToast({
            type: 'fail',
            message: data?.message || `请求失败，状态码: ${status}`
          });
      }
    } else if (error.request) {
      // 请求已发送，但没有收到响应（网络错误）
      showToast({
        type: 'fail',
        message: '网络连接失败，请检查网络'
      });
    } else {
      // 请求配置错误
      showToast({
        type: 'fail',
        message: error.message || '请求配置错误'
      });
    }
    
    return Promise.reject(error);
  }
);

export default instance;