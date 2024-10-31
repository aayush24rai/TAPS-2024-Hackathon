import './Login.css'
import React from 'react';
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import axios from 'axios';

function Login() {
    const [email, setEmail] = useState('');
    const navigate = useNavigate();

    const navigateToDashboard = () => {
        console.log(email);

        axios.get("http://127.0.0.1:5000/login")
            .then(response => console.log(response))
            .catch(error => console.log(error))

        navigate("/Map", {
            state: { "email": email}
        });
    }

    return (
        <div className='login-container'>
            <div className='email-container'>
                <h1 className='login-header'>Email</h1>
                <input className='email-i' placeholder='Enter your email' value={email} onChange={(event) => setEmail(event.target.value)} />
                <div className='btn'>
                    <button className='submit-btn' onClick={navigateToDashboard}>Enter</button>
                </div>
            </div>
        </div>
    )
}

export default Login