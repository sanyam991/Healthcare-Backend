from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor
from patients.serializers import PatientListSerializer
from doctors.serializers import DoctorListSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for PatientDoctorMapping model.
    Handles mapping creation, retrieval, and updates.
    """
    assigned_by = serializers.StringRelatedField(read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.get_specialization_display', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'patient_name', 'doctor_name',
            'doctor_specialization', 'notes', 'is_primary', 'is_active',
            'assigned_by', 'assigned_at'
        ]
        read_only_fields = ['id', 'assigned_by', 'assigned_at']

    def validate(self, attrs):
        """
        Validate the mapping data.
        """
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        request = self.context.get('request')

        # Check if patient belongs to the current user
        if patient and patient.created_by != request.user:
            raise serializers.ValidationError({
                'patient': 'You can only assign doctors to your own patients.'
            })

        # Check if patient and doctor are active
        if patient and not patient.is_active:
            raise serializers.ValidationError({
                'patient': 'Cannot assign doctor to inactive patient.'
            })

        if doctor and not doctor.is_active:
            raise serializers.ValidationError({
                'doctor': 'Cannot assign inactive doctor to patient.'
            })

        # Check for existing mapping (only for creation)
        if not self.instance:
            existing_mapping = PatientDoctorMapping.objects.filter(
                patient=patient,
                doctor=doctor,
                is_active=True
            ).exists()
            
            if existing_mapping:
                raise serializers.ValidationError(
                    'This doctor is already assigned to this patient.'
                )

        return attrs

    def create(self, validated_data):
        """
        Create a new patient-doctor mapping.
        """
        validated_data['assigned_by'] = self.context['request'].user
        return super().create(validated_data)


class PatientDoctorMappingDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for PatientDoctorMapping with nested patient and doctor info.
    """
    patient = PatientListSerializer(read_only=True)
    doctor = DoctorListSerializer(read_only=True)
    assigned_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'notes', 'is_primary',
            'is_active', 'assigned_by', 'assigned_at'
        ]


class PatientDoctorMappingListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for mapping list view.
    """
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    patient_email = serializers.CharField(source='patient.email', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.get_specialization_display', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient_name', 'patient_email', 'doctor_name',
            'doctor_specialization', 'is_primary', 'assigned_at', 'is_active'
        ]


class DoctorAssignmentSerializer(serializers.Serializer):
    """
    Serializer for bulk doctor assignment to multiple patients.
    """
    doctor_id = serializers.IntegerField()
    patient_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    is_primary = serializers.BooleanField(default=False)

    def validate_doctor_id(self, value):
        """
        Validate that doctor exists and is active.
        """
        try:
            doctor = Doctor.objects.get(id=value, is_active=True)
            return value
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor not found or inactive.")

    def validate_patient_ids(self, value):
        """
        Validate that all patients exist, are active, and belong to current user.
        """
        request = self.context.get('request')
        patients = Patient.objects.filter(
            id__in=value,
            created_by=request.user,
            is_active=True
        )
        
        if len(patients) != len(value):
            raise serializers.ValidationError(
                "Some patients not found, inactive, or don't belong to you."
            )
        
        return value


class PatientDoctorsSerializer(serializers.ModelSerializer):
    """
    Serializer to show all doctors assigned to a patient.
    """
    doctors = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = ['id', 'name', 'email', 'doctors']

    def get_doctors(self, obj):
        """
        Get all active doctors assigned to this patient.
        """
        mappings = obj.doctor_mappings.filter(is_active=True).select_related('doctor')
        return [
            {
                'mapping_id': mapping.id,
                'doctor_id': mapping.doctor.id,
                'doctor_name': mapping.doctor.name,
                'specialization': mapping.doctor.get_specialization_display(),
                'is_primary': mapping.is_primary,
                'assigned_at': mapping.assigned_at,
                'notes': mapping.notes
            }
            for mapping in mappings
        ]
