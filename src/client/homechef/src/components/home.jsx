import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useUserId } from './customhooks/userIDHook';
import { Navigate } from 'react-router-dom';

export const withAuth = (Component) => {
  return (props) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      return <Navigate to="/login" />;
    }
    return <Component {...props} />;
  };
};

const HomeComponent = () => {
  const [message, setMessage] = useState('');
  const { userId } = useUserId();

  useEffect(() => {
    (async () => {
      try {
        const { data } = await axios.get(
          `http://localhost:8000/user/${userId}`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          }
        );
        setMessage(data.message);
      } catch (e) {
        console.log('not auth');
      }
    })();
  }, [userId]);

  return (
    <div className="form-signin mt-5 text-center">
      <h3>Hi {message}</h3>
    </div>
  );
};

export const Home = withAuth(HomeComponent);
