import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
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
  return await api.get('/api/system/info');
};

export const generateTestPlan = async () => {
  return await api.post('/api/test-plan/generate');
};

export const executeTests = async (testPlan) => {
  return await api.post('/api/test/execute', testPlan);
};

export const getReports = async () => {
  return await api.get('/api/reports');
};

export const getReport = async (reportId) => {
  return await api.get(`/api/reports/${reportId}`);
};

export default api; 