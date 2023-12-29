import React, { createContext, useState, useContext } from 'react';
import {jwtDecode} from 'jwt-decode';

const UserIdContext = createContext();

export const UserIdProvider = ({ children }) => {
  const [userId, setUserId] = useState(() => {
    const jwt = localStorage.getItem('access_token');

    if (jwt) {
      const decoded = jwtDecode(jwt);
      return decoded.user_id;
    }

    return null;
  });

  return (
    <UserIdContext.Provider value={{ userId, setUserId }}>
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
