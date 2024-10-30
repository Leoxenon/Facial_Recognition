class AuthenticationError(Exception):
    def __init__(self, message, status_code=401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class FaceRecognitionError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message) 