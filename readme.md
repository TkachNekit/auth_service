# RESTful API for Authentication

## Objective 
Develop a REST API for a user authentication and authorization system using Django and Django REST Framework. The system should support user registration, authentication, token refresh, logout, and allow users to retrieve and update their personal information.

Authentication should utilize Access and Refresh tokens.

Refresh Token – A UUID stored in the database, issued for 30 days by default.
Access Token – A JSON Web Token with a default lifespan of 30 seconds.

Clients may request an Access Token refresh at any time, for instance, upon Access Token expiry by providing a valid Refresh Token. In this case, the service returns a new valid pair of Access and Refresh Tokens, resetting their lifespans.

## Required Endpoints Description
### User Registration

```text
Endpoint: /api/me/
Method: GET
Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiZXhhbXBsZVVzZXIiLCJleHAiOjE3MTIxNDYxNDd9.zKobBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA
Response: {"id": 1, "username": "", "email": "user@example.com"}  
```

### Updating Personal Information
```text
Endpoint: /api/me/
Method: PUT
Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiZXhhbXBsZVVzZXIiLCJleHAiOjE3MTIxNDYxNDd9.zKobBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA
Body: {"email: testuser", "password": "xyz", "username": "John Smith"}
Response: {"id": 1, "username": "John Smith", "email": "user@example.com"}
```

### Logout
```text
Endpoint: /api/logout/
Method: POST
Body: {"refresh_token": "eb0464c2-ed6e-4346-a709-042c33946154"}
Response: {"success": "User logged out."}
```

### Access Token Refresh
```text
Endpoint: /api/refresh/
Method: POST
Body: {"refresh_token": "d952527b-caef-452c-8c93-1100214f82e5"}
Response: {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiZXhhbXBsZVVzZXIiLCJleHAiOjE3MTIxNDYxNDd9.zKobBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA", "refresh_token": "eb0464c2-ed6e-4346-a709-042c33946154"}
```

### Authentication (Obtaining Access and Refresh Token)
```text
Endpoint: /api/login/
Method: POST
Body: {"email": "user@example.com", "password": "password"}
Response: {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImV4cCI6MTcxMjE0NTk0NiwiaWF0IjoxNzEyMTQ1OTE2fQ.KX6LM66tC3p3bUCdkWRQkPvariP8tzUfWd8Z13akCPY", "refresh_token": "d952527b-caef-452c-8c93-1100214f82e5"}
```

### User Registration
```text
Endpoint: /api/register/
Method: POST
Body: {"password": "password", "email": "user@example.com"}
Response: {"id": 1, "email": "user@example.com"}
```

## Implementation Requirements 
- RESTful API must be developed with Django and Django REST Framework.
- Access Token is not stored in the database; it’s verified in authentication endpoints without database calls, using the PyJWT library.
- Refresh Token should be stored in the database with its expiry time and linked to a user. This allows for the token to be invalidated when necessary (e.g., when the user logs out).
- Use the django-constance module for managing the lifetimes of Access and Refresh tokens.
- API Documentation: Provide a browsable API with endpoint documentation.
- Tests: Unit tests and integration tests for your API are recommended.
- Deployment: For demonstrating the API’s functionality, you can use free hosting platforms like Heroku, which offer convenient means for deploying Django applications.