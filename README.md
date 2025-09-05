<<<<<<< HEAD
# Healthcare Backend API

A Django REST Framework-based backend system for managing healthcare data including patients, doctors, and their relationships.

## Features

- User authentication with JWT tokens
- Patient management (CRUD operations)
- Doctor management (CRUD operations)
- Patient-Doctor mapping system
- PostgreSQL database integration
- RESTful API design

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

### Installation

1. Clone the repository and navigate to the project directory

2. Create a virtual environment:
\`\`\`bash
python -m venv healthcare_env
healthcare_env\Scripts\activate  # On Windows
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Set up PostgreSQL database:
   - Create a database named `healthcare_db`
   - Update database credentials in `.env` file

5. Copy environment variables:
\`\`\`bash
copy .env.example .env
\`\`\`
   - Update the `.env` file with your database credentials and secret key

6. Run migrations:
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

7. Create a superuser (optional):
\`\`\`bash
python manage.py createsuperuser
\`\`\`

8. Start the development server:
\`\`\`bash
python manage.py runserver
\`\`\`

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login user

### Patients
- `GET /api/patients/` - List all patients
- `POST /api/patients/` - Create a new patient
- `GET /api/patients/<id>/` - Get patient details
- `PUT /api/patients/<id>/` - Update patient
- `DELETE /api/patients/<id>/` - Delete patient

### Doctors
- `GET /api/doctors/` - List all doctors
- `POST /api/doctors/` - Create a new doctor
- `GET /api/doctors/<id>/` - Get doctor details
- `PUT /api/doctors/<id>/` - Update doctor
- `DELETE /api/doctors/<id>/` - Delete doctor

### Patient-Doctor Mappings
- `GET /api/mappings/` - List all mappings
- `POST /api/mappings/` - Create a new mapping
- `GET /api/mappings/<patient_id>/` - Get doctors for a patient
- `DELETE /api/mappings/<id>/` - Delete mapping

## Testing

Use Postman or any API client to test the endpoints. Make sure to include the JWT token in the Authorization header for protected endpoints.
=======
# Healthcare-Backend
A secure and scalable backend system built with Django, Django REST Framework (DRF), and PostgreSQL for managing patients, doctors, and their relationships. This project demonstrates JWT authentication, role-based access, and RESTful API design for a healthcare application.

🚀 Features

User Authentication

Register & Login with JWT (using djangorestframework-simplejwt).

Patient Management

Add, view, update, and delete patient records.

Patients are linked to the authenticated user who created them.

Doctor Management

CRUD APIs for managing doctor records.

Patient-Doctor Mapping

Assign doctors to patients.

Retrieve mappings per patient.

Remove doctor-patient relationships.

Security

JWT authentication for protected endpoints.

Environment variables for sensitive configuration.

🛠️ Tech Stack

Backend Framework: Django, Django REST Framework

Database: PostgreSQL

Authentication: JWT (djangorestframework-simplejwt)

Tools: Django ORM, Environment Variables, Postman for API testing

📂 API Endpoints
🔐 Authentication

POST /api/auth/register/ → Register new user

POST /api/auth/login/ → Login & get JWT token

👩‍⚕️ Patient APIs

POST /api/patients/ → Add patient (Auth required)

GET /api/patients/ → Get all patients (Auth required)

GET /api/patients/<id>/ → Get patient by ID

PUT /api/patients/<id>/ → Update patient

DELETE /api/patients/<id>/ → Delete patient

🧑‍⚕️ Doctor APIs

POST /api/doctors/ → Add doctor (Auth required)

GET /api/doctors/ → Get all doctors

GET /api/doctors/<id>/ → Get doctor by ID

PUT /api/doctors/<id>/ → Update doctor

DELETE /api/doctors/<id>/ → Delete doctor

🔗 Patient-Doctor Mapping APIs

POST /api/mappings/ → Assign doctor to patient

GET /api/mappings/ → Get all mappings

GET /api/mappings/<patient_id>/ → Get doctors for a patient

DELETE /api/mappings/<id>/ → Remove mapping


⚙️ Installation & Setup
1. Clone repository
git clone https://github.com/<your-username>/healthcare-backend.git
cd healthcare-backend

2. Create virtual environment
python -m venv venv
venv\Scripts\activate    # on Windows
source venv/bin/activate # on Linux/Mac

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables

Create a .env file in project root:

SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

5. Apply migrations
python manage.py migrate

6. Run development server
python manage.py runserver

🧪 Testing APIs

Use Postman or cURL to test endpoints.

Example login request:

POST /api/auth/login/
{
  "email": "user@example.com",
  "password": "yourpassword"
}

📌 Future Enhancements

Role-based permissions (Admin, Doctor, Patient).

Pagination & filtering for APIs.

Docker setup for easy deployment.

Unit tests & CI pipeline with GitHub Actions.
>>>>>>> d614e44a41ab60e0bf1ff39fcb3cf72b729f4a8d
