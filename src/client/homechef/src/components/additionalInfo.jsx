import {useState} from "react";
import axios from 'axios';
import { useUserId } from './customhooks/userIDHook';

export const AdditionalInfo = () => {
    const [full_name, setFullName] = useState('');
    const [bio, setBio] = useState('');
    const [birthday, setBirthday] = useState('');
    const [error, setError] = useState('');

    const {userId} = useUserId();



    const handleAdditionalInfo = async () => {
        // Check if birthday is a valid date
        if (birthday && isNaN(Date.parse(birthday))) {
            setError('Invalid birthday');
            return;
        }

        // Check if the entered year is more than 110 years from the current year
        const currentYear = new Date().getFullYear();
        const enteredYear = new Date(birthday).getFullYear();
        if (birthday && currentYear - enteredYear > 110) {
            setError('Invalid birthday');
            return;
        }
        //Check if the date is in the future
        const currentDate = new Date();
        const enteredDate = new Date(birthday);
        if (birthday && enteredDate > currentDate) {
            setError('Invalid birthday');
            return;
        }

        let age = currentDate.getFullYear() - enteredDate.getFullYear();
        const m = currentDate.getMonth() - enteredDate.getMonth();
        if (birthday && (m < 0 || (m === 0 && currentDate.getDate() < enteredDate.getDate()))) {
            age--;
        }
        if (birthday && age < 13) {
            setError('You must be at least 13 years old to submit');
            return;
        }

        try {
            const response = await axios.patch(
                `${process.env.REACT_APP_API_URL}/user/${userId}`,
                {
                    full_name: full_name,
                    bio: bio,
                    birthday: birthday
                },
                {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    },
                    withCredentials: true,
                }
            );

            if (response.status === 200) {
                console.log('successful');
                window.location.href = '/login';
            }
        } catch (error) {
            console.error('Registration error:', error);
        }
    }

    return (
        <div className="registration-container">
            <form onSubmit={handleAdditionalInfo}>
                <div>
                    <h3>AdditionalInfo</h3>
                    {error && <p>{error}</p>} 
                    <div className="input-container">
                        <label>Full name:</label>
                        <input
                            type="text"
                            placeholder="Full name"
                            value={full_name}
                            onChange={(e) => setFullName(e.target.value)}
                        />
                    </div>
                    <div className="input-container">
                        <label>Bio:</label>
                        <input
                            type="text"
                            placeholder="bio"
                            value={bio}
                            onChange={(e) => setBio(e.target.value)}
                        />
                    </div>
                    <div className="input-container">
                        <label>Birthday:</label>
                        <input
                            type="date"
                            placeholder="birthday"
                            value={birthday}
                            onChange={(e) => {
                                setBirthday(e.target.value);
                                setError('');
                            }}
                        />
                    </div>
                    <button>Next</button>
                </div>
            </form>
        </div>
    );
}
