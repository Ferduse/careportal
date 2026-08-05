# CarePortal Backend

## Stack

- Python
- FastAPI
- JWT (`python-jose`)
- Password hashing (`passlib` + bcrypt)

## What is Implemented

- `POST /api/v1/auth/register`: creates a user account (in memory)
- `POST /api/v1/auth/login`: returns access token and refresh token
- `POST /api/v1/auth/refresh`: refreshes access token
- `POST /api/v1/auth/logout`: revokes refresh token
- `GET /api/v1/auth/me`: protected route that checks bearer token
- `PUT /api/v1/patient/profile`: create/update patient profile
- `GET /api/v1/patient/profile`: read patient profile
- `POST /api/v1/appointments`: create appointment
- `GET /api/v1/appointments`: list appointments for current user
- `PUT /api/v1/appointments/{appointment_id}`: update appointment
- `POST /api/v1/appointments/{appointment_id}/cancel`: cancel appointment
- `POST /api/v1/medical-history`: create medical history record
- `GET /api/v1/medical-history`: list history records
- `PUT /api/v1/medical-history/{record_id}`: update history record
- `POST /api/v1/predictions`: run diabetes risk prediction (rule-based placeholder)
- `GET /api/v1/predictions`: list prediction history
- Global exception handling for:
  - business errors (conflict/auth/not found)
  - validation errors (422)
  - unexpected errors (500)
- Simple request logging middleware
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

### 3) Login and get tokens

- Call `POST /api/v1/auth/login` with same email/password
- Expected result: returns `access_token`, `refresh_token`, and `token_type`

### 4) Test protected route

- Copy `access_token` from login response
- In Swagger, click **Authorize** and paste token as `Bearer <token>`
- Call `GET /api/v1/auth/me`
- Expected result: returns the logged-in user info

### 5) Test patient profile

- Call `PUT /api/v1/patient/profile`
- Then call `GET /api/v1/patient/profile`

### 6) Test appointments

- Create appointment with `POST /api/v1/appointments`
- List with `GET /api/v1/appointments`
- Update with `PUT /api/v1/appointments/{appointment_id}`
- Cancel with `POST /api/v1/appointments/{appointment_id}/cancel`

### 7) Test medical history

- Create with `POST /api/v1/medical-history`
- List with `GET /api/v1/medical-history`
- Update with `PUT /api/v1/medical-history/{record_id}`

### 8) Test predictions

- Submit inputs to `POST /api/v1/predictions`
- Check history with `GET /api/v1/predictions`

### 9) Test session endpoints

- Call `POST /api/v1/auth/refresh` with refresh token from login
- Call `POST /api/v1/auth/logout` with refresh token

### 10) Test error handling

- Duplicate register:
  - Register the same email again
  - Expected: 409 conflict-style error response
- Invalid login:
  - Use wrong password in login
  - Expected: 401 authentication error response
- Validation error:
  - Send invalid email format
  - Expected: 422 validation error response


