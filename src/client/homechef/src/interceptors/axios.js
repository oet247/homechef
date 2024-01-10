import axios from "axios";
import {jwtDecode} from "jwt-decode";
import { EventEmitter } from "events";

export const userIdEmitter = new EventEmitter();

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
        const token = response.data['access'];
        const decoded = jwtDecode(token);
        const userId = decoded.user_id;

        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        localStorage.setItem('access_token', token);
        localStorage.setItem('refresh_token', response.data.refresh);

        userIdEmitter.emit('userIdUpdated', userId);
        return axios(error.config);
      }
    }

    refresh = false;
    return error;
  }
);
