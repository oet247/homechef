import React, { createContext, useState, useEffect, useContext } from 'react';
import {jwtDecode} from 'jwt-decode';

const UserIdContext = createContext();

export const UserIdProvider = ({ children }) => {
  const [userId, setUserId] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const setUserIdFromToken = async () => {
      try {
        const jwt = localStorage.getItem('access_token');

        if (jwt) {
          const decoded = jwtDecode(jwt);
          setUserId(decoded.user_id);
        }
      } catch (error) {
        console.error('Invalid JWT token', error);
        setError('Invalid JWT token');
      }
    };

    setUserIdFromToken();
  }, []);

  return (
    <UserIdContext.Provider value={{ userId, setUserId, error }}>
      {children}
    </UserIdContext.Provider>
  );
};

export const useUserId = () => {
  const context = useContext(UserIdContext);
  if (context === undefined) {
    throw new Error('useUserId must be used within a UserIdProvider');
  }
  return context;
};
