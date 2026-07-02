# CarePortal Backend (Progress Report 1 Scaffold)

This folder contains a working backend scaffold focused on the two priorities for Progress Report #1:

- Authentication (register, login, token-protected profile route)
- Centralized API error handling (consistent JSON error responses)

## Stack

- Python
- FastAPI
- JWT (`python-jose`)
- Password hashing (`passlib` + bcrypt)

## What is Implemented

- `POST /api/v1/auth/register`: create user account (currently in-memory)
- `POST /api/v1/auth/login`: validate credentials and issue access token
- `GET /api/v1/auth/me`: protected endpoint that validates bearer token
- Global exception handling for:
  - business errors (conflict/auth/not found)
  - validation errors (422)
  - unexpected errors (500)
- `GET /health`: simple health check endpoint

## Run Locally

1. Create and activate virtual environment.
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

## Notes for Next Iteration

- Replace in-memory auth store with MySQL/PostgreSQL persistence.
- Add refresh tokens and logout/revocation strategy.
- Add role-based authorization for patient/admin/doctor workflows.
- Add integration tests for auth and error response contracts.
