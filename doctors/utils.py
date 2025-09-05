from .models import Doctor
from django.db.models import Count, Avg, Q


def get_doctor_recommendations(patient=None, specialization=None, max_fee=None):
    """
    Get doctor recommendations based on criteria.
    
    Args:
        patient: Patient instance (optional)
        specialization: Required specialization (optional)
        max_fee: Maximum consultation fee (optional)
        
    Returns:
        QuerySet: Recommended doctors
    """
    queryset = Doctor.objects.filter(is_active=True)
    
    if specialization:
        queryset = queryset.filter(specialization=specialization)
    
    if max_fee:
        queryset = queryset.filter(consultation_fee__lte=max_fee)
    
    # Annotate with patient count and order by experience and patient load
    queryset = queryset.annotate(
        patient_count=Count('patient_mappings', filter=Q(patient_mappings__is_active=True))
    ).order_by('-years_of_experience', 'patient_count', 'consultation_fee')
    
    return queryset[:10]  # Return top 10 recommendations


def get_specialization_stats():
    """
    Get statistics for all specializations.
    
    Returns:
        dict: Specialization statistics
    """
    stats = {}
    
    for choice in Doctor.SPECIALIZATION_CHOICES:
        specialization_code = choice[0]
        specialization_name = choice[1]
        
        doctors = Doctor.objects.filter(
            specialization=specialization_code,
            is_active=True
        )
        
        if doctors.exists():
            stats[specialization_name] = {
                'total_doctors': doctors.count(),
                'avg_experience': doctors.aggregate(Avg('years_of_experience'))['years_of_experience__avg'],
                'avg_fee': doctors.aggregate(Avg('consultation_fee'))['consultation_fee__avg'],
                'total_patients': doctors.aggregate(
                    total=Count('patient_mappings', filter=Q(patient_mappings__is_active=True))
                )['total']
            }
    
    return stats


def validate_doctor_availability(doctor, day=None):
    """
    Validate if doctor is available on a specific day.
    
    Args:
        doctor: Doctor instance
        day: Day of the week (optional)
        
    Returns:
        bool: True if available, False otherwise
    """
    if not doctor.is_active:
        return False
    
    if day and day.lower() not in doctor.available_days.lower():
        return False
    
    return True
