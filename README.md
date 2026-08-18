# CarePortal

## Product Vision

For patients who want a simpler way to manage their healthcare information and understand potential health risks, CarePortal is a web-based healthcare platform that allows users to register, manage appointments, maintain a basic medical history, and receive a machine-learning-based diabetes risk prediction.

Unlike basic appointment-booking systems that only allow patients to schedule visits, CarePortal combines appointment management, patient medical information, and predictive healthcare features in one platform. Patients can access their dashboard, review upcoming appointments, update their medical history, and submit health information to receive an estimated diabetes-risk result.

CarePortal is designed to make basic healthcare management more organized and accessible while helping users become more aware of potential diabetes risk factors.

---

## System Architecture

Below is our architectural plan for the final development of CarePortal.

The patient interacts with the CarePortal frontend to register, log in, manage appointments, enter medical history, and request a diabetes-risk prediction.

The frontend communicates with the Python backend through REST API requests and JSON responses. The backend handles authentication, validation, application logic, database communication, and machine-learning integration.

For diabetes-risk predictions, the backend sends the patient's submitted health information to the machine-learning module. The model returns a prediction, which is then displayed on the patient's dashboard.

```text
Patient / User
      |
      v
CarePortal Web Interface
HTML / CSS / JavaScript
      |
      | HTTP requests and JSON responses
      v
FastAPI Backend
Authentication, validation, REST APIs, and business logic
      |
      |-------------------------------|
      |                               |
      v                               v
PostgreSQL / MySQL             ML Prediction Module
Users                          Python
Patients                       pandas
Doctors                        scikit-learn
Appointments                   PyTorch
Medical History
Predictions
```
---

## System Layers

### Presentation Layer

The presentation layer consists of the patient-facing web interface built with HTML, CSS, and JavaScript.

The interface includes:

- Registration and login pages
- Patient dashboard
- Appointment-booking page
- Appointment history
- Medical-history form
- Diabetes-risk prediction form
- Prediction-results page
- Account and profile management

### API Layer

The API layer is built using Python with FastAPI.

It is responsible for:

- Registration and login requests
- Authentication and authorization
- Appointment management
- Medical-history requests
- Patient information
- Input validation
- Error handling
- Diabetes-risk prediction requests
- Communication between the frontend and database


### Data Access Layer

The data access layer manages database queries and data-persistence operations.

It allows the backend to create, retrieve, update, and manage patient records, appointments, medical history, doctors, and prediction results.

### Database Layer

The database stores the application's persistent data.

The planned database includes:

- Users
- Patients
- Doctors
- Appointments
- Medical history
- Prediction results

### Machine Learning Layer

The machine-learning layer predicts whether a patient may be at risk of diabetes.

The prediction is treated as a binary-classification problem:

- `0`: No diabetes
- `1`: Diabetes

The model uses patient information such as:

- Age
- Gender
- BMI
- HbA1c level
- Blood-glucose level
- Hypertension
- Heart-disease status
- Smoking history

---

## Frontend (UI) Quick Start

The UI app from the `UI` branch is a Create React App project.

In the project root, you can run:

- `npm install`
- `npm start`
- `npm test`
- `npm run build`
