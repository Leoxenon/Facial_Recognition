export const validatePassword = (password) => {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*]/.test(password);
    
    if (password.length < minLength) {
        return 'Password length is at least 8 characters';
    }
    if (!hasUpperCase || !hasLowerCase) {
        return 'Password must contain upper and lower case letters';
    }
    if (!hasNumbers) {
        return 'Password must contain numbers';
    }
    if (!hasSpecialChar) {
        return 'Password must contain special characters';
    }
    
    return null;
}; 