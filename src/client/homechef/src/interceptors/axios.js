import axios from "axios";

let refresh = false;

axios.interceptors.response.use(
  (resp) => resp,
  async (error) => {
    if (error.response.status === 401 && !refresh) {
      refresh = true;

      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/user/login/refresh/`,
        {
          refresh: localStorage.getItem('refresh_token'),
        },
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
        },
        { withCredentials: true }
      );

      if (response.status === 200) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data['access']}`;
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        return axios(error.config);
      }
    }

    refresh = false;
    return error;
  }
);
