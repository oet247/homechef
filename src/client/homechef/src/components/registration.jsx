import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import instance from '../interceptors/axiosInstance';
import './universalFormStyle.css'

export const Registration = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const user = {
      email: email,
      username: username,
      password: password,
    };

    try {
      const response = await instance.post('/user/create/', user);

      if (response.status === 201) {
        console.log('Registration successful!');
        navigate('/additionalInfo');
      }
      if (response.status === 203) {
        setError('Enter valid email address!')
      }
    } catch (error) {
      if (error.response) {
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        console.log(error.request);
      } else {
        console.log('Error', error.message);
      }
      console.error('Registration error:', error);
    
    }
  };

  return (
    <div className='wrapper'>
      <div className="logoAndMoto">
        <div>
        <img className="logo" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" alt="logo" width={500} height={187}/>
        </div>
        <div className='moto'><p>The ultimate kitchen hack.</p></div>
      </div>
      <div className="form-container">
      <form className='form' onSubmit={handleSubmit}>
        <div className='form-content'>
        <h3 className='form-title'>Registration</h3>
        <p className={`error ${error ? 'visible' : 'hidden'}`}>{error}</p>
          <div className="form-group">
            <label>Username:</label>
            <input
              className='form-control'
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Email:</label>
            <input
              className='form-control'
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input
              className='form-control'
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className='form-group'>
            <button className='btn'>Register</button>
          </div> 
        </div>
      </form>
    </div>
    </div> 
  );
}
