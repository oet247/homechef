import React, { useState } from 'react';
import axios from 'axios';
import './Registration.css';

function Registration() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const user = {
      email: email,
      username: username,
      password: password,
    };

    try {
      const response = await axios.post('http://localhost:8000/user/create/', user,{
          headers: {
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        }
      );

      if (response.status === 201) {
        console.log('Registration successful!');
      }
      if (response.status === 203) {
        setError('Enter valid email address!')
      }
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  return (
    <div className="registration-container">
      <form onSubmit={handleSubmit}>
        <div>
        <h3>Registration</h3>
        {error && <p className="error">{error}</p>}
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
          <button>Register</button>
        </div>
      </form>
    </div>
  );
}

export default Registration;
