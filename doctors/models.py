from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


class Doctor(models.Model):
    """
    Doctor model to store doctor information.
    Doctors can be assigned to multiple patients.
    """
    SPECIALIZATION_CHOICES = [
        ('CARDIOLOGY', 'Cardiology'),
        ('DERMATOLOGY', 'Dermatology'),
        ('ENDOCRINOLOGY', 'Endocrinology'),
        ('GASTROENTEROLOGY', 'Gastroenterology'),
        ('GENERAL_MEDICINE', 'General Medicine'),
        ('NEUROLOGY', 'Neurology'),
        ('ONCOLOGY', 'Oncology'),
        ('ORTHOPEDICS', 'Orthopedics'),
        ('PEDIATRICS', 'Pediatrics'),
        ('PSYCHIATRY', 'Psychiatry'),
        ('RADIOLOGY', 'Radiology'),
        ('SURGERY', 'Surgery'),
        ('OTHER', 'Other'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    
    # Professional Details
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    years_of_experience = models.PositiveIntegerField()
    qualification = models.CharField(max_length=200)
    
    # Contact Information
    clinic_address = models.TextField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Availability
    available_days = models.CharField(
        max_length=100,
        help_text="e.g., Monday-Friday, Saturday"
    )
    available_time = models.CharField(
        max_length=100,
        help_text="e.g., 9:00 AM - 5:00 PM"
    )
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'doctors'
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        ordering = ['name']

    def __str__(self):
        return f"Dr. {self.name} - {self.get_specialization_display()}"
