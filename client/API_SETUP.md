# API Setup and Client-Server Connection

## Overview

The React Native client has been configured to connect to the FastAPI backend running on `http://127.0.0.1:8003`.

## Architecture

### API Service Layer (`services/api.js`)
- **ApiClient**: Centralized API communication with error handling and retries
- **Configuration**: Base URL, timeouts, and retry attempts
- **Endpoints**: All API endpoints defined as constants
- **Authentication**: Automatic token management

### Authentication Service (`services/auth.js`)
- **AuthService**: Handles login, logout, and session management
- **Token Storage**: Secure token persistence using AsyncStorage
- **Session Management**: Automatic token validation and refresh

## Key Features

### ✅ Authentication Flow
- User registration and login
- JWT token management
- Session persistence
- Automatic logout on token expiration

### ✅ API Communication
- Centralized API client with error handling
- Automatic retry logic with exponential backoff
- Proper error messages and validation
- Support for file uploads (FormData)

### ✅ User Preferences
- Load and save user preferences
- Offline support with sync queue
- Automatic preference synchronization

## Testing the Connection

### 1. Start the Backend Server
```bash
cd backend
venv\Scripts\uvicorn.exe app.main:app --reload --host 127.0.0.1 --port 8003
```

### 2. Test API Endpoints
You can test the API endpoints in your browser:
- **Health Check**: `http://127.0.0.1:8003/`
- **API Docs**: `http://127.0.0.1:8003/docs`
- **OpenAPI Schema**: `http://127.0.0.1:8003/openapi.json`

### 3. Test Client-Server Communication
The client includes a test script (`test_connection.js`) that can be used to verify the connection:

```javascript
import { testApiConnection } from './test_connection';

// Run the test
testApiConnection().then(success => {
  if (success) {
    console.log('✅ Client-server connection working!');
  } else {
    console.log('❌ Connection failed');
  }
});
```

## Available API Endpoints

### Authentication
- `POST /users/register` - Register new user
- `POST /users/login` - Login user

### Users
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get specific user
- `GET /users/me/preferences` - Get user preferences
- `PUT /users/me/preferences` - Update user preferences

### Books
- `GET /books/` - List user's books
- `GET /books/{book_id}` - Get specific book
- `POST /books/upload` - Upload EPUB file
- `DELETE /books/{book_id}` - Delete book
- `GET /books/{book_id}/markup` - Get book markup
- `GET /books/jobs/{job_id}/status` - Get processing status
- `GET /books/jobs/{job_id}/result` - Get processing result

### Analytics
- `GET /analytics/events` - Get analytics events
- `POST /analytics/events` - Post analytics events

## Configuration

### API Configuration (`services/api.js`)
```javascript
const API_CONFIG = {
  BASE_URL: 'http://127.0.0.1:8003',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
};
```

### Storage Keys (`services/auth.js`)
```javascript
const STORAGE_KEYS = {
  AUTH_TOKEN: 'cinei_auth_token',
  USER_DATA: 'cinei_user_data',
  REMEMBER_ME: 'cinei_remember_me',
};
```

## Error Handling

The API client includes comprehensive error handling:
- **Network errors**: Automatic retry with exponential backoff
- **Authentication errors**: Automatic token clearing and logout
- **Validation errors**: Detailed error messages from backend
- **Timeout handling**: Configurable request timeouts

## Next Steps

1. **Test the connection** using the test script
2. **Test user registration and login** in the app
3. **Test book upload and processing**
4. **Test the full reading experience**

## Troubleshooting

### Common Issues

1. **Connection refused**: Make sure the backend server is running on port 8003
2. **CORS errors**: The backend should handle CORS for React Native
3. **Authentication failed**: Check that the backend JWT configuration is correct
4. **File upload issues**: Ensure the backend accepts multipart/form-data

### Debug Mode

Enable debug logging by adding to your React Native app:
```javascript
// In your App.js or index.js
if (__DEV__) {
  console.log('API Base URL:', API_CONFIG.BASE_URL);
}
```
