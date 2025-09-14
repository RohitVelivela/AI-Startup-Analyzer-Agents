import axios from 'axios';
import toast from 'react-hot-toast';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 300000, // 5 minutes timeout for long-running analyses
});

// Request interceptor for loading states
api.interceptors.request.use((config) => {
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'An error occurred';
    toast.error(message);
    return Promise.reject(error);
  }
);

export const competitorAPI = {
  // Discover competitors
  discoverCompetitors: async (inputType, inputValue) => {
    const response = await api.post('/discover', {
      input_type: inputType,
      input_value: inputValue,
    });
    return response.data;
  },

  // Analyze competitors
  analyzeCompetitors: async (competitorUrls) => {
    const response = await api.post('/analyze', competitorUrls);
    return response.data;
  },

  // Compare competitors
  compareCompetitors: async (companyAUrl, companyBUrl) => {
    const response = await api.post('/compare', {
      company_a_url: companyAUrl,
      company_b_url: companyBUrl,
    });
    return response.data;
  },

  // Export report
  exportReport: async (format, dataType, data) => {
    const response = await api.post('/export', {
      format,
      data_type: dataType,
      data,
    }, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;