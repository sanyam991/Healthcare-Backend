from django.db import models
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor

User = get_user_model()


class PatientDoctorMapping(models.Model):
    """
    Model to manage the relationship between patients and doctors.
    A patient can have multiple doctors, and a doctor can have multiple patients.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_mappings')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mappings_created')
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about this assignment")
    is_primary = models.BooleanField(
        default=False,
        help_text="Indicates if this doctor is the primary care physician for the patient"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'patient_doctor_mappings'
        verbose_name = 'Patient-Doctor Mapping'
        verbose_name_plural = 'Patient-Doctor Mappings'
        unique_together = ('patient', 'doctor')
        ordering = ['-assigned_at']

    def __str__(self):
        primary_text = " (Primary)" if self.is_primary else ""
        return f"{self.patient.name} -> Dr. {self.doctor.name}{primary_text}"

    def save(self, *args, **kwargs):
        """
        Override save method to ensure only one primary doctor per patient.
        """
        if self.is_primary:
            # Set all other mappings for this patient to non-primary
            PatientDoctorMapping.objects.filter(
                patient=self.patient,
                is_primary=True
            ).exclude(id=self.id).update(is_primary=False)
        
        super().save(*args, **kwargs)
