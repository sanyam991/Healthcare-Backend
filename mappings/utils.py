from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor
from django.db.models import Count, Q


def get_patient_care_team(patient_id):
    """
    Get the complete care team for a patient.
    
    Args:
        patient_id: Patient ID
        
    Returns:
        dict: Care team information
    """
    try:
        patient = Patient.objects.get(id=patient_id)
        mappings = PatientDoctorMapping.objects.filter(
            patient=patient,
            is_active=True
        ).select_related('doctor')
        
        primary_doctor = mappings.filter(is_primary=True).first()
        other_doctors = mappings.filter(is_primary=False)
        
        return {
            'patient': {
                'id': patient.id,
                'name': patient.name,
                'email': patient.email
            },
            'primary_doctor': {
                'id': primary_doctor.doctor.id,
                'name': primary_doctor.doctor.name,
                'specialization': primary_doctor.doctor.get_specialization_display(),
                'assigned_at': primary_doctor.assigned_at
            } if primary_doctor else None,
            'other_doctors': [
                {
                    'id': mapping.doctor.id,
                    'name': mapping.doctor.name,
                    'specialization': mapping.doctor.get_specialization_display(),
                    'assigned_at': mapping.assigned_at
                }
                for mapping in other_doctors
            ],
            'total_doctors': mappings.count()
        }
    except Patient.DoesNotExist:
        return None


def get_doctor_patient_load(doctor_id):
    """
    Get patient load information for a doctor.
    
    Args:
        doctor_id: Doctor ID
        
    Returns:
        dict: Patient load information
    """
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        mappings = PatientDoctorMapping.objects.filter(
            doctor=doctor,
            is_active=True
        ).select_related('patient')
        
        primary_patients = mappings.filter(is_primary=True)
        other_patients = mappings.filter(is_primary=False)
        
        return {
            'doctor': {
                'id': doctor.id,
                'name': doctor.name,
                'specialization': doctor.get_specialization_display()
            },
            'total_patients': mappings.count(),
            'primary_patients': primary_patients.count(),
            'secondary_patients': other_patients.count(),
            'patients': [
                {
                    'id': mapping.patient.id,
                    'name': mapping.patient.name,
                    'is_primary': mapping.is_primary,
                    'assigned_at': mapping.assigned_at
                }
                for mapping in mappings
            ]
        }
    except Doctor.DoesNotExist:
        return None


def suggest_doctors_for_patient(patient_id, max_suggestions=5):
    """
    Suggest doctors for a patient based on various criteria.
    
    Args:
        patient_id: Patient ID
        max_suggestions: Maximum number of suggestions
        
    Returns:
        list: Suggested doctors
    """
    try:
        patient = Patient.objects.get(id=patient_id)
        
        # Get doctors not already assigned to this patient
        assigned_doctor_ids = PatientDoctorMapping.objects.filter(
            patient=patient,
            is_active=True
        ).values_list('doctor_id', flat=True)
        
        available_doctors = Doctor.objects.filter(
            is_active=True
        ).exclude(
            id__in=assigned_doctor_ids
        ).annotate(
            patient_count=Count('patient_mappings', filter=Q(patient_mappings__is_active=True))
        ).order_by('patient_count', '-years_of_experience')
        
        suggestions = []
        for doctor in available_doctors[:max_suggestions]:
            suggestions.append({
                'id': doctor.id,
                'name': doctor.name,
                'specialization': doctor.get_specialization_display(),
                'years_of_experience': doctor.years_of_experience,
                'consultation_fee': doctor.consultation_fee,
                'current_patient_load': doctor.patient_count,
                'available_days': doctor.available_days
            })
        
        return suggestions
    except Patient.DoesNotExist:
        return []


def validate_mapping_constraints(patient_id, doctor_id):
    """
    Validate constraints before creating a mapping.
    
    Args:
        patient_id: Patient ID
        doctor_id: Doctor ID
        
    Returns:
        dict: Validation result
    """
    errors = []
    warnings = []
    
    try:
        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)
        
        # Check if patient is active
        if not patient.is_active:
            errors.append("Patient is inactive")
        
        # Check if doctor is active
        if not doctor.is_active:
            errors.append("Doctor is inactive")
        
        # Check if mapping already exists
        existing_mapping = PatientDoctorMapping.objects.filter(
            patient=patient,
            doctor=doctor,
            is_active=True
        ).exists()
        
        if existing_mapping:
            errors.append("Doctor is already assigned to this patient")
        
        # Check doctor's current patient load
        current_load = PatientDoctorMapping.objects.filter(
            doctor=doctor,
            is_active=True
        ).count()
        
        if current_load > 50:  # Arbitrary threshold
            warnings.append(f"Doctor has high patient load ({current_load} patients)")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
        
    except (Patient.DoesNotExist, Doctor.DoesNotExist):
        return {
            'valid': False,
            'errors': ['Patient or Doctor not found'],
            'warnings': []
        }
