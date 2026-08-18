# CarePortal Frontend-Backend Integration Notes

## Why This File Exists
This document explains exactly what was changed to connect the frontend to the backend APIs.

It has two layers:
- ELI5 sections for fast understanding.
- Deep dive sections with code citations.

---

## High-Level Summary
Before these changes, most frontend pages used browser storage only and did not call backend APIs.

After these changes:
- Login and register now call backend auth endpoints.
- Appointments create, list, edit, and cancel now call backend endpoints.
- Medical history load, add, and edit now call backend endpoints.
- Dashboard now pulls real data from backend endpoints.
- Prediction still calls backend, now through the shared API client.
- Risk history now loads from backend prediction history.

---

## ELI5: What Changed

### ELI5: One helper talks to backend
Think of this as one universal phone line for all frontend API calls.
- It knows where the backend lives.
- It automatically attaches login token when needed.
- It translates backend errors into readable messages.

Code:
- [src/api/client.js](src/api/client.js#L1)
- [src/api/client.js](src/api/client.js#L4)
- [src/api/client.js](src/api/client.js#L16)
- [src/api/client.js](src/api/client.js#L33)
- [src/api/client.js](src/api/client.js#L42)
- [src/api/client.js](src/api/client.js#L52)

### ELI5: Login now checks real backend
Before: it compared email and password from browser storage.

Now:
- It calls backend login.
- Saves access and refresh tokens.
- Calls profile endpoint to fetch current user.

Code:
- [src/pages/Login/Login.jsx](src/pages/Login/Login.jsx#L8)
- [src/pages/Login/Login.jsx](src/pages/Login/Login.jsx#L23)
- [src/pages/Login/Login.jsx](src/pages/Login/Login.jsx#L29)
- [src/pages/Login/Login.jsx](src/pages/Login/Login.jsx#L34)
- [src/pages/Login/Login.jsx](src/pages/Login/Login.jsx#L37)

### ELI5: Register now creates user in backend
Before: it only saved a user in browser storage.

Now:
- It sends name, email, and password to backend register endpoint.
- Keeps a local user snapshot for UI display.

Code:
- [src/pages/Register/Register.jsx](src/pages/Register/Register.jsx#L8)
- [src/pages/Register/Register.jsx](src/pages/Register/Register.jsx#L25)
- [src/pages/Register/Register.jsx](src/pages/Register/Register.jsx#L36)

### ELI5: Appointments now use real server data
Before: appointments only lived in browser storage.

Now:
- Booking sends appointment data to backend.
- Upcoming page loads list from backend.
- Edit calls backend update endpoint.
- Cancel calls backend cancel endpoint.

Code:
- [src/pages/Appointment/Appointment.jsx](src/pages/Appointment/Appointment.jsx#L5)
- [src/pages/Appointment/Appointment.jsx](src/pages/Appointment/Appointment.jsx#L51)
- [src/pages/Appointment/Appointment.jsx](src/pages/Appointment/Appointment.jsx#L68)
- [src/pages/Appointment/UpcomingAppointments.jsx](src/pages/Appointment/UpcomingAppointments.jsx#L13)
- [src/pages/Appointment/UpcomingAppointments.jsx](src/pages/Appointment/UpcomingAppointments.jsx#L74)
- [src/pages/Appointment/UpcomingAppointments.jsx](src/pages/Appointment/UpcomingAppointments.jsx#L117)
- [src/pages/Appointment/UpcomingAppointments.jsx](src/pages/Appointment/UpcomingAppointments.jsx#L146)

### ELI5: Medical history now talks to backend
Before: medical history was browser-storage only.

Now:
- Load pulls records from backend.
- Add sends new record to backend.
- Edit updates record through backend.

Code:
- [src/pages/MedicalHistory/MedicalHistory.jsx](src/pages/MedicalHistory/MedicalHistory.jsx#L12)
- [src/pages/MedicalHistory/MedicalHistory.jsx](src/pages/MedicalHistory/MedicalHistory.jsx#L63)
- [src/pages/MedicalHistory/MedicalHistory.jsx](src/pages/MedicalHistory/MedicalHistory.jsx#L83)
- [src/pages/MedicalHistory/MedicalHistory.jsx](src/pages/MedicalHistory/MedicalHistory.jsx#L120)

### ELI5: Dashboard now shows backend data
Before: dashboard read browser storage snapshots.

Now:
- It loads user profile, appointments, predictions, and medical history from backend.
- It also clears auth tokens on logout.

Code:
- [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L4)
- [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L46)
- [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L55)
- [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L68)
- [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L89)
- [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L103)
- [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L141)

### ELI5: Predictions and risk history are consistent now
Prediction already called backend, but now it uses the shared API helper.
Risk history now loads prediction history from backend.

Code:
- [src/pages/Prediction/Prediction.jsx](src/pages/Prediction/Prediction.jsx#L6)
- [src/pages/Prediction/Prediction.jsx](src/pages/Prediction/Prediction.jsx#L71)
- [src/pages/Prediction/RiskHistory.jsx](src/pages/Prediction/RiskHistory.jsx#L5)
- [src/pages/Prediction/RiskHistory.jsx](src/pages/Prediction/RiskHistory.jsx#L20)

---

## Deep Dive: What Changed and Why

### 1) Shared API client
File added:
- [src/api/client.js](src/api/client.js)

What it does:
- Defines backend base URL with optional environment override.
- Builds request headers and injects Bearer token when provided.
- Normalizes error parsing so all pages can use simple try/catch.
- Exposes apiGet, apiPost, and apiPut helpers.

Key lines:
- Base URL: [src/api/client.js](src/api/client.js#L1)
- Auth header injection: [src/api/client.js](src/api/client.js#L9)
- Error normalization: [src/api/client.js](src/api/client.js#L21)
- Helper exports: [src/api/client.js](src/api/client.js#L33)

Why it matters:
- Removes duplicated fetch boilerplate.
- Keeps endpoint calls consistent across pages.
- Makes backend URL configurable for different environments.

### 2) Authentication flow rewired
Files changed:
- [src/pages/Login/Login.jsx](src/pages/Login/Login.jsx)
- [src/pages/Register/Register.jsx](src/pages/Register/Register.jsx)

Login behavior now:
1. Calls backend login endpoint.
2. Stores access_token and refresh_token.
3. Calls auth me endpoint for canonical profile data.
4. Stores a UI snapshot in local storage.

Citations:
- Login request: [src/pages/Login/Login.jsx](src/pages/Login/Login.jsx#L29)
- Token persistence: [src/pages/Login/Login.jsx](src/pages/Login/Login.jsx#L34)
- Profile pull: [src/pages/Login/Login.jsx](src/pages/Login/Login.jsx#L37)
- Navigation to dashboard: [src/pages/Login/Login.jsx](src/pages/Login/Login.jsx#L53)

Register behavior now:
1. Builds full_name from first and last name.
2. Calls backend register endpoint.
3. Keeps extra non-backend form fields in local snapshot for UI continuity.

Citations:
- Full name composition: [src/pages/Register/Register.jsx](src/pages/Register/Register.jsx#L28)
- Register API call: [src/pages/Register/Register.jsx](src/pages/Register/Register.jsx#L36)
- Local user snapshot: [src/pages/Register/Register.jsx](src/pages/Register/Register.jsx#L42)

Why it matters:
- Auth is now backed by real server state and JWTs.
- Protected endpoints can now be called by frontend pages.

### 3) Appointment create/list/edit/cancel rewired
Files changed:
- [src/pages/Appointment/Appointment.jsx](src/pages/Appointment/Appointment.jsx)
- [src/pages/Appointment/UpcomingAppointments.jsx](src/pages/Appointment/UpcomingAppointments.jsx)

Create page behavior:
- Converts selected human-readable time to a backend-friendly datetime.
- Sends provider_name, start_time, end_time, and reason to backend.
- Updates local cache for immediate dashboard compatibility.

Citations:
- Time conversion helper: [src/pages/Appointment/Appointment.jsx](src/pages/Appointment/Appointment.jsx#L7)
- Submit logic: [src/pages/Appointment/Appointment.jsx](src/pages/Appointment/Appointment.jsx#L51)
- Backend create call: [src/pages/Appointment/Appointment.jsx](src/pages/Appointment/Appointment.jsx#L68)

Upcoming page behavior:
- Fetches appointments from backend.
- Maps backend shape to UI shape.
- Uses backend cancel endpoint.
- Uses backend update endpoint for edits.

Citations:
- Data load call: [src/pages/Appointment/UpcomingAppointments.jsx](src/pages/Appointment/UpcomingAppointments.jsx#L83)
- Cancel endpoint usage: [src/pages/Appointment/UpcomingAppointments.jsx](src/pages/Appointment/UpcomingAppointments.jsx#L126)
- Edit endpoint usage: [src/pages/Appointment/UpcomingAppointments.jsx](src/pages/Appointment/UpcomingAppointments.jsx#L162)

Why it matters:
- Appointment data is now durable and user-specific in backend storage.
- Editing and cancellation are reflected in server state.

### 4) Medical history rewired (load/add/edit)
File changed:
- [src/pages/MedicalHistory/MedicalHistory.jsx](src/pages/MedicalHistory/MedicalHistory.jsx)

Behavior now:
- Loads medical history records from backend.
- Maps backend condition_name and notes into existing sectioned UI model.
- Adds entries with backend create endpoint.
- Edits entries with backend update endpoint.

Citations:
- API imports: [src/pages/MedicalHistory/MedicalHistory.jsx](src/pages/MedicalHistory/MedicalHistory.jsx#L12)
- Mapping function: [src/pages/MedicalHistory/MedicalHistory.jsx](src/pages/MedicalHistory/MedicalHistory.jsx#L31)
- Load request: [src/pages/MedicalHistory/MedicalHistory.jsx](src/pages/MedicalHistory/MedicalHistory.jsx#L74)
- Create request: [src/pages/MedicalHistory/MedicalHistory.jsx](src/pages/MedicalHistory/MedicalHistory.jsx#L96)
- Update request: [src/pages/MedicalHistory/MedicalHistory.jsx](src/pages/MedicalHistory/MedicalHistory.jsx#L137)

Note:
- Delete remains intentionally unsupported because there is no delete route in current backend API for medical history.
- Current user request explicitly said delete is not needed.

### 5) Dashboard summary rewired
File changed:
- [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx)

Behavior now:
- On page load, fetches authenticated profile.
- Fetches appointments and maps them for existing UI cards.
- Fetches prediction history and shows latest risk result.
- Fetches medical history and builds summary counts.
- Removes auth tokens on logout.

Citations:
- Dashboard loader start: [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L46)
- Profile fetch: [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L55)
- Appointment fetch/map: [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L68)
- Prediction fetch/map: [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L89)
- Medical history summary fetch/map: [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L103)
- Token clear on logout: [src/pages/Dashboard/Dashboard.jsx](src/pages/Dashboard/Dashboard.jsx#L141)

### 6) Prediction and risk history consistency
Files changed:
- [src/pages/Prediction/Prediction.jsx](src/pages/Prediction/Prediction.jsx)
- [src/pages/Prediction/RiskHistory.jsx](src/pages/Prediction/RiskHistory.jsx)

Behavior now:
- Prediction submit uses the shared API helper instead of direct fetch boilerplate.
- Risk history requests backend prediction history endpoint and falls back to local cache if request fails.

Citations:
- Prediction helper usage import: [src/pages/Prediction/Prediction.jsx](src/pages/Prediction/Prediction.jsx#L6)
- Prediction API call: [src/pages/Prediction/Prediction.jsx](src/pages/Prediction/Prediction.jsx#L71)
- Risk history fetch: [src/pages/Prediction/RiskHistory.jsx](src/pages/Prediction/RiskHistory.jsx#L20)
- Risk history fallback: [src/pages/Prediction/RiskHistory.jsx](src/pages/Prediction/RiskHistory.jsx#L33)

---

## Operational Notes

### About the readonly database error you saw
The readonly error came from runtime process state, not from the frontend integration code itself.

Observed behavior:
- Backend process held a stale database handle and writes failed with sqlite readonly messages.

Operational fix used:
- Restart backend process cleanly so it reopens the active database file.

Recommended run command:
- Start backend from the backend directory context, or use absolute paths.

---

## What Was Not Added (Per Your Request)
- No root one-command launcher script was added.
- No medical history delete API wiring was added.

---

## Quick Verification Checklist
1. Register a new user from frontend register page.
2. Login from frontend login page.
3. Book an appointment.
4. Open upcoming appointments and edit or cancel one.
5. Add a medical history entry and edit it.
6. Run a prediction and open risk history.

If all six work, the frontend-backend integration path is functioning for the implemented scope.
