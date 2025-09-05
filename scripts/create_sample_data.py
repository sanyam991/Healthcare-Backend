#!/usr/bin/env python
"""
Script to create sample data for the healthcare backend.
Run this script after setting up the database and running migrations.
"""

import os
import sys
import django
from datetime import date, datetime, timedelta
from decimal import Decimal

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping

User = get_user_model()

def create_sample_users():
    """Create sample users for testing."""
    print("Creating sample users...")
    
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        email='admin@healthcare.com',
        defaults={
            'username': 'admin',
            'name': 'Healthcare Admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"Created admin user: {admin_user.email}")
    
    # Create test users
    test_users = [
        {
            'email': 'doctor1@healthcare.com',
            'username': 'doctor1',
            'name': 'Dr. John Smith',
            'password': 'doctor123'
        },
        {
            'email': 'doctor2@healthcare.com',
            'username': 'doctor2',
            'name': 'Dr. Sarah Johnson',
            'password': 'doctor123'
        },
        {
            'email': 'nurse1@healthcare.com',
            'username': 'nurse1',
            'name': 'Nurse Mary Wilson',
            'password': 'nurse123'
        }
    ]
    
    created_users = []
    for user_data in test_users:
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'username': user_data['username'],
                'name': user_data['name']
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"Created user: {user.email}")
        created_users.append(user)
    
    return [admin_user] + created_users

def create_sample_doctors(users):
    """Create sample doctors."""
    print("Creating sample doctors...")
    
    sample_doctors = [
        {
            'name': 'Dr. Michael Brown',
            'email': 'michael.brown@hospital.com',
            'phone_number': '+1234567890',
            'license_number': 'MD001234',
            'specialization': 'CARDIOLOGY',
            'years_of_experience': 15,
            'qualification': 'MD, FACC - Harvard Medical School',
            'clinic_address': '123 Heart Street, Medical District, City',
            'consultation_fee': Decimal('200.00'),
            'available_days': 'Monday-Friday',
            'available_time': '9:00 AM - 5:00 PM'
        },
        {
            'name': 'Dr. Emily Davis',
            'email': 'emily.davis@hospital.com',
            'phone_number': '+1234567891',
            'license_number': 'MD001235',
            'specialization': 'PEDIATRICS',
            'years_of_experience': 12,
            'qualification': 'MD, FAAP - Johns Hopkins University',
            'clinic_address': '456 Children Ave, Pediatric Center, City',
            'consultation_fee': Decimal('150.00'),
            'available_days': 'Monday-Saturday',
            'available_time': '8:00 AM - 6:00 PM'
        },
        {
            'name': 'Dr. Robert Wilson',
            'email': 'robert.wilson@hospital.com',
            'phone_number': '+1234567892',
            'license_number': 'MD001236',
            'specialization': 'ORTHOPEDICS',
            'years_of_experience': 20,
            'qualification': 'MD, FAAOS - Mayo Clinic',
            'clinic_address': '789 Bone Street, Orthopedic Center, City',
            'consultation_fee': Decimal('250.00'),
            'available_days': 'Tuesday-Saturday',
            'available_time': '10:00 AM - 4:00 PM'
        },
        {
            'name': 'Dr. Lisa Anderson',
            'email': 'lisa.anderson@hospital.com',
            'phone_number': '+1234567893',
            'license_number': 'MD001237',
            'specialization': 'DERMATOLOGY',
            'years_of_experience': 8,
            'qualification': 'MD, FAAD - Stanford University',
            'clinic_address': '321 Skin Care Blvd, Dermatology Clinic, City',
            'consultation_fee': Decimal('180.00'),
            'available_days': 'Monday-Friday',
            'available_time': '9:00 AM - 3:00 PM'
        },
        {
            'name': 'Dr. James Taylor',
            'email': 'james.taylor@hospital.com',
            'phone_number': '+1234567894',
            'license_number': 'MD001238',
            'specialization': 'GENERAL_MEDICINE',
            'years_of_experience': 25,
            'qualification': 'MD, FACP - University of Pennsylvania',
            'clinic_address': '654 General Health St, Family Medicine, City',
            'consultation_fee': Decimal('120.00'),
            'available_days': 'Monday-Sunday',
            'available_time': '7:00 AM - 7:00 PM'
        }
    ]
    
    created_doctors = []
    for i, doctor_data in enumerate(sample_doctors):
        doctor, created = Doctor.objects.get_or_create(
            email=doctor_data['email'],
            defaults={
                **doctor_data,
                'created_by': users[i % len(users)]
            }
        )
        if created:
            print(f"Created doctor: {doctor.name}")
        created_doctors.append(doctor)
    
    return created_doctors

