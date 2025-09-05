-- Script to create the healthcare database and user
-- Run this script as PostgreSQL superuser

-- Create database
CREATE DATABASE healthcare_db;

-- Create user (optional - you can use existing postgres user)
CREATE USER healthcare_user WITH PASSWORD 'healthcare_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO healthcare_user;

-- Connect to the database
\c healthcare_db;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO healthcare_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO healthcare_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO healthcare_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO healthcare_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO healthcare_user;
