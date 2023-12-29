import { useEffect } from "react";
import axios from "axios";

export const Logout = () => {
  useEffect(() => {
    (async () => {
      try {
        await axios.get(
          `${process.env.REACT_APP_API_URL}/user/logout/`,
          {
            refresh_token: localStorage.getItem('refresh_token')
          },
          {
            headers: {
              'Authorization': `Bearer localStorage.getItem('access_token')`
            },
            withCredentials: true
          }
        );

        localStorage.clear();
        axios.defaults.headers.common['Authorization'] = null;
        window.location.href = '/login';
      } catch (e) {
        console.log('logout not working', e);
      }
    })();
  }, []);

}
