from rest_framework import serializers
from .models import Doctor
from django.contrib.auth import get_user_model

User = get_user_model()


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model.
    Handles doctor creation, retrieval, and updates.
    """
    created_by = serializers.StringRelatedField(read_only=True)
    patient_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'email', 'phone_number', 'license_number',
            'specialization', 'years_of_experience', 'qualification',
            'clinic_address', 'consultation_fee', 'available_days',
            'available_time', 'patient_count', 'created_by', 
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'patient_count', 'created_by', 'created_at', 'updated_at']

    def get_patient_count(self, obj):
        """
        Get the number of patients assigned to this doctor.
        """
        return obj.patient_mappings.filter(is_active=True).count()

    def validate_email(self, value):
        """
        Validate that email is unique, excluding current instance during updates.
        """
        queryset = Doctor.objects.filter(email=value.lower())
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value.lower()

    def validate_license_number(self, value):
        """
        Validate that license number is unique, excluding current instance during updates.
        """
        queryset = Doctor.objects.filter(license_number=value.upper())
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("A doctor with this license number already exists.")
        return value.upper()

    def validate_phone_number(self, value):
        """
        Validate phone number format.
        """
        if not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Please enter a valid phone number.")
        return value

    def validate_years_of_experience(self, value):
        """
        Validate years of experience.
        """
        if value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative.")
        if value > 70:
            raise serializers.ValidationError("Years of experience seems unrealistic.")
        return value

    def validate_consultation_fee(self, value):
        """
        Validate consultation fee.
        """
        if value < 0:
            raise serializers.ValidationError("Consultation fee cannot be negative.")
        if value > 10000:
            raise serializers.ValidationError("Consultation fee seems unrealistic.")
        return value

    def create(self, validated_data):
        """
        Create a new doctor instance.
        """
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class DoctorListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for doctor list view.
    """
    patient_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'email', 'phone_number', 'specialization',
            'years_of_experience', 'consultation_fee', 'patient_count',
            'available_days', 'is_active'
        ]

    def get_patient_count(self, obj):
        """
        Get the number of patients assigned to this doctor.
        """
        return obj.patient_mappings.filter(is_active=True).count()


class DoctorDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for doctor detail view.
    """
    created_by = serializers.StringRelatedField(read_only=True)
    patient_count = serializers.SerializerMethodField()
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'email', 'phone_number', 'license_number',
            'specialization', 'specialization_display', 'years_of_experience', 
            'qualification', 'clinic_address', 'consultation_fee',
            'available_days', 'available_time', 'patient_count',
            'created_by', 'created_at', 'updated_at', 'is_active'
        ]

    def get_patient_count(self, obj):
        """
        Get the number of patients assigned to this doctor.
        """
        return obj.patient_mappings.filter(is_active=True).count()


class DoctorSearchSerializer(serializers.ModelSerializer):
    """
    Serializer for doctor search results.
    """
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialization', 'specialization_display',
            'years_of_experience', 'consultation_fee', 'available_days',
            'clinic_address'
        ]
