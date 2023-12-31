import { useState, useEffect } from "react";
import axios from "axios";
import { useUserId } from './customhooks/userIDHook';

export const ProfilePage = () => {
  const [full_name, setFullName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [bio, setBio] = useState('');
  const [birthday, setBirthday] = useState('');

  const { userId } = useUserId();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/user/${userId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        const profileData = response.data;

        if (profileData) {
          setFullName(profileData.full_name);
          setUsername(profileData.username);
          setEmail(profileData.email);
          setPassword(profileData.password);
          setBio(profileData.bio);
          setBirthday(profileData.birthday);
        } else {
          console.error('No profile data returned from API');
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [userId]);

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
