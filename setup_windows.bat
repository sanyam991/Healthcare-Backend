@echo off
echo Healthcare Backend Setup Script for Windows
echo ==========================================

echo.
echo Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python is installed.

echo.
echo Step 2: Checking PostgreSQL installation...
psql --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: PostgreSQL is not in PATH
    echo Please ensure PostgreSQL is installed and accessible
    echo Download from: https://www.postgresql.org/download/windows/
)

echo.
echo Step 3: Creating virtual environment...
if exist healthcare_env (
    echo Virtual environment already exists.
) else (
    python -m venv healthcare_env
    echo Virtual environment created.
)

echo.
echo Step 4: Activating virtual environment...
call healthcare_env\Scripts\activate.bat

echo.
echo Step 5: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 6: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 7: Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo Environment file created. Please edit .env with your database credentials.
) else (
    echo Environment file already exists.
)

echo.
echo Step 8: Database setup...
echo Please ensure PostgreSQL is running and create the database:
echo   1. Open PostgreSQL command line (psql)
echo   2. Run: CREATE DATABASE healthcare_db;
echo   3. Press any key to continue after creating the database...
pause

echo.
echo Step 9: Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo Step 10: Creating superuser...
echo Please create a superuser account:
python manage.py createsuperuser

echo.
echo Step 11: Creating sample data (optional)...
set /p create_sample="Do you want to create sample data? (y/n): "
if /i "%create_sample%"=="y" (
    python scripts\create_sample_data.py
)

echo.
echo Setup completed successfully!
echo.
echo To start the development server:
echo   1. Activate virtual environment: healthcare_env\Scripts\activate.bat
echo   2. Run server: python manage.py runserver
echo.
echo The API will be available at: http://localhost:8000/
echo Admin panel: http://localhost:8000/admin/
echo.
pause
