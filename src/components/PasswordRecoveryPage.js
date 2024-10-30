import React, { useState } from 'react';
import { handlePasswordRecovery } from '../utils';
import CameraCapture from './CameraCapture';
import '../styles/main.css';

const PasswordRecoveryPage = () => {
    const [username, setUsername] = useState('');
    const [faceImage, setFaceImage] = useState(null);
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [step, setStep] = useState(1);
    const [status, setStatus] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleCapture = (imageSrc) => {
        setFaceImage(imageSrc);
        setStatus('Face image captured successfully');
    };

    const handleVerify = async (e) => {
        e.preventDefault();
        if (!username || !faceImage) {
            setStatus('Please provide username and face image');
            return;
        }
        setIsLoading(true);
        setStatus('Verifying identity...');
        
        try {
            const response = await fetch('http://localhost:5000/api/auth/verify-identity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, faceImage }),
            });
            
            const data = await response.json();
            if (data.success) {
                setStep(2);
                setStatus('Identity verified. Please set your new password.');
            } else {
                setStatus(`Verification failed: ${data.message}`);
            }
        } catch (error) {
            setStatus('Verification failed. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleResetPassword = async (e) => {
        e.preventDefault();
        if (newPassword !== confirmPassword) {
            setStatus('Passwords do not match');
            return;
        }
        setIsLoading(true);
        setStatus('Resetting password...');
        
        const success = await handlePasswordRecovery(username, faceImage, newPassword);
        setIsLoading(false);
        
        if (success) {
            setStatus('Password reset successful! Redirecting to login...');
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        }
    };

    return (
        <div className="container">
            <div className="card">
                <h2>{step === 1 ? 'Verify Identity' : 'Reset Password'}</h2>
                
                {step === 1 ? (
                    <form onSubmit={handleVerify}>
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
                        
                        <div className="camera-section">
                            <label className="form-label">Face Verification</label>
                            <CameraCapture onCapture={handleCapture} />
                            {faceImage && (
                                <img src={faceImage} alt="Face preview" className="preview-image" />
                            )}
                        </div>
                        
                        <button 
                            type="submit"
                            className="btn btn-primary"
                            disabled={isLoading || !faceImage}
                        >
                            {isLoading ? 'Verifying...' : 'Verify Identity'}
                        </button>
                    </form>
                ) : (
                    <form onSubmit={handleResetPassword}>
                        <div className="form-group">
                            <label className="form-label">New Password</label>
                            <input
                                className="form-input"
                                type="password"
                                placeholder="Enter new password"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                required
                            />
                        </div>
                        
                        <div className="form-group">
                            <label className="form-label">Confirm Password</label>
                            <input
                                className="form-input"
                                type="password"
                                placeholder="Re-enter new password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                            />
                        </div>
                        
                        <button 
                            type="submit"
                            className="btn btn-primary"
                            disabled={isLoading}
                        >
                            {isLoading ? 'Resetting...' : 'Reset Password'}
                        </button>
                    </form>
                )}
                
                {status && (
                    <div className={`status-text ${
                        status.includes('successful') ? 'status-success' : 
                        status.includes('failed') ? 'status-error' : 'status-info'
                    }`}>
                        {status}
                    </div>
                )}
            </div>
        </div>
    );
};

export default PasswordRecoveryPage;
