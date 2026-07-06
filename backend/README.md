# CarePortal Backend (Progress Report 1 Scaffold)

This folder has a working backend scaffold focused on the two main priorities for Progress Report #1:

- Authentication (register, login, token-protected profile route)
- Centralized API error handling (consistent JSON error responses)

## Stack

- Python
- FastAPI
- JWT (`python-jose`)
- Password hashing (`passlib` + bcrypt)

## What is Implemented

- `POST /api/v1/auth/register`: creates a user account (currently stored in memory)
- `POST /api/v1/auth/login`: checks login info and returns an access token
- `GET /api/v1/auth/me`: protected route that checks bearer token
- Global exception handling for:
  - business errors (conflict/auth/not found)
  - validation errors (422)
  - unexpected errors (500)
- `GET /health`: basic health check endpoint

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment template:

```bash
cp .env.example .env
```

4. Start API server:

```bash
uvicorn app.main:app --reload
```

5. Open docs at `http://127.0.0.1:8000/docs`

## Manual Testing (Local)

You can test everything through Swagger UI at `http://127.0.0.1:8000/docs`.

### 1) Check API is running

- Call `GET /health`
- Expected result: status is `ok`

### 2) Register a user

- Call `POST /api/v1/auth/register`
- Example body:

```json
{
  "full_name": "Test Student",
  "email": "student@example.com",
  "password": "Password123"
}
```

- Expected result: returns new user info (id, full_name, email)

### 3) Login and get token

- Call `POST /api/v1/auth/login` with same email/password
- Expected result: returns `access_token` and `token_type`

### 4) Test protected route

- Copy `access_token` from login response
- In Swagger, click **Authorize** and paste token as `Bearer <token>`
- Call `GET /api/v1/auth/me`
- Expected result: returns the logged-in user info

### 5) Test error handling

- Duplicate register:
  - Register the same email again
  - Expected: 409 conflict-style error response
- Invalid login:
  - Use wrong password in login
  - Expected: 401 authentication error response
- Validation error:
  - Send invalid email format
  - Expected: 422 validation error response

## Notes for Next Iteration

- Replace in-memory auth store with MySQL/PostgreSQL persistence.
- Add refresh tokens and logout/revocation strategy.
- Add role-based authorization for patient/admin/doctor workflows.
- Add integration tests for auth and error response contracts.
