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
