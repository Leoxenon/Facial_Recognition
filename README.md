# Face Recognition Authentication System

A secure cloud-based authentication system leveraging Amazon Rekognition API for facial recognition and authentication.

## Table of Contents
- [System Requirements](#system-requirements)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)
- [Security Features](#security-features)
- [Development Guidelines](#development-guidelines)
- [Deployment](#deployment)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)
- [Performance Considerations](#performance-considerations)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)
- [Version History](#version-history)

## System Requirements

- CPU: Dual-core processor or better
- RAM: 4GB minimum, 8GB recommended
- Storage: 1GB free space
- Camera: HD webcam (720p or better)
- Network: Stable internet connection
- OS: Windows 10+, macOS 10.15+, or Ubuntu 20.04+

## Prerequisites

- Node.js >= 12.0.0
- Python >= 3.8
- AWS Account with appropriate permissions
- Modern web browser with camera access
- Git

## Quick Start

1. Clone the repository
```bash
git clone https://github.com/Leoxenon/Facial_Recognition.git
cd Facial_Recognition
```

2. Install frontend dependencies
```bash
npm install
```

3. Set up Python virtual environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Configure environment variables
Create a `.env` file in the root directory:
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
S3_BUCKET=your_bucket_name
COLLECTION_ID=facial_collection
DYNAMODB_TABLE=facial_database
```

5. Install backend dependencies
```bash
cd backend && pip install -r requirements.txt
```

6. Configure AWS
- Create `.env` file with AWS credentials
- Configure S3 bucket and DynamoDB table

7. Run Application
```bash
npm start
cd backend && flask run
```

## Features

- User registration with facial enrollment
- Face recognition-based login
- Real-time camera face capture
- Face comparison and matching
- Secure password recovery with facial verification
- Multi-factor authentication (Password + Face)
- Real-time face detection confidence scoring
- Secure session management
- Input validation and sanitization
- Rate limiting protection (60 requests per minute)
- Swagger UI API documentation
- Cross-Origin Resource Sharing (CORS) support
- JWT-based session management
- Face quality validation
- Comprehensive error handling and logging

## Technology Stack

### Frontend
- React 17.0.2
- React Router DOM 5.2.0
- React Webcam 7.2.0
- HTML5/CSS3
- ES6+ JavaScript

### Backend
- Python Flask
- Flask-CORS
- AWS SDK (Boto3)
- Amazon Web Services
  - Amazon Rekognition
  - Amazon S3
  - Amazon DynamoDB
  - AWS IAM
  
### Backend Additional Components
- Flask-RESTX for Swagger UI
- PyJWT for token management
- Werkzeug for password hashing
- Python-dotenv for environment management

### Development Tools
- Node.js
- npm
- Python virtual environment
- Git version control

### Backend Additional Components
- Flask-RESTX for Swagger UI
- PyJWT for token management
- Werkzeug for password hashing
- Python-dotenv for environment management

## Architecture

The system follows a microservices architecture with:
- Frontend React SPA
- Flask REST API backend
- AWS cloud services integration
- Secure API endpoints
- Stateless authentication

## Database Schema

### DynamoDB Table Structure
- Table Name: facial_database
- Primary Key: FaceID
- Attributes:
  - FaceID (String): Unique identifier for the face
  - username (String): User's username
  - password_hash (String): Hashed password
  - ImageURL (String): S3 URL of the face image
  - Confidence (Number): Face detection confidence score
```json
{
  "FaceID": "string (Primary Key)",
  "Username": "string",
  "password_hash": "string",
  "ImageURL": "string",
  "Confidence": "number",
  "CreatedAt": "timestamp",
  "LastLogin": "timestamp"
}
```

## API Documentation

### Authentication Endpoints
1. POST /api/auth/register
   - Purpose: Register new user
   - Request Body: { username, password, faceImage }
   - Response: { success, message, face_id? }

2. POST /api/auth/login
   - Purpose: User authentication
   - Request Body: { username, password, faceImage }
   - Response: { success, message, face_verified }

3. POST /api/auth/recover-password
   - Purpose: Password recovery
   - Request Body: { username, faceImage, newPassword }
   - Response: { success, message }

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
    "username": string,
    "password": string,
    "face_image": base64_string
}
```

Response:
```json
{
    "success": boolean,
    "message": string
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": string,
    "password": string,
    "face_image": base64_string
}
```

Response:
```json
{
    "success": boolean,
    "message": string,
    "face_verified": boolean
}
```

#### Password Recovery
```http
POST /api/auth/recover-password
Content-Type: application/json

{
    "username": string,
    "face_image": base64_string,
    "new_password": string
}
```

Response:
```json
{
    "success": boolean,
    "message": string
}
```

### Face Recognition Endpoints
1. POST /detect_faces
   - Purpose: Detect faces in image
   - Request: Multipart form data with 'file'
   - Response: { faces_detected, details }

2. POST /compare_faces
   - Purpose: Compare two face images
   - Request: Multipart form data with 'source' and 'target' files
   - Response: { matches, details }

3. POST /upload_face
   - Purpose: Upload and index a face
   - Request: Multipart form data with 'file'
   - Response: { message, face_id }

4. POST /api/auth/refresh-token - Token refresh

#### Detect Faces
```http
POST /detect_faces/
Content-Type: multipart/form-data

file: image_file
```

Response:
```json
{
    "faces_detected": number,
    "details": array
}
```

#### Compare Faces
```http
POST /compare_faces/
Content-Type: multipart/form-data

source: image_file
target: image_file
```

Response:
```json
{
    "matches": number,
    "details": [
        {
            "Similarity": number,
            "Face": object
        }
    ]
}
```

#### Upload Face
```http
POST /upload_face/
Content-Type: multipart/form-data

file: image_file
```

Response:
```json
{
    "message": string,
    "face_id": string
}
```

### Error Responses

All endpoints may return the following error format:
```json
{
    "error": string,
    "code": number
}
```

Common error codes:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 500: Internal Server Error

### Authentication

All protected endpoints require a Bearer token:
```http
Authorization: Bearer <token>
```

### Rate Limiting

- Maximum requests: 100 per minute per IP
- Face detection timeout: 30 seconds
- Maximum image size: 1MB

### API Endpoints
- POST /api/auth/register - User registration
- POST /api/auth/login - User authentication
- POST /api/auth/recover-password - Password recovery
- POST /api/auth/refresh-token - Token refresh
- POST /api/detect_faces - Face detection
- POST /api/compare_faces - Face comparison
- POST /api/upload_face - Face enrollment

## Security Features

- AWS IAM role-based access control
- HTTPS/TLS encryption
- CORS protection
- Input sanitization
- Password hashing
- Face confidence threshold validation
- Session management
- Error handling and logging

### Authentication Security
- Multi-factor authentication combining:
  - Username/password
  - Facial recognition
  - Confidence score threshold
- Password hashing using Werkzeug security
- Face detection confidence validation

### AWS Security
- IAM role-based access
- S3 bucket encryption
- DynamoDB encryption at rest

### Rate Limiting
- Maximum 60 requests per minute per IP
- Time window: 60 seconds
- Automatic request cleanup
Reference: backend/middleware/rate_limit.py (lines 6-25)

### Request Validation
- Required field validation
- Image format validation
- Face quality checks
Reference: backend/middleware/validators.py (lines 1-54)

## Development Guidelines

1. Code Style
   - Follow PEP 8 for Python
   - ESLint configuration for JavaScript
   - Component-based architecture for React

2. Git Workflow
   - Feature branch workflow
   - Pull request reviews
   - Semantic versioning

3. Testing
   - Unit tests for backend services
   - Integration tests for API endpoints
   - Frontend component testing

## Deployment

1. AWS Infrastructure Setup
   - Configure S3 bucket
   - Set up DynamoDB tables
   - Create Rekognition collection
   - Configure IAM roles

2. Application Deployment
   - Build frontend assets
   - Configure production environment
   - Set up monitoring and logging

## Error Handling

Common error codes and solutions:
- 400: Invalid request format
- 401: Authentication failed
- 403: Insufficient permissions
- 500: Internal server error

### Custom Exception Types
- AuthenticationError: Authentication-related failures
- FaceRecognitionError: Face detection/recognition issues
Reference: backend/exceptions/auth_exceptions.py (lines 1-10)

### Global Error Handler
- Centralized error handling
- Consistent error response format
Reference: backend/app.py (lines 24-31)

## Troubleshooting

Common issues and solutions:

1. Camera Access Issues
   - Ensure browser permissions are granted
   - Check if another application is using the camera
   - Verify webcam drivers are up to date

2. Face Detection Problems
   - Ensure proper lighting
   - Face should be clearly visible
   - Maintain appropriate distance from camera

3. AWS Connection Issues
   - Verify AWS credentials
   - Check network connectivity
   - Confirm AWS service quotas

## Performance Considerations

- Image size: Recommended max 1MB per image
- Face detection timeout: 30 seconds
- Minimum face confidence score: 90%
- Maximum concurrent users: 100
- API rate limits: 100 requests per minute

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- GitHub Issues
- Stack Overflow tag: `facial-recognition-auth`
- AWS Support

## Authors

- [@Leoxenon](https://github.com/Leoxenon)

## Acknowledgments

- AWS SDK Documentation
- React Documentation
- Flask Documentation
- OpenCV Community

## Version History

- v1.0.0 (2024-10-19)
  - Initial release
  - Basic face recognition features
  - AWS integration

- v1.0.1 (2024-10-29)
  - Performance improvements
  - Bug fixes in face detection
  - Enhanced error handling