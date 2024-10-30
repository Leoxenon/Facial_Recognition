import React, { useState } from 'react';
import { handleRegister } from '../utils';
import CameraCapture from './CameraCapture';
import '../styles/main.css';

function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [faceImage, setFaceImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setStatus('Passwords do not match');
      return;
    }
    setIsLoading(true);
    setStatus('Processing registration...');
    const success = await handleRegister(username, password, faceImage);
    setIsLoading(false);
    if (success) {
      setStatus('Registration successful! Redirecting to login...');
      setTimeout(() => {
        window.location.href = '/login';
      }, 2000);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Create Account</h2>
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

          <div className="form-group">
            <label className="form-label">Confirm Password</label>
            <input
              className="form-input"
              type="password"
              placeholder="Confirm password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <div className="camera-section">
            <label className="form-label">Face Recognition Setup</label>
            <CameraCapture onCapture={(imageSrc) => setFaceImage(imageSrc)} />
            {faceImage && (
              <img src={faceImage} alt="Face preview" className="preview-image" />
            )}
          </div>

          {status && (
            <div className={`status-text ${
              status.includes('successful') ? 'status-success' : 'status-error'
            }`}>
              {status}
            </div>
          )}

          <button 
            type="submit"
            className="btn btn-primary"
            disabled={isLoading || !faceImage}
          >
            {isLoading ? 'Registering...' : 'Register'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Register;
