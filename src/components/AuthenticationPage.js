import React, { useState } from 'react';
import CameraCapture from './CameraCapture';
import '../styles/main.css';

const AuthenticationPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [faceImage, setFaceImage] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [status, setStatus] = useState('');

    const handleAuthentication = async (username, password, faceImage) => {
        try {
            setLoading(true);
            setError('');
            setStatus('Verifying credentials...');

            const response = await fetch('http://localhost:5000/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    username,
                    password,
                    faceImage
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Authentication failed');
            }

            if (data.success) {
                setStatus('Login successful! Redirecting...');
                localStorage.setItem('token', data.token);
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            } else {
                throw new Error(data.message || 'Authentication failed');
            }
        } catch (err) {
            setError(err.message);
            setStatus('');
            return false;
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!username || !password || !faceImage) {
            setStatus('Please fill in all required fields');
            return;
        }
        handleAuthentication(username, password, faceImage);
    };

    const handleCapture = (imageSrc) => {
        setFaceImage(imageSrc);
        setStatus('Face image captured successfully');
    };

    return (
        <div className="container">
            <div className="card">
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Username</label>
                        <input
                            className="form-input"
                            type="text"
                            placeholder="Enter username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            className="form-input"
                            type="password"
                            placeholder="Enter password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <div className="camera-section">
                        <label className="form-label">Face Verification</label>
                        <CameraCapture onCapture={handleCapture} />
                        {faceImage && (
                            <img src={faceImage} alt="Face preview" className="preview-image" />
                        )}
                    </div>

                    {error && (
                        <div className="status-text status-error">
                            {error}
                        </div>
                    )}
                    {status && !error && (
                        <div className="status-text status-info">
                            {status}
                        </div>
                    )}

                    <button 
                        type="submit"
                        className="btn btn-primary"
                        disabled={loading || !faceImage}
                    >
                        {loading ? 'Verifying...' : 'Login'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default AuthenticationPage;
