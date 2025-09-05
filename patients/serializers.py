from rest_framework import serializers
from .models import Patient
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    Handles patient creation, retrieval, and updates.
    """
    age = serializers.ReadOnlyField()
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'email', 'phone_number', 'date_of_birth', 
            'gender', 'address', 'medical_history', 'allergies',
            'emergency_contact_name', 'emergency_contact_phone',
            'age', 'created_by', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'age', 'created_by', 'created_at', 'updated_at']

    def validate_email(self, value):
        """
        Validate that email is unique, excluding current instance during updates.
        """
        queryset = Patient.objects.filter(email=value.lower())
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("A patient with this email already exists.")
        return value.lower()

    def validate_phone_number(self, value):
        """
        Validate phone number format.
        """
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Please enter a valid phone number.")
        return value

    def validate_emergency_contact_phone(self, value):
        """
        Validate emergency contact phone number format.
        """
        if not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Please enter a valid emergency contact phone number.")
        return value

    def validate_date_of_birth(self, value):
        """
        Validate that date of birth is not in the future.
        """
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def create(self, validated_data):
        """
        Create a new patient instance.
        """
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class PatientListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for patient list view.
    """
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'email', 'phone_number', 'gender', 
            'age', 'created_at', 'is_active'
        ]


class PatientDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for patient detail view.
    """
    age = serializers.ReadOnlyField()
    created_by = serializers.StringRelatedField(read_only=True)
    doctor_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'email', 'phone_number', 'date_of_birth', 
            'gender', 'address', 'medical_history', 'allergies',
            'emergency_contact_name', 'emergency_contact_phone',
            'age', 'doctor_count', 'created_by', 'created_at', 
            'updated_at', 'is_active'
        ]

    def get_doctor_count(self, obj):
        """
        Get the number of doctors assigned to this patient.
        """
        return obj.doctor_mappings.filter(is_active=True).count()
