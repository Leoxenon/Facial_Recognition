export const handleApiError = async (error, operation) => {
    console.error(`${operation} error:`, error);
    
    let message = 'Operation failed, please try again';
    
    if (error.response) {
        try {
            const data = await error.response.json();
            message = data.message || message;
        } catch (e) {
            console.error('Error parsing response:', e);
        }
    } else if (error.request) {
        message = 'Network connection failed, please check your internet';
    }
    
    alert(message);
    return false;
};

export const handleValidationError = (message) => {
    alert(message);
    return false;
}; 