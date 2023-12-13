import { useState, useEffect } from "react";
import axios from "axios";

export const ProfilePage = () => {
  const [full_name, setFullName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [bio, setBio] = useState('');
  const [birthday, setBirthday] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      
      const profileData ={
        full_name:full_name,
        username:username,
        email:email,
        password:password,
        bio:bio,
        birthday:birthday
      }
      
      try {
        const response = await axios.get(`http://localhost:8000/user/3`);
        const profileData = response.data;

        setFullName(profileData.full_name);
        setUsername(profileData.username);
        setEmail(profileData.email);
        setPassword(profileData.password);
        setBio(profileData.bio);
        setBirthday(profileData.birthday);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>User Profile</h1>
      <div>
        <p>Full Name: {full_name}</p>
        <p>Username: {username}</p>
        <p>Email: {email}</p>
        <p>Password: {password}</p>
        <p>Bio: {bio}</p>
        <p>Birthday: {birthday}</p>
      </div>
    </div>
  );
};
