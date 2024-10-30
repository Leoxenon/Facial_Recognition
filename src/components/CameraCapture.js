import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';

function CameraCapture({ onCapture }) {
  const webcamRef = useRef(null);
  const [error, setError] = useState('');
  const [status, setStatus] = useState('');

  const handleCapture = useCallback(async () => {
    try {
      setStatus('Processing image...');
      setError('');

      const imageSrc = webcamRef.current.getScreenshot();
      if (!imageSrc) {
        throw new Error('Failed to capture image');
      }

      const response = await fetch('http://localhost:5000/detect_faces/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: imageSrc
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Server response:', errorData);
        throw new Error(errorData.error || 'Face detection failed');
      }

      const data = await response.json();
      console.log('Face detection response:', data);
      
      if (data.faces_detected === 1) {
        setStatus('Face detected successfully');
        onCapture(imageSrc);
      } else if (data.faces_detected === 0) {
        throw new Error('No face detected in image');
      } else {
        throw new Error('Multiple faces detected. Please ensure only one face is visible');
      }
    } catch (error) {
      setError(error.message);
      setStatus('');
      console.error('Face detection error:', error);
    }
  }, [onCapture]);

  return (
    <div className="camera-container">
      <Webcam
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        mirrored={true}
        videoConstraints={{
          width: 720,
          height: 480,
          facingMode: "user"
        }}
      />
      <button onClick={handleCapture} className="btn btn-primary">拍照</button>
      {status && <div className="status-text status-info">{status}</div>}
      {error && <div className="status-text status-error">{error}</div>}
    </div>
  );
}

export default CameraCapture;
