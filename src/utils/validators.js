export const validatePassword = (password) => {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*]/.test(password);
    
    if (password.length < minLength) {
        return '密码长度至少为8个字符';
    }
    if (!hasUpperCase || !hasLowerCase) {
        return '密码必须包含大小写字母';
    }
    if (!hasNumbers) {
        return '密码必须包含数字';
    }
    if (!hasSpecialChar) {
        return '密码必须包含特殊字符';
    }
    
    return null;
}; 