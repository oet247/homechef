import axios from "axios";
import { useState } from "react";
import './universalFormStyle.css'

export const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const user = {
      username: username,
      password: password
    };

    try {
      const { data } = await axios.post(`${process.env.REACT_APP_API_URL}/user/login/`, user, {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: true
      });

      localStorage.clear();
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${data['access']}`;
      window.location.href = '/';
    } catch (error) {
      setError('Username or password is incorrect');
      console.error(error);
    }
  }

  return (
    <div className="wrapper">
      <div className="logoAndMoto">
        <div>
        <img className="logo" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" alt="logo" width={500} height={187}/>
        </div>
        <div className="moto"><p>The ultimate kitchen hack.</p></div>
      </div>
      <div className="form-container">
      <form className="form" onSubmit={handleSubmit}>
        <div className="form-content">
          <h3 className="form-title">Sign In</h3>
          <p className={`error ${error ? 'visible' : 'hidden'}`}>{error}</p>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              className="form-control"
              placeholder="Enter Username"
              name="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              name="password"
              type="password"
              className="form-control"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <button type="submit" className="btn">Submit</button>
          </div>
        </div>
      </form>
      </div> 
    </div>
    
  );
}