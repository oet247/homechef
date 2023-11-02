import React, { useState } from 'react';
import axios from 'axios';
import './Registration.css';

function Registration() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState(''); // Add email state
  const [password, setPassword] = useState('');

  const handleRegistration = async () => {
    try {
      const response = await axios.post(
        'http://localhost:8000/register/',
        {
          email: email,
          username: username,
          password: password,
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        }
      );

      if (response.status === 201) {
        console.log('Registration successful!');
      }
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  return (
    <div className="registration-container">
      <h2>Registration</h2>
      <div className="input-container">
        <label>Username:</label>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div className="input-container">
        <label>Email:</label>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div className="input-container">
        <label>Password:</label>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <button onClick={handleRegistration}>Register</button>
    </div>
  );
}

export default Registration;
