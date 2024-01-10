import {useState} from "react";
import axios from 'axios';
import { useUserId } from './customhooks/userIDHook';
import './universalFormStyle.css'

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
            const response = await axios.put(
                `http://localhost:8000/user/update/${userId}`,
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
                window.location.href = '/profilepage';
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
              console.error('Additional info error:', error);
        }
    }

    return (
        <div className="wrapper">
            <div className="logoAndMoto">
                <div>
                <img className="logo" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" alt="logo" width={500} height={187}/>
                </div>
                <div className='moto'><p>The ultimate kitchen hack.</p></div>
        </div>
            <div className="form-container">
                <form className="form" onSubmit={handleAdditionalInfo}>
                    <div className="form-content">
                        <h3 className="form-title">Additional Info</h3>
                        <p className={`error ${error ? 'visible' : 'hidden'}`}>{error}</p>
                        <div className="form-group">
                            <label>Full name:</label>
                            <input
                                className="form-control"
                                type="text"
                                placeholder="Full name"
                                value={full_name}
                                onChange={(e) => setFullName(e.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label>Bio:</label>
                            <input
                                className="form-control"
                                type="text"
                                placeholder="bio"
                                value={bio}
                                onChange={(e) => setBio(e.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label>Birthday:</label>
                            <input
                                className="form-control"
                                type="date"
                                placeholder="birthday"
                                value={birthday}
                                onChange={(e) => {
                                    setBirthday(e.target.value);
                                    setError('');
                                }}
                            />
                        </div>
                        <div className='form-group'>
                            <button className='btn'>Next</button>
                        </div>
                    </div>
                </form>
            </div>
            
        </div>
    );
}