def create_sample_patients(users):
    """Create sample patients."""
    print("Creating sample patients...")
    
    sample_patients = [
        {
            'name': 'Alice Johnson',
            'email': 'alice.johnson@email.com',
            'phone_number': '+1987654321',
            'date_of_birth': date(1985, 3, 15),
            'gender': 'F',
            'address': '123 Main St, Apartment 4B, City, State 12345',
            'medical_history': 'Hypertension, managed with medication. No known allergies.',
            'allergies': 'None',
            'emergency_contact_name': 'Bob Johnson (Husband)',
            'emergency_contact_phone': '+1987654322'
        },
        {
            'name': 'David Smith',
            'email': 'david.smith@email.com',
            'phone_number': '+1987654323',
            'date_of_birth': date(1978, 7, 22),
            'gender': 'M',
            'address': '456 Oak Avenue, House 12, City, State 12345',
            'medical_history': 'Type 2 Diabetes, well controlled. Previous knee surgery in 2019.',
            'allergies': 'Penicillin',
            'emergency_contact_name': 'Mary Smith (Wife)',
            'emergency_contact_phone': '+1987654324'
        },
        {
            'name': 'Emma Brown',
            'email': 'emma.brown@email.com',
            'phone_number': '+1987654325',
            'date_of_birth': date(2010, 11, 8),
            'gender': 'F',
            'address': '789 Pine Street, City, State 12345',
            'medical_history': 'Asthma, uses inhaler as needed. Regular pediatric checkups.',
            'allergies': 'Peanuts, Tree nuts',
            'emergency_contact_name': 'Jennifer Brown (Mother)',
            'emergency_contact_phone': '+1987654326'
        },
        {
            'name': 'Michael Davis',
            'email': 'michael.davis@email.com',
            'phone_number': '+1987654327',
            'date_of_birth': date(1992, 1, 30),
            'gender': 'M',
            'address': '321 Elm Drive, Unit 8, City, State 12345',
            'medical_history': 'Healthy young adult. Regular exercise routine.',
            'allergies': 'Shellfish',
            'emergency_contact_name': 'Patricia Davis (Mother)',
            'emergency_contact_phone': '+1987654328'
        },
        {
            'name': 'Sarah Wilson',
            'email': 'sarah.wilson@email.com',
            'phone_number': '+1987654329',
            'date_of_birth': date(1965, 9, 12),
            'gender': 'F',
            'address': '654 Maple Lane, City, State 12345',
            'medical_history': 'Osteoarthritis in knees. Takes calcium supplements.',
            'allergies': 'Latex',
            'emergency_contact_name': 'Robert Wilson (Husband)',
            'emergency_contact_phone': '+1987654330'
        }
    ]
    
    created_patients = []
    for i, patient_data in enumerate(sample_patients):
        patient, created = Patient.objects.get_or_create(
            email=patient_data['email'],
            defaults={
                **patient_data,
                'created_by': users[i % len(users)]
            }
        )
        if created:
            print(f"Created patient: {patient.name}")
        created_patients.append(patient)
    
    return created_patients

def create_sample_mappings(patients, doctors, users):
    """Create sample patient-doctor mappings."""
    print("Creating sample patient-doctor mappings...")
    
    # Create some logical mappings
    mappings_data = [
        # Alice Johnson (Hypertension) -> Cardiologist + General Medicine
        {'patient': patients[0], 'doctor': doctors[0], 'is_primary': True, 'notes': 'Primary care for hypertension management'},
        {'patient': patients[0], 'doctor': doctors[4], 'is_primary': False, 'notes': 'General health monitoring'},
        
        # David Smith (Diabetes + Knee surgery) -> General Medicine + Orthopedics
        {'patient': patients[1], 'doctor': doctors[4], 'is_primary': True, 'notes': 'Diabetes management and general care'},
        {'patient': patients[1], 'doctor': doctors[2], 'is_primary': False, 'notes': 'Post-surgical knee care'},
        
        # Emma Brown (Child with Asthma) -> Pediatrics
        {'patient': patients[2], 'doctor': doctors[1], 'is_primary': True, 'notes': 'Pediatric care and asthma management'},
        
        # Michael Davis (Healthy young adult) -> General Medicine
        {'patient': patients[3], 'doctor': doctors[4], 'is_primary': True, 'notes': 'Annual checkups and preventive care'},
        
        # Sarah Wilson (Osteoarthritis) -> Orthopedics + General Medicine
        {'patient': patients[4], 'doctor': doctors[2], 'is_primary': True, 'notes': 'Osteoarthritis treatment'},
        {'patient': patients[4], 'doctor': doctors[4], 'is_primary': False, 'notes': 'General health monitoring'},
    ]
    
    created_mappings = []
    for mapping_data in mappings_data:
        mapping, created = PatientDoctorMapping.objects.get_or_create(
            patient=mapping_data['patient'],
            doctor=mapping_data['doctor'],
            defaults={
                'assigned_by': users[0],  # Admin user
                'is_primary': mapping_data['is_primary'],
                'notes': mapping_data['notes']
            }
        )
        if created:
            print(f"Created mapping: {mapping.patient.name} -> {mapping.doctor.name}")
        created_mappings.append(mapping)
    
    return created_mappings

def main():
    """Main function to create all sample data."""
    print("Starting sample data creation...")
    
    try:
        # Create users
        users = create_sample_users()
        
        # Create doctors
        doctors = create_sample_doctors(users)
        
        # Create patients
        patients = create_sample_patients(users)
        
        # Create mappings
        mappings = create_sample_mappings(patients, doctors, users)
        
        print(f"\nSample data creation completed successfully!")
        print(f"Created {len(users)} users")
        print(f"Created {len(doctors)} doctors")
        print(f"Created {len(patients)} patients")
        print(f"Created {len(mappings)} patient-doctor mappings")
        
        print("\nSample login credentials:")
        print("Admin: admin@healthcare.com / admin123")
        print("Doctor: doctor1@healthcare.com / doctor123")
        print("Nurse: nurse1@healthcare.com / nurse123")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
