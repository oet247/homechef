import { useEffect, useState } from "react";
import axios from "axios";
import {jwtDecode} from "jwt-decode";

export const Home = () => {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const authorizationToken = localStorage.getItem("access_token");
    if (authorizationToken) {
      const decoded = jwtDecode(authorizationToken);
      (async () => {
        try {
          const { data } = await axios.get(
            `http://localhost:8000/user/${decoded.user_id}`,
            {
              headers: {
                'Authorization': `Bearer ${authorizationToken}`
              }
            }
          );
          setMessage(data.message);
        } catch (e) {
          console.log('not auth');
        }
      })();
    } else {
      window.location.href = '/login';
    }
  }, []);

  return (
    <div className="form-signin mt-5 text-center">
      <h3>Hi {message}</h3>
    </div>
  );
};
