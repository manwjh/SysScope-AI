import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

console.log('API_BASE_URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response.data;
  },
  (error) => {
    console.error('API Response Error:', error);
    if (error.response) {
      throw new Error(error.response.data.detail || error.response.data.message || '请求失败');
    } else if (error.request) {
      throw new Error('网络连接失败，请检查后端服务是否正常运行');
    } else {
      throw new Error('请求配置错误');
    }
  }
);

// API函数
export const getSystemInfo = async () => {
  console.log('Calling getSystemInfo...');
  return await api.get('/api/system/info');
};

export const generateTestPlan = async () => {
  console.log('Calling generateTestPlan...');
  return await api.post('/api/test-plan/generate');
};

export const executeTests = async (testPlan) => {
  console.log('Calling executeTests...', testPlan);
  return await api.post('/api/test/execute', testPlan);
};

export const getReports = async () => {
  console.log('Calling getReports...');
  return await api.get('/api/reports');
};

export const getReport = async (reportId) => {
  console.log('Calling getReport...', reportId);
  return await api.get(`/api/reports/${reportId}`);
};

export const saveSettings = async (settings) => {
  console.log('Calling saveSettings...', settings);
  return await api.post('/api/settings/save', settings);
};

export default api; 