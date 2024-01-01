import axios from 'axios';

let refresh = false;

const instance = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');

    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }

    return config;
  },
  (error) => {
    throw error;
  }
);

instance.interceptors.response.use(
  async (response) => {
    if (response.config.url === '/user/create/' && response.status === 201) {
      const data = JSON.parse(response.config.data);
      const user = {
        email: data.email,
        username: data.username,
        password: data.password,
      };
      const loginResponse = await instance.post('/user/login/', user);

      localStorage.clear();
      localStorage.setItem('access_token', loginResponse.data.access);
      localStorage.setItem('refresh_token', loginResponse.data.refresh);
      instance.defaults.headers.common['Authorization'] = `Bearer ${loginResponse.data['access']}`;
    }

    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry && !refresh) {
      originalRequest._retry = true;
      refresh = true;

      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          const response = await instance.post('/user/refresh/', { refresh: refreshToken });
          localStorage.setItem('access_token', response.data.access)
          instance.defaults.headers.common['Authorization'] = `Bearer ${response.data['access']}`;

          return instance(originalRequest);
        } catch (error) {
          console.error('Unable to refresh token', error);
        }
      }
    }

    refresh = false;
    throw error;
  }
);

export default instance;
