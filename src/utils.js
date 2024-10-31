import { handleApiError, handleValidationError } from './utils/errorHandler';

export const handleImageUpload = (file, setFaceImage) => {
    if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
            setFaceImage(reader.result);
        };
        reader.readAsDataURL(file);
    }
};

export const handleRegister = async (username, password, faceImage) => {
    try {
        const response = await fetch('http://localhost:5000/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password, faceImage }),
        });
        const data = await response.json();
        if (response.ok) {
            return { success: true, data };
        }
        return handleApiError(new Error(data.message), 'Registration');
    } catch (error) {
        return handleApiError(error, 'Registration');
    }
};

export const handleAuthentication = async (username, password, faceImage) => {
    try {
        if (!username || !password || !faceImage) {
            return handleValidationError('Please fill in all fields');
        }
        
        const response = await fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                username: validateInput(username), 
                password, 
                faceImage 
            }),
        });
        
        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('authToken', data.token);
            return true;
        }
        return handleApiError(new Error(data.message), 'Login');
    } catch (error) {
        return handleApiError(error, 'Login');
    }
};

export const handlePasswordRecovery = async (username, faceImage, newPassword) => {
    try {
        const response = await fetch('http://localhost:5000/api/auth/recover-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, faceImage, newPassword }),
        });
        const data = await response.json();
        if (response.ok) {
            return true;
        }
        return handleApiError(new Error(data.message), 'Password recovery');
    } catch (error) {
        return handleApiError(error, 'Password recovery');
    }
};

export const validateInput = (input) => {
    return input.replace(/[<>&'"]/g, '');
};


